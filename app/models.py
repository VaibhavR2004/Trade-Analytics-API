from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class TradeData(Base):
    __tablename__ = "trade_data"
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String)
    region = Column(String)
    trade_value = Column(Float)
    year = Column(Integer)
    month = Column(Integer)


class TopCountry(Base):
    __tablename__ = "top_countries"
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String)
    total_trade = Column(Float)


class RegionSummary(Base):
    __tablename__ = "region_summary"
    id = Column(Integer, primary_key=True, index=True)
    region = Column(String)
    region_trade = Column(Float)


class TradeTrend(Base):
    __tablename__ = "trade_trend"
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer)
    month = Column(Integer)
    monthly_trade = Column(Float) 