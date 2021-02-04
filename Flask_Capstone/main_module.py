
import os.path

import base64
from io import BytesIO

import pandas as pd
from matplotlib.figure import Figure
from matplotlib import rcParams


import numpy as np

from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

import sklearn.cluster as cluster

def main(csv_data):
    loan_data = csv_data[["census_tract", "derived_dwelling_category", "purchaser_type", "loan_purpose", "business_or_commercial_purpose",
        "loan_amount", "loan_to_value_ratio", "interest_rate", "rate_spread", "total_loan_costs", "total_points_and_fees", "origination_charges", "discount_points",
        "lender_credits", "loan_term", "prepayment_penalty_term", "intro_rate_period", "property_value", "income", "debt_to_income_ratio", "applicant_age"]]

    # * 1
    loan_amount_vs_interest_rate = loan_data[
        (loan_data["census_tract"] == 4013010101) &
        (loan_data["derived_dwelling_category"] == "Single Family (1-4 Units):Site-Built") & 
        (loan_data["purchaser_type"] > -1_000) & 
        (loan_data["loan_purpose"] == 1) &
        (loan_data["business_or_commercial_purpose"] == 2) &
        (loan_data["loan_amount"] < 1_000_000) &
        (loan_data["loan_to_value_ratio"] > -1_000) &
        (loan_data["interest_rate"] > -1000) &
        (loan_data["income"] < 500) &
        (loan_data["debt_to_income_ratio"] > 30)]
    loan_amount_vs_interest_rate = loan_amount_vs_interest_rate[["loan_amount", "interest_rate"]].astype({"loan_amount": "int32"})
    
     # !!!!!!!!!!!!!!!!!!!!!!!!!!! REGRESSION
    XX = pd.DataFrame(loan_amount_vs_interest_rate["loan_amount"])
    YY = pd.DataFrame(loan_amount_vs_interest_rate["interest_rate"])

    # PLOTS SCATTER GRAPH UPON WHICH TO BASE REGRESSION
    fig = Figure()
    ax = fig.subplots()
    ax.scatter(XX, YY)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    yield f"<img src='data:image/png;base64,{data}'/>"

    model = Pipeline([('poly', PolynomialFeatures(degree=1)), ('linear', LinearRegression(fit_intercept=False))])
    scores = []
    kfold = KFold(n_splits=2, shuffle=True, random_state=42)
    for i, (train, test) in enumerate(kfold.split(XX, YY)):
        model.fit(XX.iloc[train,:], YY.iloc[train,:])
        score = model.score(XX.iloc[test,:], YY.iloc[test,:])
        scores.append(score)
    print(scores)

    YY_pred = model.predict(XX)

    ax.plot(XX, YY_pred, label="regression", color="red")
    ax.set_xlabel("loan_amount")
    ax.set_ylabel("interest_rate")
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!


    # * 2
    loan_amount_vs_income = loan_data[
        (loan_data["census_tract"] == 4013010101) &
        (loan_data["derived_dwelling_category"] == "Single Family (1-4 Units):Site-Built") & 
        (loan_data["purchaser_type"] > -1_000) & 
        (loan_data["loan_purpose"] == 1) &
        (loan_data["business_or_commercial_purpose"] == 2) &
        (loan_data["loan_amount"] < 1_000_000) &
        (loan_data["loan_to_value_ratio"] > -1_000) &
        (loan_data["interest_rate"] > -1000) &
        (loan_data["income"] < 500) &
        (loan_data["debt_to_income_ratio"] > 30)]
    loan_amount_vs_income = loan_amount_vs_income[["loan_amount", "income"]].astype({"loan_amount": "int32"})
    #loan_amount_vs_income.plot.scatter(x="loan_amount", y="income")

    # 3
    loan_amount_vs_loan_to_value_ratio =  loan_data[
        (loan_data["census_tract"] == 4013010101) &
        (loan_data["derived_dwelling_category"] == "Single Family (1-4 Units):Site-Built") & 
        (loan_data["purchaser_type"] > -1_000) & 
        (loan_data["loan_purpose"] == 1) &
        (loan_data["business_or_commercial_purpose"] == 2) &
        (loan_data["loan_amount"] < 1_000_000) &
        (loan_data["loan_to_value_ratio"] > -1_000) &
        (loan_data["interest_rate"] > -1000) &
        (loan_data["income"] < 500) &
        (loan_data["debt_to_income_ratio"] > 30)]
    loan_amount_vs_loan_to_value_ratio = loan_amount_vs_loan_to_value_ratio[["loan_amount", "loan_to_value_ratio"]].astype({"loan_amount": "int32"})
    #loan_amount_vs_loan_to_value_ratio.plot.scatter(x="loan_amount", y="loan_to_value_ratio")

    #4
    income_vs_loan_to_value_ratio =  loan_data[
        (loan_data["census_tract"] == 4013010101) &
        (loan_data["derived_dwelling_category"] == "Single Family (1-4 Units):Site-Built") & 
        (loan_data["purchaser_type"] > -1_000) & 
        (loan_data["loan_purpose"] == 1) &
        (loan_data["business_or_commercial_purpose"] == 2) &
        (loan_data["loan_amount"] < 1_000_000) &
        (loan_data["loan_to_value_ratio"] > -1_000) &
        (loan_data["interest_rate"] > -1000) &
        (loan_data["income"] < 500) &
        (loan_data["debt_to_income_ratio"] > 30)]
    income_vs_loan_to_value_ratio = income_vs_loan_to_value_ratio[["income", "loan_to_value_ratio"]]
    #income_vs_loan_to_value_ratio.plot.scatter(x="income", y="loan_to_value_ratio")

    #5
    income_vs_property_value = loan_data[
        (loan_data["census_tract"] == 4013010101) &
        (loan_data["derived_dwelling_category"] == "Single Family (1-4 Units):Site-Built") & 
        (loan_data["purchaser_type"] > -1_000) & 
        (loan_data["loan_purpose"] == 1) &
        (loan_data["business_or_commercial_purpose"] == 2) &
        (loan_data["loan_amount"] < 1_000_000) &
        (loan_data["loan_to_value_ratio"] > -1_000) &
        (loan_data["interest_rate"] > -1000) &
        (loan_data["income"] < 500) &
        (loan_data["debt_to_income_ratio"] > 30)]
    income_vs_property_value = income_vs_property_value[["income", "property_value", "debt_to_income_ratio"]]

    # !!!!!!!!!!!!!!!!!!!!!!!!!!! REGRESSION
    XX = pd.DataFrame(income_vs_property_value["income"])
    YY = pd.DataFrame(income_vs_property_value["property_value"])

    # PLOTS SCATTER GRAPH UPON WHICH TO BASE REGRESSION
   
    #regression
    model = Pipeline([('poly', PolynomialFeatures(degree=1)), ('linear', LinearRegression(fit_intercept=False))])
    scores = []
    kfold = KFold(n_splits=2, shuffle=True, random_state=42)
    for i, (train, test) in enumerate(kfold.split(XX, YY)):
        model.fit(XX.iloc[train,:], YY.iloc[train,:])
        score = model.score(XX.iloc[test,:], YY.iloc[test,:])
        scores.append(score)
    print(scores)

    YY_pred = model.predict(XX)
    #

    

    fig = Figure()
    ax = fig.subplots()
    
    #Kmeans
    cluster_y_pred = cluster.KMeans(n_clusters=2).fit_predict(XX, YY)
    ax.scatter(XX, YY, c=cluster_y_pred)
    #

    #regression
    ax.plot(XX, YY_pred, label="regression", color="red")
    
    ax.set_xlabel("income")
    ax.set_ylabel("property_value")

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    yield f"<img src='data:image/png;base64,{data}'/>"


