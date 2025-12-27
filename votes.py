
from fastapi import APIRouter, Response, status, HTTPException, Depends
# from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import model
import schema
import OAuth2
# from main import get_db
from database import get_db

router = APIRouter(
    prefix="/votes",  # Prefix for all routes in this router
    # Tags for all routes in this router. It helps in grouping the routes in the documentation
    tags=['Votes'],
    # Apply authentication dependency to all routes in this router
    dependencies=[Depends(OAuth2.get_current_user)]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote, db: Session = Depends(get_db), current_user: model.Users = Depends(OAuth2.get_current_user)):
    post = db.query(model.Posts).filter(model.Posts.post_id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {vote.post_id} does not exist")

    vote_query = db.query(model.Votes).filter(
        model.Votes.post_id == vote.post_id,
        model.Votes.user_id == current_user.user_id
    )
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.user_id} has already voted on post {vote.post_id}")
        new_vote = model.Votes(post_id=vote.post_id, user_id=current_user.user_id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added successfully"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote removed successfully"}
    
