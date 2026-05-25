from pydantic import BaseModel

class TradeBase(BaseModel):
    country: str
    region: str
    trade_value: float
    year: int
    month: int


class TradeResponse(TradeBase):
    id: int
    class Config:
        orm_mode = True


class CountryResponse(BaseModel):
    country: str
    total_trade: float
    class Config:
        orm_mode = True


class RegionResponse(BaseModel):
    region: str
    region_trade: float
    class Config:
        orm_mode = True


class TrendResponse(BaseModel):
    year: int
    month: int
    monthly_trade: float

    class Config:
        orm_mode = True 