def make_plot(data_frame, x_axis, y_axis, user_point_x=None):
    df = data_frame[[x_axis, y_axis]].dropna()
    XX = pd.DataFrame(df[x_axis])
    YY = pd.DataFrame(df[y_axis])

    # finds regression
    should_do_user_point = False
    try:
        model = Pipeline([('poly', PolynomialFeatures(degree=1)), ('linear', LinearRegression(fit_intercept=False))])
        scores = []
        kfold = KFold(n_splits=2, shuffle=True, random_state=42)
        for i, (train, test) in enumerate(kfold.split(XX, YY)):
            model.fit(XX.iloc[train,:], YY.iloc[train,:])
            score = model.score(XX.iloc[test,:], YY.iloc[test,:])
            scores.append(score)
        YY_pred = model.predict(XX)
        
        #user_point_x prediction
        if user_point_x is not None: 
            should_do_user_point = True
    # when there is less than 2 samples then can't do regression:
    except ValueError:
        YY_pred = YY
        
    
    # creates figure
    fig = Figure()
    ax = fig.subplots()
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)

    #Kmeans
    try:
        cluster_y_pred = cluster.KMeans(n_clusters=2).fit_predict(XX, YY)
        #plots data points colored according to assigned cluster
        ax.scatter(XX, YY, c=cluster_y_pred)
    #when there is less than 2 samples then can't do cluster:
    except ValueError:
        #plots data points
        ax.scatter(XX,YY)
    #

    #plot regression
    ax.plot(XX, YY_pred, label="regression", color="red")
    
    
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    if should_do_user_point:
        user_point_x = [[user_point_x]]
        user_point_y_pred = model.predict(user_point_x)
        return f"<img src='data:image/png;base64,{data}'/> <h2>recommended value is: {user_point_y_pred[0][0]}</h2>"
    else:
        return f"<img src='data:image/png;base64,{data}'/>"
        
