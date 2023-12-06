from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List
import pandas as pd
import pickle

app = FastAPI()


class Item(BaseModel):
    name: str
    year: int
    km_driven: int
    fuel: str
    seller_type: str
    transmission: str
    owner: str
    mileage: str
    engine: str
    max_power: str
    torque: str
    seats: float


class Items(BaseModel):
    objects: List[Item]

def data_prepare(df_test):
    df_test['mileage'] = df_test['mileage'].str.extract('(\d+\.\d+|\d+)').astype(float)
    df_test['engine'] = df_test['engine'].str.extract('(\d+)').astype(float)
    df_test['max_power'] = df_test['max_power'].str.extract('(\d+\.\d+|\d+)').astype(float)
    df_test['engine'] = df_test['engine'].astype('Int64')
    df_test['seats'] = df_test['seats'].astype('Int64')
    df_test.drop(columns=['torque'], inplace=True, axis=1)
    df_test['km_driven_engine_ratio'] = df_test['km_driven'] / df_test['engine']
    df_test['km_driven_max_power_ratio'] = df_test['km_driven'] / df_test['max_power']
    df_test['engine_max_power_ratio'] = df_test['engine'] / df_test['max_power']
    numeric_features = ['year', 'km_driven', 'mileage', 'engine', 'max_power']

    for i in numeric_features:
        for j in numeric_features:
            df_test[f'{i}_mul_{j}'] = df_test[i] * df_test[j]
            df_test[f'{i}_mul_{j}'] = df_test[i] * df_test[j]
    df_test['brand'] = df_test['name'].str.split().str[0]
    df_test = df_test.drop(['name'], axis=1)

    with open('columns.pkl', 'rb') as file:
        pickle_columns = pickle.load(file)

    df_test = pd.get_dummies(df_test, columns=['fuel', 'seller_type', 'owner', 'transmission', 'seats', 'brand'])

    miss_feat = set(pickle_columns) - set(df_test.columns.tolist())
    for i in miss_feat:
        df_test[i] = False

    del_feat = list(set(df_test.columns.tolist()) - set(pickle_columns))
    df_test.drop(columns=del_feat, inplace=True, axis=1)
    return df_test[pickle_columns]

def predict_car_price(df_test: pd.DataFrame) -> float:
    df_test_new = data_prepare(df_test)
    with open('model.pkl', 'rb') as file:
        pickle_model = pickle.load(file)
    with open('scaler.pkl', 'rb') as file:
        pickle_scaler = pickle.load(file)
    sc_df_test = pickle_scaler.transform(df_test_new)
    prediction = pickle_model.predict(sc_df_test)
    return prediction[0]

@app.post("/predict_price/")
async def predict_price(item: Item):
    try:
        df_data = [item.dict()]
        df = pd.DataFrame(df_data)
        predicted_price = predict_car_price(df)
        return {"predicted_price": predicted_price}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def predict_car_prices(df_test: pd.DataFrame) -> pd.DataFrame:
    df_test_old = df_test.copy()
    df_test_new = data_prepare(df_test)
    with open('model.pkl', 'rb') as file:
        pickle_model = pickle.load(file)
    with open('scaler.pkl', 'rb') as file:
        pickle_scaler = pickle.load(file)
    sc_df_test = pickle_scaler.transform(df_test_new)
    df_test_old['prediction'] = pickle_model.predict(sc_df_test)
    return df_test_old

@app.post("/predict_prices/")
async def predict_prices(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        predicted_df = predict_car_prices(df)

        response_csv = predicted_df.to_csv(index=False)
        return response_csv
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))