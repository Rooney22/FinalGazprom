import numpy as np
from fastapi import Depends
from typing import BinaryIO
from datetime import datetime
from src.db.db import Session, get_session
from src.models.method import Method
from src.models.schemas.utils.method_enum import Methods_Enum
from sklearn.tree import DecisionTreeRegressor
import pickle
import csv
import pandas as pd
from io import StringIO


def encode_and_bind(original_dataframe, feature_to_encode):
    dummies = pd.get_dummies(original_dataframe[[feature_to_encode]])
    res = pd.concat([original_dataframe, dummies], axis=1)
    res = res.drop([feature_to_encode], axis=1)
    return res


class MethodsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def data_processing(self, user_id: int, input_file: BinaryIO):
        method = Method()
        method.method_name = Methods_Enum.dataProcessing
        method.used_at = datetime.now()
        method.user_id = user_id
        self.session.add(method)
        self.session.commit()
        df = pd.read_csv(input_file)
        for i in df.columns:
            if df.dtypes[i] == "float64":
                df[i] = df[i].fillna(df[i].mean())
            elif df.dtypes[i] == "int64":
                df[i] = df[i].fillna(df[i].median())
            else:
                df[i] = df[i].fillna(df[i].mode())
        df_onehot = df.copy()
        for i in ['WeekStatus', 'Day_of_week', 'Load_Type']:
            df_onehot = encode_and_bind(df_onehot, i)
        return df_onehot.to_csv(index=False)

    def fit(self, user_id: int, input_file: BinaryIO):
        method = Method()
        method.method_name = Methods_Enum.fit
        method.used_at = datetime.now()
        method.user_id = user_id
        self.session.add(method)
        self.session.commit()
        df = pd.read_csv(input_file)
        y_train = df["Usage_kWh"]
        X_train = df.drop(["Usage_kWh", "date"], axis=1)
        model = DecisionTreeRegressor().fit(X_train, y_train)
        with open('MLmodel/tree_classifier.pkl', 'wb') as fid:
            pickle.dump(model, fid)
        with open('MLmodel/train_data.csv', 'wb') as fid:
            pickle.dump(df.to_csv(), fid)

    def predict(self, user_id: int, input_file: BinaryIO):
        method = Method()
        method.method_name = Methods_Enum.predict
        method.used_at = datetime.now()
        method.user_id = user_id
        self.session.add(method)
        self.session.commit()
        df = pd.read_csv(input_file)
        X = df.drop(["Usage_kWh", "date"], axis=1)
        with open('MLmodel/tree_classifier.pkl', 'rb') as fid:
            model = pickle.load(fid)
            X["Usage_kWh"] = model.predict(X)
            return X.to_csv()

    def download(self, user_id: int):
        method = Method()
        method.method_name = Methods_Enum.download
        method.used_at = datetime.now()
        method.user_id = user_id
        self.session.add(method)
        self.session.commit()
        with open('MLmodel/train_data.csv', 'rb') as fid:
            train_data = pickle.load(fid)
            return train_data
