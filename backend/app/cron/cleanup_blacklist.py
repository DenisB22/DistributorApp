from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

from app.db.database import PostgresSessionLocal
from app.models import TokenBlacklist

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def delete_expired_tokens():
    """Deletes blacklisted tokens older than 24 hours."""
    db: Session = PostgresSessionLocal()
    expiration_time = datetime.utcnow() - timedelta(hours=24)
    
    deleted_tokens = db.query(TokenBlacklist).filter(TokenBlacklist.created_at < expiration_time).delete()
    db.commit()
    db.close()

    logger.info(f"Deleted {deleted_tokens} expired tokens from the blacklist.")

def start_cron():
    """Starts the cron job for cleaning up the blacklist table."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_expired_tokens, "interval", hours=24)
    scheduler.start()

    logger.info("Cron job for cleaning up blacklist started.")
