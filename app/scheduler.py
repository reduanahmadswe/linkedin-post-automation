import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from ai.generator import generate_post
from app.database import insert_post
from services.email_service import send_approval_email
import logging
import pytz

scheduler = BackgroundScheduler()

# Bangladesh timezone (UTC+6)
TIMEZONE = pytz.timezone('Asia/Dhaka')

def job():
    logging.info("Generating LinkedIn post...")
    try:
        post_content, topic = generate_post()
        post_id = insert_post(post_content)
        from services.linkedin_service import publish_post
        success = publish_post(post_content)
        if success:
            logging.info(f"Post published successfully to LinkedIn: {post_id}")
        else:
            logging.error(f"Failed to publish post to LinkedIn: {post_id}")
    except Exception as e:
        logging.error(f"Error in job: {str(e)}")

def start_scheduler():
    # Post 1: Morning 9:00 AM Bangladesh Time (Best engagement - people check before work)
    scheduler.add_job(
        job, 
        CronTrigger(hour=9, minute=0, timezone=TIMEZONE),
        id='morning_post',
        name='Morning LinkedIn Post'
    )
    
    # Post 2: Evening 6:00 PM Bangladesh Time (Best engagement - after work hours)
    scheduler.add_job(
        job, 
        CronTrigger(hour=18, minute=0, timezone=TIMEZONE),
        id='evening_post',
        name='Evening LinkedIn Post'
    )
    
    scheduler.start()
    logging.info("Scheduler started - Posts scheduled at 9:00 AM and 6:00 PM (Bangladesh Time)")
