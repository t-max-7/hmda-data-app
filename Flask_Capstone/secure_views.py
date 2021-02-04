
"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import make_response, redirect, render_template, render_template_string, request, session, url_for
from Flask_Capstone import app

#!

import pandas as pd
import os
import pyargon2
from hmac import compare_digest as compare_hash
import pickle
from . import main_module
from . import ad_hoc
#!
# read pickle containing data
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
file_name = "2019_state_AZ_actions_taken_1_loan_types_1.pkl"
abs_path_to_data_pickle = os.path.join(PROJECT_ROOT, f"static/data/{file_name}").replace("\\", "/")
original_data_frame = pd.read_pickle(abs_path_to_data_pickle)
name_of_original_data_frame_variable = "original_data_frame"
table_info = ad_hoc.TableInfo(file_name, original_data_frame.columns.format())

#read pickle containing passwords
abs_path_to_password_dict_pickle = os.path.join(PROJECT_ROOT, "static/data/password_dict.pkl").replace("\\", "/")
with open(abs_path_to_password_dict_pickle, "rb") as password_dict_pickle:
    password_dict = pickle.load(password_dict_pickle)

#set up secret_key for session
app.secret_key = os.urandom(32)

@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return login_user()
    else:
        return make_secure_response(render_template(
            'login.html',
            title='Login',
            year=datetime.now().year,
            message=""
        ))

def login_user():
    username = request.form.get("username")

    user_password_info = password_dict.get(username)
    if (user_password_info is None):
        return make_secure_response(render_template(
            'login.html',
            title='Login',
            year=datetime.now().year,
            message="wrong username"
        ))
    
    salt = user_password_info["salt"]
    hash = user_password_info["hash"]

    password = request.form.get("password")
    
    if compare_hash(pyargon2.hash(password, salt), hash):
        session["username"] = username
        return make_secure_response(redirect(url_for("home")))
    else:
        return make_secure_response(render_template(
            'login.html',
            title='Login',
            year=datetime.now().year,
            message="wrong password"
        ))
    

@app.route('/home')
def home():
    """Renders the home page."""
    if "username" in session:
        return make_secure_response(render_template(
            'index.html',
            year=datetime.now().year,
        ))
    else:
        return make_secure_response(redirect(url_for("login")))

@app.route('/query', methods=["GET", "POST"])
def query():
    if "username" in session:
        if request.method == "POST":
            return make_secure_response(do_query())
        else:
            return make_secure_response(render_template(
                'query.html',
                title='Query',
                year=datetime.now().year,
                message='Your query page.',
                table_info=table_info
            ))
    else:
        return make_secure_response(redirect(url_for("login")))

def do_query():
    """Renders the contact page."""
    if "username" in session:
        query_type = request.form.get("sqlQueryType")
   
        if query_type == "SELECT":
            table_columns = request.form.getlist("tableColumns")
            #table_to_select_from = request.form.get("tableToSelectFrom")
            limit = int(request.form.get("limit"))        
            where_condition = ad_hoc.get_where_condition(request, name_of_original_data_frame_variable)
            sql_query =  ad_hoc.SqlSelectQuery(table_columns, where_condition, limit)
            try:
                result = ad_hoc.query_data_frame(sql_query, original_data_frame, abs_path_to_data_pickle)
                result = result.to_html(justify="center", classes="table")
            except SyntaxError as error:
                result = f"<h3> {str(error)} </h3>"
        elif query_type == "UPDATE":
            #table_to_update = request.form.get("tableToUpdate")
            table_columns = request.form.getlist("tableColumns")
            set_expression = request.form.get("setExpression")
            where_condition = ad_hoc.get_where_condition(request, name_of_original_data_frame_variable)
            sql_query = ad_hoc.SqlUpdateQuery(table_columns, set_expression, where_condition)
            try:
                result = ad_hoc.query_data_frame(sql_query, original_data_frame, abs_path_to_data_pickle).to_html(justify="center", classes="table")
                result = "<h3> update sucessful </h3>" + result
            except SyntaxError as error:
                result = f"<h3> {str(error)} </h3>"
       
        return make_secure_response(render_template_string(result))
    else:
        return make_secure_response(redirect(url_for("login")))

@app.route("/plot", methods=["POST"])
def make_plot():
    if "username" in session:
        x_axis = request.form.get("xAxis")
        y_axis = request.form.get("yAxis")

        table_columns = request.form.getlist("tableColumns")
        #table_to_select_from = request.form.get("tableToSelectFrom")
        where_condition = ad_hoc.get_where_condition(request, name_of_original_data_frame_variable)
        sql_query =  ad_hoc.SqlSelectQuery(table_columns, where_condition, None)
        try:
            df = ad_hoc.query_data_frame(sql_query, original_data_frame, abs_path_to_data_pickle)
            plot = main_module.make_plot(df, x_axis, y_axis)
        except SyntaxError as error:
            plot =  f"<h3> {str(error)} </h3>"
        return make_secure_response(render_template_string(plot))
        
    else:
        return make_secure_response(redirect(url_for("login")))

@app.route('/calculate', methods=["GET", "POST"])
def calculate():
    if "username" in session:
        if request.method == "POST":
            return do_calculate()
        else:
            options = [
                ad_hoc.CalculateOption("census_tract", "=", None, False),
                ad_hoc.CalculateOption("derived_dwelling_category", "=", "\"Single Family (1-4 Units):Site-Built\"", True),
                ad_hoc.CalculateOption("loan_purpose", "=", "1", True),
                ad_hoc.CalculateOption("loan_amount", "<", "1_000_000", True),
                ad_hoc.CalculateOption("income", "<", "100", True),
                ad_hoc.CalculateOption("debt_to_income_ratio", "<", "100", True),
                ad_hoc.CalculateOption("debt_to_income_ratio", ">", "0", True),
                ad_hoc.CalculateOption("property_value", "<", "1_000_000", True),
            ]
            return make_secure_response(render_template(
                "calculate.html",
                title='Calculate',
                year=datetime.now().year,
                message='Your calculate page.',
                options=options,
             ))
    else:
        return make_secure_response(redirect(url_for("login")))

def do_calculate():
        x_axis = "income"
        y_axis = "loan_amount"

        table_columns = []
        
        user_income = ad_hoc.parse_numerical_expression(request.form.get("userIncome"))

        table_column = request.form.get("tableColumns0")
        table_column_index = 0
        while table_column is not None:
            table_columns.append(table_column)
            table_column_index += 1
            table_column = request.form.get("tableColumns" + str(table_column_index))
        where_condition = ad_hoc.get_where_condition(request, name_of_original_data_frame_variable)
        sql_query =  ad_hoc.SqlSelectQuery(table_columns, where_condition, None)
        try:
            df = ad_hoc.query_data_frame(sql_query, original_data_frame, abs_path_to_data_pickle)
            plot = main_module.make_plot(df, x_axis, y_axis, user_income)
        except Exception as error:
            raise error
            plot =  f"<h3> {str(error)} </h3>"
        return make_secure_response(render_template_string(plot))

@app.route("/logout")
def logout():
    session.pop("username", None)
    return make_secure_response(redirect(url_for("login")))

def make_secure_response(template):
    response = make_response(template)
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response