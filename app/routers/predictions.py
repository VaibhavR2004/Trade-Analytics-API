from fastapi import APIRouter
from pydantic import BaseModel
from app.routers.ml_service import predict_growth
from app.oauth2 import get_current_user
from fastapi import Depends

router = APIRouter(
    tags=["Prediction"]
)

class PredictionRequest(BaseModel):

    month: int


@router.post("/predict-growth")
def predict_trade_growth(
    request: PredictionRequest,
    current_user: dict = Depends(get_current_user)
):

    prediction = predict_growth(
        request.month
    )

    return {
        "predicted_trade_growth": prediction
    }