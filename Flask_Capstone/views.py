"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import redirect, render_template, render_template_string, request, session, url_for
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
abs_path_to_data_pickle = os.path.join(PROJECT_ROOT, "static/data/csv_data - Copy.pkl").replace("\\", "/")
original_data_frame = pd.read_pickle(abs_path_to_data_pickle)
name_of_original_data_frame_variable = "original_data_frame"
table_info = ad_hoc.TableInfo("2019_state_AZ_actions_taken_1_loan_types_1.csv", original_data_frame.columns.format())

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
        return render_template(
            'login.html',
            title='Login',
            year=datetime.now().year,
            message=""
        )

def login_user():
    username = request.form.get("username")

    user_password_info = password_dict.get(username)
    if (user_password_info is None):
        return render_template(
            'login.html',
            title='Login',
            year=datetime.now().year,
            message="wrong username"
        )
    
    salt = user_password_info["salt"]
    hash = user_password_info["hash"]

    password = request.form.get("password")
    
    if compare_hash(pyargon2.hash(password, salt), hash):
        session["username"] = username
        return redirect(url_for("home"))
    else:
        return render_template(
            'login.html',
            title='Login',
            year=datetime.now().year,
            message="wrong password"
        )
    

@app.route('/home')
def home():
    """Renders the home page."""
    if "username" in session:
        return render_template(
            'index.html',
            year=datetime.now().year,
        )
    else:
        return redirect(url_for("login"))

@app.route('/query', methods=["GET", "POST"])
def query():
    if "username" in session:
        if request.method == "POST":
            return do_query()
        else:
            return render_template(
                'query.html',
                title='Query',
                year=datetime.now().year,
                message='Your query page.',
                table_info=table_info
            )
    else:
        return redirect(url_for("login"))

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
            result = ad_hoc.query_data_frame(sql_query, original_data_frame, abs_path_to_data_pickle).to_html(justify="center", classes="table")
    
        elif query_type == "UPDATE":
            #table_to_update = request.form.get("tableToUpdate")
            table_columns = request.form.getlist("tableColumns")
            set_expression = request.form.get("setExpression")
            where_condition = ad_hoc.get_where_condition(request, name_of_original_data_frame_variable)
            sql_query = ad_hoc.SqlUpdateQuery(table_columns, set_expression, where_condition)
            result = "<h3> update sucessful </h3>" + ad_hoc.query_data_frame(sql_query, original_data_frame, abs_path_to_data_pickle).to_html(justify="center", classes="table")

        return render_template_string(result)
    else:
        return redirect(url_for("login"))

@app.route("/plot", methods=["POST"])
def make_plot():
    if "username" in session:
        x_axis = request.form.get("xAxis")
        y_axis = request.form.get("yAxis")

        table_columns = request.form.getlist("tableColumns")
        #table_to_select_from = request.form.get("tableToSelectFrom")
        where_condition = ad_hoc.get_where_condition(request, name_of_original_data_frame_variable)
        sql_query =  ad_hoc.SqlSelectQuery(table_columns, where_condition, None)
        df = ad_hoc.query_data_frame(sql_query, original_data_frame, abs_path_to_data_pickle)
        plot = main_module.make_plot(df, x_axis, y_axis)
    
        return plot
    else:
        return dedirect(url_for("login"))


@app.route('/plots')
def plots():
    if "username" in session:
        plots = ""
        for p in main_module.main(original_data_frame):
            plots = plots + p
        return render_template(
            'plots.html',
            title='Plots',
            year=datetime.now().year,
            message='Description',
            plots=plots
        )
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))