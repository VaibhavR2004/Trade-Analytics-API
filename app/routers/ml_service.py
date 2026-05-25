from sklearn.linear_model import LinearRegression
import pandas as pd

model = LinearRegression()

def train_model():

    df = pd.read_csv(
        "processed_data/trade_trend.csv"
    )

    X = df[["month"]]

    y = df["monthly_transit_cost"]

    model.fit(X, y)

    return model


trained_model = train_model()


def predict_growth(month: int):

    prediction = trained_model.predict(
        [[month]]
    )

    return float(prediction[0])