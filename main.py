
from fastapi import Request, Response, FastAPI, Depends, Security
from fastapi_jwt_auth import AuthJWT
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from middleware.engine import init_db
from sqlmodel import SQLModel

from src.auth.router import router as auth_router
from src.post.router import router as post_router

#from fastapi.security import OAuth2PasswordBearer
from fastapi.security.api_key import APIKeyHeader

app = FastAPI(debug=True)

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login") 

@app.on_event("startup")
async def on_startup():
    await init_db()


app.include_router(auth_router, prefix="/auth")
app.include_router(post_router, prefix="/post")

origins = ["*"]

api_key_header = APIKeyHeader(name='Authorization')

@app.get('/')
def main(api_key: str = Security(api_key_header)):
    return api_key 

# def catch_exceptions_middleware(request: Request, call_next):
#     try:
#         return call_next(request)
#     except Exception as err:
#         return Response("Internal server error", status_code=500)


# app.middleware('http')(catch_exceptions_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,
                reload=False, timeout_keep_alive=600)
