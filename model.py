import numpy as np
import pandas as pd

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import recall_score, accuracy_score, precision_score

import pickle

#turning off SettingWithCopyWarning: A value is trying to be set on a copy of a slice from a DataFrame
pd.options.mode.chained_assignment = None 

#open data from given path
def open_data(path):

    df = pd.read_csv(path)

    return df

#preprocessing numeric (int, float) data
def preprocessing_numeric_data(df: pd.DataFrame):

    df['Age'] = np.where(df['Age'] > 80, np.NaN, df['Age'])
    df['Age'] = np.where(df['Age'] == 0, np.NaN, df['Age'])

    df['Flight Distance'] = np.where(df['Flight Distance'] > 4000, np.NaN, df['Flight Distance'])
    df['Flight Distance'] = np.where(df['Flight Distance'] == 0, np.NaN, df['Flight Distance'])

    departure_99 = np.nanpercentile(df['Departure Delay in Minutes'], 99)
    df['Departure Delay in Minutes'] = np.where(df['Departure Delay in Minutes'] > departure_99, np.NaN, df['Departure Delay in Minutes'])

    arrival_99 = np.nanpercentile(df['Arrival Delay in Minutes'], 99)
    df['Arrival Delay in Minutes'] = np.where(df['Arrival Delay in Minutes'] > arrival_99, np.NaN, df['Arrival Delay in Minutes'])
    

    return df

#preprocessing estimated (from 0 to 5) data
def preprocessing_estimated_data(df: pd.DataFrame):

    cathegorial = list(df.select_dtypes(include=['float64']))[4:]
    for col in cathegorial:
        df[col] = np.where(df[col] > 5, np.NaN, df[col])

    return df

#preprocessing categorical (male-female) data
def preprocessing_categorical_data(df: pd.DataFrame):

    df = df[df['satisfaction'] != '-']

    return df

#preprocessing data which is NaN
def processing_missing_data(df: pd.DataFrame):

    nulls = pd.DataFrame(df.isna().sum(), columns=['NaN count'])
    has_nulls = nulls[nulls['NaN count'] > 0].index
    for col in has_nulls:
        if df[col].dtype == 'int64' or df[col].dtype == 'float64':
            df[col].fillna(df[col].mean(), inplace=True)
    
    object_cols = list(df.select_dtypes(include=['object']))
    df.dropna(subset = object_cols, inplace=True)

    
    return df

#encode categorial data and scale all data for fitting the model
def encoding_and_scaling(df: pd.DataFrame, app=False):

    df['Gender'] = df['Gender'].map({'Male' : 1, 'Female' : 0})
    df['Customer Type'] = df['Customer Type'].map({'Loyal Customer' : 1, 'disloyal Customer' : 0})
    df['Type of Travel'] = df['Type of Travel'].map({'Business travel' : 1, 'Personal Travel' : 0})
    
    if not app:
        df['satisfaction'] = df['satisfaction'].map({'satisfied' : 1, 'neutral or dissatisfied' : 0})

        categorical = ['Class']
        numeric_features = [col for col in df.columns if col not in categorical]

        column_transformer = ColumnTransformer([
            ('ohe', OneHotEncoder(drop='first', handle_unknown="ignore"), categorical),
            ('scaling', MinMaxScaler(), numeric_features)
            ])
        
        df= column_transformer.fit_transform(df)

        lst = list(column_transformer.transformers_[0][1].get_feature_names_out())
        lst.extend(numeric_features)

        df = pd.DataFrame(df, columns=lst)

    else:
        numeric_features = [col for col in df.columns]
        column_transformer = ColumnTransformer([('scaling', MinMaxScaler(), numeric_features)])

        df= column_transformer.fit_transform(df)

        df = pd.DataFrame(df, columns=numeric_features)

    return df


#split data to train and test
def split_data(df: pd.DataFrame, test=False):

    X = df.drop(['id', 'satisfaction'], axis=1)
    y = df['satisfaction'] #target

    if test:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        return X_train, X_test, y_train, y_test
    else:
        return X, y

#prepare data for training
def prepare_data(df: pd.DataFrame, test=False):

    df = preprocessing_numeric_data(df)
    df = preprocessing_estimated_data(df)
    df = preprocessing_categorical_data(df)
    df = processing_missing_data(df)
    df = encoding_and_scaling(df)

    if test:
        X_train, X_test, y_train, y_test = split_data(df)
        return X_train, X_test, y_train, y_test
    else:
        X_train, y_train = split_data(df)
        return X_train, y_train

#fits logistic regression model
def fit_and_save(df: pd.DataFrame, path="data/model.pickle", test=False):

    if test:
        X_train, X_test, y_train, y_test = prepare_data(df)
    else:
        X_train, y_train = prepare_data(df)

    model = LogisticRegression(max_iter=500, random_state=42)
    model.fit(X_train, y_train)

    if test:
        preds = model.predict(X_test)
        print(f'Accuracy: {round(accuracy_score(y_test, preds), 3)}')
        print(f'Precision: {round(precision_score(y_test, preds), 3)}')
        print(f'Recall: {round(recall_score(y_test, preds), 3)}')

    with open(path, 'wb') as f:
        pickle.dump(model, f)
        print(f"Model was saved to {path}")
        


#load preload model
def load_model(path="data/model.pickle"):
    with open(path, 'rb') as f:
        model = pickle.load(f)
    return model


#make prediction on input
def predict_on_input(df: pd.DataFrame):

    model=load_model()

    prediction = model.predict(df)[0]

    prediction_proba = model.predict_proba(df)[0]

    encode_prediction_proba = {
        0: "Пассажиру не понравилось с вероятностью",
        1: "Пассажиру понравилось с вероятностью"
    }

    encode_prediction = {
        0: "К сожалению, пассажир недоволен",
        1: "Ура! Пассажир доволен!"
    }

    prediction_data = {}
    for key, value in encode_prediction_proba.items():
        prediction_data.update({value: prediction_proba[key]})

    prediction_df = pd.DataFrame(prediction_data, index=[0])
    prediction = encode_prediction[prediction]

    return prediction, prediction_df

if __name__ == "__main__":

    df = open_data(path = "data/clients.csv")

    fit_and_save(df)
