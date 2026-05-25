from sqlalchemy.orm import Session
from app import models

def get_trade_data(db: Session):
    return db.query(models.TradeData).all()

def get_top_countries(db: Session):
    return db.query(models.TopCountry).all()

def get_region_summary(db: Session):
    return db.query(models.RegionSummary).all()

def get_trade_trend(db: Session):
    return db.query(models.TradeTrend).all()
 