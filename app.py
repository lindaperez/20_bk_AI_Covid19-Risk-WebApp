# import necessary libraries
from datetime import date
from models import create_classes

import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

import pickle
import json
import gzip, pickle

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

from flask_sqlalchemy import SQLAlchemy
import datetime as dt
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','') or "sqlite:///db.sqlite"
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace('postgres://','postgresql://') or "sqlite:///db.sqlite"

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

result = create_classes(db)
Patient = result['Patient']

# create route that renders index.html template
@app.route("/")
def home():
    return redirect("/list", code=302)

def calculateAge(birthdate: date):
    today = date.today()
    age = today.year - birthdate.year - \
        ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age
def strDate(str:str):
    bd=dt.datetime.strptime(str, '%Y-%m-%d')
    return bd

def calculateAgeCategory(age: int):    
    if 0<=age<=16:
        return "Child"
    elif 17<=age<=32:
        return "Young Adult"
    elif 33<=age<=48:
        return "Middle Aged Adult"
    elif 49<=age<=64:
        return "Old Aged Adult"
    return "Senior Adult"
def calculateNumberCategory(age: int):    
    if 0<=age<=16:
        return 1
    elif 17<=age<=32:
        return 2
    elif 33<=age<=48:
        return 3
    elif 49<=age<=64:
        return 4
    return 5   
def genCovidcl(input : int):
    if (input == 1) :
        return "COVID-19 CONFIRMED BY EPIDEMIOLOGICAL CLINICAL ASSOCIATION"
    elif (input == 2):
        return "COVID-19 CONFIRMED BY JUDGMENT COMMITTEE"
    else:
        return "SARS-COV-2 CASE CONFIRMED"

# Query the database and register the jsonified results
@app.route("/register", methods=["GET", "POST"])
def register():
    params = {}
    if request.method == "POST":      
        if 'patientFirstName' in request.form.keys() and\
            request.form['patientFirstName'].strip()!='':
            params['first_name'] = request.form["patientFirstName"]
        if 'patientLastName' in request.form.keys() and\
            request.form['patientLastName'].strip()!='':
            params['last_name'] = request.form["patientLastName"]
        
        
        params['gender'] =  int(request.form["patientGender"])
       

        params['pneumonia'] =  int('patientPneumonia' in request.form.keys())
        params['age'] = strDate(request.form["patientAge"])
        params['pregnant'] = int('patientPregnant' in request.form.keys())
        params['diabetes'] = int('patientDiabetes' in request.form.keys())
        params['copd'] = int('patientCopd' in request.form.keys())

        params['asthma'] = int('patientAsthma' in request.form.keys())
        params['immunosup'] = int('patientImmunosup' in request.form.keys())
        params['hypertension'] = int('patientHypertension' in request.form.keys())
        params['another_complication'] = int('patientAnother' in request.form.keys())

        params['cardiovascular'] = int('patientCardiovascular' in request.form.keys())
        params['obesity'] = int('patientObesity' in request.form.keys())
        params['renal_chronic'] = int('patientRenalChronic' in request.form.keys())
        params['tobacco'] = int('patientTobacco' in request.form.keys())
        params['closed_contanct'] = int('patientClosedContact' in request.form.keys())
        if 'patientCovidcl' in request.form.keys() and request.form['patientCovidcl'].strip()!='':
          
            params['covidcl'] =  int(request.form["patientCovidcl"])

        #params['intubated'] = int("patientIntubated" in request.form.keys())
        #params['icu'] = int('patientICU' in request.form.keys())

        pat = Patient(**params)
        db.session.add(pat)
        db.session.commit()
        return redirect("/list", code=302)

    return render_template("form.html")

@app.route("/list", methods=["GET", "POST"])
def list():
    if request.method == "GET":
        patients = Patient.query.all()
        pats = {}
        for pat in patients:
            # print(pat.id,pat.first_name,pat.last_name,pat.gender,pat.age)
            # print(pat.pregnant,pat.diabetes,pat.copd,pat.asthma,pat.pneumonia)
            # print(pat.immunosup,pat.hypertension,pat.another_complication,pat.cardiovascular)
            # print(pat.obesity,pat.renal_chronic,pat.tobacco,pat.closed_contanct)
            # print(pat.covidcl)         
            pats[pat.id]={'ageValue':calculateAge( pat.age),
           'ageCategory':calculateAgeCategory(calculateAge( pat.age)),
              'covidcl': genCovidcl(pat.covidcl) }        
        return render_template("listPatients.html", patients=patients,pats=pats)

    return render_template("form.html")

@app.route("/view/<id>")
def view(id):
    if request.method == "GET":
        patients = Patient.query.all()
        pat = Patient.query.get(id)
        pats = {}
        pats['date'] =dt.datetime.now().strftime("%B %d, %Y")
        for patient in patients:        
            pats[patient.id]={'ageValue':calculateAge( patient.age),
           'ageCategory':calculateAgeCategory(calculateAge( patient.age)),           
            'covidcl': genCovidcl(patient.covidcl) }
            
 
        print('gender',pat.gender,'pneumonia',pat.pneumonia, 'pregnant',pat.pregnant,
        'diabetes',pat.diabetes,'copd',pat.copd,'asthma',pat.asthma,'immunosup',pat.immunosup,
        'hypertension',pat.hypertension,'cardiovascular',pat.cardiovascular,'obesity',pat.obesity,
        'renal_chronic',pat.renal_chronic,'tobacco',pat.tobacco,'closed_contanct',pat.closed_contanct)
        filename = "balanced_random_forest50.pkl"
        X_test = [[pat.gender,pat.pneumonia,pat.pregnant,pat.diabetes,pat.copd,pat.asthma,pat.immunosup,
            pat.hypertension,pat.cardiovascular,pat.obesity,pat.renal_chronic,pat.tobacco,pat.closed_contanct,
            pat.another_complication,calculateNumberCategory(calculateAge(pat.age))]]
        #print(X_test)
        with gzip.open(filename,'rb') as f:
            p  = pickle.Unpickler(f)
            brf_pkl = p.load()
            predicted = brf_pkl.predict(X_test)
        
        pats[pat.id]['predicted'] = predicted
        #print(predicted)
        return render_template("listPatients.html", patient=pat,patients=patients,pats=pats)

    return redirect("/list",patient=pat)


@app.route("/dashboard")
def dashboard():
    return render_template("gen_dashboard.html")


@app.route("/dropall")
def dropall():
    db.drop_all() 
    return render_template("gen_dashboard.html")

@app.route("/createall")
def createall():
    db.create_all()    
    return render_template("gen_dashboard.html")
