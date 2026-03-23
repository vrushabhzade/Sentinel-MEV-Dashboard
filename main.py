import argparse
import asyncio
from loguru import logger

from core.mempool.listener import MempoolListener
from config.settings import settings
from db.database import init_db

def start_bot():
    logger.info("Initializing MEV Trading Bot...")
    init_db()  # Create sqlite database tables
    if not settings.ETH_WSS_URL:
        logger.warning("ETH_WSS_URL is not set. Mempool listening will not work.")
    
    listener = MempoolListener()
    try:
        listener.start()
    except KeyboardInterrupt:
        logger.info("Shutting down the MEV Bot...")

def start_dashboard():
    import os
    logger.info("Starting Streamlit Dashboard...")
    os.system("streamlit run dashboard/app.py")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MEV Trading Bot")
    parser.add_argument("--mode", choices=["bot", "dashboard", "api"], default="bot", help="Run mode")
    
    args = parser.parse_args()
    
    if args.mode == "bot":
        start_bot()
    elif args.mode == "dashboard":
        start_dashboard()
    elif args.mode == "api":
        import os
        os.system("uvicorn api.main:app --host 0.0.0.0 --port 8000")
