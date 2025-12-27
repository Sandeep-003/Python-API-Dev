
from fastapi import APIRouter, Response, status, HTTPException, Depends
# from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import model
import schema
import OAuth2
# from main import get_db
from database import get_db

router = APIRouter(
    prefix="/posts",  # Prefix for all routes in this router
    # Tags for all routes in this router. It helps in grouping the routes in the documentation
    tags=['Posts'],
    # Apply authentication dependency to all routes in this router
    dependencies=[Depends(OAuth2.get_current_user)]
)

"""
Query: - INFO:     127.0.0.1:53524 - "GET /posts/all/ HTTP/1.1" 422 Unprocessable Entity
 Response: - {
  "detail": [
    {
      "type": "int_parsing",
      "loc": [
        "path",
        "post_id"
      ],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "all"
    }
  ]
}
What's happening

Your request GET /posts/all/ is being routed to the endpoint with the path parameter {post_id}.
FastAPI (Starlette) attempted to parse the path segment "all" as the integer post_id (you annotated post_id: int), so pydantic/int parsing failed and you get a 422 with message "Input should be a valid integer, unable to parse string as an integer".
Why that occurs

You defined the dynamic path ("/{post_id}/") before the static "/all/" route, so the router matched the dynamic route first and tried to use "all" as the dynamic parameter.
Even though the function expects an int, route-resolution already selected that path and only then validation occurs — hence the 422.
"""
@router.get("/all/", response_model=list[schema.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: str = Depends(OAuth2.get_current_user)):
    posts = db.query(model.Posts).filter(
        model.Posts.user_id == current_user.user_id).all()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return posts


@router.get("/{post_id}/", response_model=schema.PostResponse)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(OAuth2.get_current_user),
):
    print(f"Current authorized user ID: {current_user.user_id}")
    post = (
        db.query(model.Posts)
        .filter(
            model.Posts.user_id == current_user.user_id,
            model.Posts.post_id == post_id,
        )
        .first()
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return post




@router.post("/", response_model=schema.PostCreate, status_code=status.HTTP_201_CREATED)
def create_post(
    post: schema.PostCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(OAuth2.get_current_user),
):
    db_post = model.Posts(
        post_id=post.post_id,
        post_data=post.post_data,
        user_id=current_user.user_id,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.put("/{post_id}/", response_model=schema.PostResponse)
def update_response(post_id: int, post_update: schema.PostCreate, db: Session = Depends(get_db), current_user: str = Depends(OAuth2.get_current_user)):
    post = db.query(model.Posts).filter(model.Posts.post_id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to update this post")

    post.post_data = post_update.post_data
    post.user_id = current_user.user_id
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: str = Depends(OAuth2.get_current_user)):
    post = db.query(model.Posts).filter(model.Posts.post_id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found with post id : {post_id}")
    if post.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to delete this post")
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
