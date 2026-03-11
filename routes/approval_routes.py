from fastapi import APIRouter
from app.database import get_post, update_post_status
from services.linkedin_service import publish_post

router = APIRouter()

@router.get("/approve/{post_id}")
def approve_post(post_id: int):
    post = get_post(post_id)
    if not post:
        return {"error": "Post not found"}
    if post[2] != "pending":
        return {"error": "Post already processed"}
    update_post_status(post_id, "approved")
    success = publish_post(post[1])
    if success:
        update_post_status(post_id, "posted")
        return {"message": "Post published to LinkedIn!"}
    else:
        return {"error": "Failed to publish to LinkedIn."}
