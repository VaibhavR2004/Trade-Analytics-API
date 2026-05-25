from app.database import SessionLocal
from app.services.analytics_service import (
    import_trade_data,
    import_top_countries,
    import_region_summary,
    import_trade_trend
)

db = SessionLocal()

print("Importing Trade Data...")
import_trade_data(db)

print("Importing Top Countries...")
import_top_countries(db)

print("Importing Region Summary...")
import_region_summary(db)

print("Importing Trade Trend...")
import_trade_trend(db)

print("All Data Imported Successfully")