import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db.database import get_db, init_db
from db.models import TradeHistory, PoolReserve

logger = logging.getLogger(__name__)

app = FastAPI(title="MEV Trading Bot API", version="1.0.0")

@app.on_event("startup")
def on_startup():
    init_db()
    logger.info("FastAPI Server Started")

@app.get("/")
def read_root():
    return {"status": "MEV Bot API is running", "components": ["mempool", "sandwich_strategy", "ml_inference"]}

@app.get("/trades/recent")
def get_recent_trades(limit: int = 10, db: Session = Depends(get_db)):
    """
    Fetch the most recent MEV trades executed by the bot.
    """
    trades = db.query(TradeHistory).order_by(TradeHistory.timestamp.desc()).limit(limit).all()
    return {"success": True, "trades": trades}

@app.get("/pools/reserves/{pair_address}")
def get_pool_reserve(pair_address: str, db: Session = Depends(get_db)):
    """
    Fetch synchronized Uniswap pool reserves from the local database.
    This eliminates the need to query the blockchain continuously.
    """
    pool = db.query(PoolReserve).filter(PoolReserve.pair_address == pair_address.lower()).first()
    if not pool:
        raise HTTPException(status_code=404, detail="Pool not found locally")
    
    return {
        "pair": pool.pair_address,
        "token0": pool.token0_address,
        "token1": pool.token1_address,
        "reserve0": pool.reserve0,
        "reserve1": pool.reserve1,
        "last_updated": pool.last_updated
    }
