import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from ai.generator import generate_post
from app.database import insert_post
from services.linkedin_service import publish_to_linkedin
import logging
import pytz

scheduler = BackgroundScheduler()

# Bangladesh timezone (UTC+6)
TIMEZONE = pytz.timezone('Asia/Dhaka')

def job():
    """Generate humanized post and publish directly to LinkedIn."""
    logging.info("Generating humanized LinkedIn post...")
    try:
        # Generate already-humanized post
        post_content = generate_post()
        logging.info("Generated humanized LinkedIn post")
        
        # Publish directly to LinkedIn
        result = publish_to_linkedin(post_content)
        
        if result.get("success"):
            # Save to database as posted
            post_id = insert_post(post_content, status="posted")
            logging.info(f"Post published successfully to LinkedIn: {post_id}")
        else:
            # Save to database as failed
            post_id = insert_post(post_content, status="failed")
            logging.error(f"Failed to publish post to LinkedIn: {result.get('error')}")
            
    except Exception as e:
        logging.error(f"Error in job: {str(e)}")

def start_scheduler():
    # LOCAL TESTING: Post every 2 minutes
    # TODO: Change back to CronTrigger for production
    from apscheduler.triggers.interval import IntervalTrigger
    
    scheduler.add_job(
        job, 
        IntervalTrigger(minutes=2),
        id='test_post',
        name='Test LinkedIn Post (every 2 min)'
    )
    
    # PRODUCTION SCHEDULE (commented out for testing):
    # scheduler.add_job(
    #     job, 
    #     CronTrigger(hour=9, minute=0, timezone=TIMEZONE),
    #     id='morning_post',
    #     name='Morning LinkedIn Post'
    # )
    # scheduler.add_job(
    #     job, 
    #     CronTrigger(hour=18, minute=0, timezone=TIMEZONE),
    #     id='evening_post',
    #     name='Evening LinkedIn Post'
    # )
    
    scheduler.start()
    logging.info("Scheduler started - LOCAL TEST MODE: Posts every 2 minutes")
