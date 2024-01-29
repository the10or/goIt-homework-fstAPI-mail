from fastapi import APIRouter, status, Depends, HTTPException, Security, BackgroundTasks, Request, UploadFile
from fastapi.params import File
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from dependencies.database import get_db
from dependencies.cloudinary_client import upload
from repository import users as repository_users
from schemas.users import UserResponse, UserBase, TokenModel, RequestEmail
from models.contacts import User
from services.auth import auth_service
from services.email import send_email

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


@router.post("/signup", response_model=dict,
             status_code=status.HTTP_201_CREATED)
async def signup(body: UserBase,
                 background_tasks: BackgroundTasks,
                 request: Request,
                 db: Session = Depends(get_db)
                 ):
    exist_user = db.query(User).filter(User.email == body.email).first()
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exist"
        )
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)

    background_tasks.add_task(send_email, new_user.email, request.base_url)

    return {
        "user": UserResponse.model_validate(new_user),
        "message": "User created, check your email"
    }


@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email"
        )

    if not user.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not confirmed"
        )
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get("/refresh_token", response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security),
                        db: Session = Depends(get_db)):
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid refresh token")
    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get("/confirmed_email/{token}")
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    email = auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repository_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}


@router.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks,
                        request: Request, db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_email(body.email, db)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(send_email, user.email, request.base_url)
    return {"message": "Check your email for confirmation"}


@router.post('/upload_userpic')
async def upload_userpic(file: UploadFile = File(...), uploader=Depends(upload),
                         current_user=Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    try:
        content = file.file.read()
        res = uploader.upload(content)
        print(res['secure_url'])

    except Exception:
        return {"message": "Error uploading file"}
    finally:
        file.file.close()
    await repository_users.set_userpic(userpic=res['secure_url'], user=current_user, db=db)
    return {"message": f" File {file.filename} successfully uploaded"}
