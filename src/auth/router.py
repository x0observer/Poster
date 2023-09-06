
from .service import *
from fastapi import Header, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(tags=["Authorization"])


@router.post("/self")
async def get_self(db: AsyncSession = Depends(get_async_session),  Authorize: AuthJWT = Depends(), api_key: str = Security(api_key_header)):
    return get_active_user(db=db, Authorize=Authorize)


form_data: OAuth2PasswordRequestForm = Depends()


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_async_session), Authorize: AuthJWT = Depends()):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid username or password")
    print("ACCESS_TOKEN_EXPIRE_MINUTES: ", ACCESS_TOKEN_EXPIRE_MINUTES)

    print("__active_user__", user)
    access_token_expires = timedelta(minutes=30)
    access_token = Authorize.create_access_token(
        subject=user.username, expires_time=False
    )
    return {"access_token": access_token}


@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_async_session)):
    user = User(
        username=user.username,
        email=user.email,
        password_hash=pwd_context.hash(user.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
