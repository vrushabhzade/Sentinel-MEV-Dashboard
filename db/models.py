from sqlalchemy import Column, Integer, String, Float, DateTime
import datetime
from db.database import Base

class PoolReserve(Base):
    __tablename__ = "pool_reserves"

    id = Column(Integer, primary_key=True, index=True)
    pair_address = Column(String, unique=True, index=True)
    token0_address = Column(String)
    token1_address = Column(String)
    reserve0 = Column(String) # Stored as String because Wei amounts exceed DB Int limits
    reserve1 = Column(String)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

class TradeHistory(Base):
    __tablename__ = "trade_history"
    
    id = Column(Integer, primary_key=True, index=True)
    tx_hash = Column(String, unique=True, index=True)
    strategy = Column(String)
    profit_eth = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
