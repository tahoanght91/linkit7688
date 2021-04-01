from flask import Flask, request, render_template, redirect
from flask import url_for
import json

app = Flask(__name__,template_folder = 'template', static_url_path="/", static_folder="static")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index',methods = ['GET'])
def index():
    src_data_index = 'data/index.json'
    with open(src_data_index) as file:
        data_index = json.loads(file.read())
    return render_template('index.html', data_index = data_index)

@app.route('/setting', methods = ['GET'])
def setting():
    src_data_setting = 'data/setting.json'
    with open(src_data_setting) as file:
        data_setting = json.loads(file.read())
    return render_template("setting.html", data_setting = data_setting)

@app.route('/status', methods = ['GET'])
def status():
    src_data_status = 'data/status.json'
    with open(src_data_status) as file:
        data_status = json.loads(file.read())
    return render_template("status.html", data_status = data_status)

@app.route('/admin', methods = ['GET'])
def admin():
    src_data_admin = 'data/admin.json'
    with open(src_data_admin) as file:
        data_admin= json.loads(file.read())
    return render_template("admin.html", data_admin = data_admin)

@app.route('/check')
def check():
    return render_template("check.html")
