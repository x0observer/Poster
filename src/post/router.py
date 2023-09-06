from .service import *
from fastapi import Query, Header, Security
from typing import Annotated
from src.auth.contexts.permissons import UserPemissions
from src.auth.service import get_active_user, api_key_header
router = APIRouter()




@router.post("/create/", response_model=Post)
async def create_post(
    post: PostBase, 
    repository: PostRepository = Depends(get_post_repository), 
    active_user: UserPemissions = Depends(get_active_user),
    api_key: str = Security(api_key_header)
    ):
    print("__active_user__", active_user)
    created_post = await repository.create_post(post, active_user)
    return created_post


@router.get("/get/{post_id}", response_model=Optional[PostFull])
async def get_post(
    post_id: int,
    repository: PostRepository = Depends(get_post_repository),
    active_user: UserPemissions = Depends(get_active_user),
    api_key: str = Security(api_key_header)
):
   
    post = await repository.get_post(post_id, active_user)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found or out of access zone.")
    return post


@router.post("/get_all/", response_model=List[Post])
async def get_posts(
    page: int = Query(1, alias="page", description="Page number"),
    items_per_page: int = Query(10, alias="items_per_page", description="Items per page"),
    filters: dict = None,
    repository: PostRepository = Depends(get_post_repository),
    active_user: UserPemissions = Depends(get_active_user),
    api_key: str = Security(api_key_header)
):
    posts = await repository.get_posts(
        filters=filters,
        active_user=active_user,
        page=page,
        items_per_page=items_per_page,)
    return posts


@router.put("/update/{post_id}", response_model=Post)
async def update_post(
    post_id: int,
    updated_post: PostBase,
    repository: PostRepository = Depends(get_post_repository),
    active_user: UserPemissions = Depends(get_active_user),
    api_key: str = Security(api_key_header)
):

    updated_post_data = await repository.update_post(post_id, updated_post, active_user)
    if updated_post_data is None:
        raise HTTPException(status_code=404, detail="Post not found or out of access zone.")
    return updated_post_data


@router.patch("/patch/{post_id}", response_model=Post)
async def patch_post(
    post_id: int,
    patch_data: dict,
    repository: PostRepository = Depends(get_post_repository),
    active_user: UserPemissions = Depends(get_active_user),
    api_key: str = Security(api_key_header)
):

    updated_post_data = await repository.patch_post(post_id, patch_data, active_user)
    if updated_post_data is None:
        raise HTTPException(status_code=404, detail="Post not found or out of access zone.")
    return updated_post_data


@router.delete("/delete/{post_id}", response_model=Post)
async def delete_post(
    post_id: int,
    repository: PostRepository = Depends(get_post_repository),
    active_user: UserPemissions = Depends(get_active_user),
    api_key: str = Security(api_key_header)
):

    deleted_post_data = await repository.delete_post(post_id, active_user)
    if deleted_post_data is None:
        raise HTTPException(status_code=404, detail="Post not found or out of access zone.")
    return deleted_post_data




