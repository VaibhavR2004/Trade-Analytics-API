import pandas as pd
from sqlalchemy.orm import Session
from app import models


def _scalar_value(value, cast_type):
    if value is None:
        return None
    if isinstance(value, (int, float, str)):
        return cast_type(value)
    return cast_type(value.item()) if hasattr(value, "item") else cast_type(value)


def import_trade_data(db: Session):
    trade_df = pd.read_csv("processed_data/cleaned_trade_data.csv")
    for _, row in trade_df.iterrows():
        trade = models.TradeData(
            country=str(row.get("flag", row.get("country"))),
            region=str(row.get("continent", row.get("region"))),
            trade_value=_scalar_value(row.get("total_transit_cost_usd", row.get("total_transit_cost")), float),
            year=_scalar_value(row["year"], int),
            month=_scalar_value(row["month"], int)
        )
        db.add(trade)
    db.commit()


def import_top_countries(db: Session):
    df = pd.read_csv("processed_data/top_flags.csv")
    for _, row in df.iterrows():
        country = models.TopCountry(
            country=str(row.get("flag", row.get("country"))),
            total_trade=_scalar_value(row.get("total_transit_cost", row.get("total_trade")), float)
        )
        db.add(country)
    db.commit()


def import_region_summary(db: Session):
    df = pd.read_csv("processed_data/continent_summary.csv")
    for _, row in df.iterrows():
        region = models.RegionSummary(
            region=str(row.get("continent", row.get("region"))),
            region_trade=_scalar_value(row.get("continent_trade", row.get("region_trade")), float)
        )
        db.add(region)
    db.commit()


def import_trade_trend(db: Session):
    df = pd.read_csv("processed_data/trade_trend.csv")
    for _, row in df.iterrows():
        trend = models.TradeTrend(
            year=_scalar_value(row["year"], int),
            month=_scalar_value(row["month"], int),
            monthly_trade=_scalar_value(row.get("monthly_transit_cost", row.get("monthly_trade")), float)
        )
        db.add(trend)
    db.commit()