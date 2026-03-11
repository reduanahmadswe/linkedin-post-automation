from apscheduler.schedulers.background import BackgroundScheduler
from ai.generator import generate_post
from app.database import insert_post
from services.email_service import send_approval_email
import logging

scheduler = BackgroundScheduler()

def job():
    logging.info("Generating LinkedIn post...")
    post_content, topic = generate_post()
    post_id = insert_post(post_content)
    from services.linkedin_service import publish_post
    success = publish_post(post_content)
    if success:
        logging.info(f"Post published directly to LinkedIn: {post_id}")
    else:
        logging.error(f"Failed to publish post to LinkedIn: {post_id}")

def start_scheduler():
    scheduler.add_job(job, 'interval', minutes=1)
    scheduler.start()
