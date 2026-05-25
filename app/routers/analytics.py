from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends

from app.database import get_db
from app import models
from app.oauth2 import get_current_user

router = APIRouter(
    tags=["Analytics"]
)


@router.get("/top-countries")
def get_top_countries(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    countries = db.query(
        models.TopCountry
    ).all()

    return countries


@router.get("/regionsummary")
def get_region_summary(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    regions = db.query(
        models.RegionSummary
    ).all()

    return regions

@router.get("/tradetrends")
def get_trade_trends(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    trends = db.query(
        models.TradeTrend
    ).all()

    return trends