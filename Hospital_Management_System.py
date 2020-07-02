# -*- coding: utf-8 -*-
from flask import Flask,redirect,url_for, render_template, request,send_file,session,flash,g
from flask_sqlalchemy import SQLAlchemy

import webbrowser
from datetime import datetime

import json
#import db_handler



app = Flask(__name__)
app.secret_key = "0d8fb9370a5bf7b892be4865cdf8b658a82209624e33ed71cae353b0df254a75db63d1baa35ad99f26f1b399c31f3c666a7fc67ecef3bdcdb7d60e8ada90b722"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column('id',db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    password =  db.Column(db.String(100))
    def __init__(self,name,passwrd):
        self.name = name
        self.password = passwrd
        
class master_diagnosis(db.Model):
    ws_diagn_id =db.Column(db.Integer, db.Sequence("ws_diagn_id"),primary_key=True)
    ws_diagn_name = db.Column(db.String(100))
    ws_diagn_rt = db.Column(db.String(100))
    def __init__(self,name,rate):
        self.ws_diagn_name = name
        self.ws_diagn_rt = rate

class master_medicine(db.Model):
    ws_med_id = db.Column(db.Integer,primary_key=True)
    ws_med_name = db.Column(db.String(100))
    ws_med_qty = db.Column(db.Integer)
    ws_med_rt = db.Column(db.Integer)
    def __init__(self,name,qty,rate):
        self.ws_med_name = name
        self.ws_med_qty = qty
        self.ws_med_rt = rate
        
class patient(db.Model):
    ws_pat_id = db.Column(db.Integer,primary_key=True)
    ws_ssn = db.Column(db.Integer)
    ws_pat_name = db.Column(db.String(100))
    ws_adrs = db.Column(db.String(100))
    ws_age = db.Column(db.Integer)
    ws_doj = db.Column(db.String(100))
    ws_rtype = db.Column(db.String(100))
    ws_state = db.Column(db.String(100))
    ws_city = db.Column(db.String(100))
    ws_status = db.Column(db.String(100))
    def __init__(self,ssn,name,adrs,age,doj,rtype,state,city,status):
        self.ws_ssn = int(ssn)
        self.ws_pat_name = name
        self.ws_adrs = adrs
        self.ws_age = int(age)
        self.ws_doj = doj
        self.ws_rtype = rtype
        self.ws_state = state
        self.ws_city = city
        self.ws_status = status
        
class medicines(db.Model):
    ws_id = db.Column(db.Integer,primary_key=True)
    ws_pat_id = db.Column(db.Integer)
    ws_med_name = db.Column(db.String(100))
    ws_qty = db.Column(db.Integer) 
    def __init__(self,pid,name,qty):
        self.ws_pat_id = pid
        self.ws_med_name = name
        self.ws_qty = qty

class daigonistics(db.Model):
    ws_id = db.Column(db.Integer,primary_key=True)
    ws_pat_id =db.Column(db.Integer)
    ws_diagn = db.Column(db.String(100))
    def __init__(self,ssn,name):
        self.ws_pat_id = ssn
        self.ws_diagn = name

class daigonistics_temp(db.Model):
    ws_id = db.Column(db.Integer,primary_key=True)
    ws_pat_id =db.Column(db.Integer)
    ws_diagn = db.Column(db.String(100))
    def __init__(self,ssn,name):
        self.ws_pat_id = ssn
        self.ws_diagn = name

class medicines_temp(db.Model):
    ws_id = db.Column(db.Integer,primary_key=True)
    ws_pat_id = db.Column(db.Integer)
    ws_med_name = db.Column(db.String(100))
    ws_qty = db.Column(db.Integer) 
    def __init__(self,pid,name,qty):
        self.ws_pat_id = pid
        self.ws_med_name = name
        self.ws_qty = qty
        



@app.route("/",methods=["POST","GET"])
@app.route("/login",methods=["POST","GET"])
def login():
    if 'user' in session:
        if session['user'] != None:
            return redirect(url_for('home'))
    if request.method == "POST":
        uname = request.form["uname"]
        password = request.form["password"]
        found_user = users.query.filter_by(name = uname,password = password).first()
        if found_user:
            session['user'] = uname
            flash("Logged in successfully",category='success')    
            return redirect(url_for('home'))
        else:
            flash("Invalid Email and password",category='error')
            return render_template('login.html')
    else:
        return render_template("login.html")


@app.route('/home')
def home():
    if 'user' in session:
        return render_template('home.html', user=session['user'])
    return redirect(url_for('login'))

@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']
    

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("logged out Successfully", category='success')
    return redirect(url_for('login'))

    
@app.route("/createPatient",methods=["POST","GET"])
def createPatient():
    #if 'user' in session:
    if request.method == 'POST':
        ssn = request.form['ssn']
        name = request.form['uname']
        age = request.form['age']
        doj = request.form['doj']
        rtype = request.form['rtype']
        adrs = request.form['adrs']
        city = request.form['city']
        state = request.form['state']
        status = "Active"
        print(" asdsssssssss")
        new_patient = patient(ssn, name, adrs, age, doj, rtype, state, city, status)
        db.session.add(new_patient)
        db.session.commit()
        flash("Successfully Added the Patient",category='success')
        return render_template('createPatient.html')
    else:
        
        return render_template('createPatient.html')
    #return redirect(url_for('login')) 

@app.route("/updatePatient",methods=["POST","GET"])
def updatePatient():
    #if 'user' in session:
    if request.method == 'POST':
        ssn = (int)(request.form['ssn'])
        name = request.form['uname']
        age = (int)(request.form['age'])
        doj = request.form['doj']
        rtype = request.form['rtype']
        adrs = request.form['adrs']
        city = request.form['city']
        state = request.form['state']
        find_patient = patient.query.filter_by(ws_ssn = ssn).first()
        find_patient.ws_ssn = ssn
        find_patient.ws_pat_name = name
        find_patient.ws_adrs = adrs
        find_patient.ws_age = age
        find_patient.ws_doj = doj
        find_patient.ws_rtype = rtype
        find_patient.ws_state = state
        find_patient.ws_city = city            
        db.session.add(find_patient)
        db.session.commit()
        flash("Successfully Updated the Patient",category='success')
        return render_template('updatePatient.html',values=None)
    else:
        try:
            ssn = (request.args.get("ssn"))
            values = patient.query.filter_by(ws_ssn = ssn).first()
            return render_template('updatePatient.html',values=values)
        except:
            return render_template('updatePatient.html',values = "")

@app.route("/deletePatient",methods=["POST","GET"])
def deletePatient():
    #if 'user' in session:
    if request.method == 'POST':
        ssn = int(request.form['ssn'])
        patient.query.filter_by(ws_ssn = ssn).delete()
        db.session.commit()
        flash("Successfully Deleted the Patient",category='success')
        return render_template('deletePatient.html',values=None)
    else:
        try:
            ssn = (request.args.get("ssn"))
            values = patient.query.filter_by(ws_ssn = ssn).first()
            if values == None:
                flash("Patient Not found",category='error')
            return render_template('deletePatient.html',values=values)
        except: 
            return render_template('deletePatient.html',values = "")
        
@app.route("/searchPatient",methods=["POST","GET"])
def searchPatient():
    #if 'user' in session:
    if request.method == 'POST':
        ssn = int(request.form['ssn'])
        values = patient.query.filter_by(ws_ssn = ssn).first()
        if values == None:
            flash("No Patient found",category='error')
        return render_template('searchPatient.html',values=values)
    else:
        try:
            ssn = (request.args.get("ssn"))
            values = patient.query.filter_by(ws_ssn = ssn).all()
            if values == None:
                flash("No Patient found",category='error')
            return render_template('searchPatient.html',values=values)
        except: 
            return render_template('searchPatient.html',values = "")

@app.route('/viewPatient',methods=["GET"])
def viewPatient():
    return render_template('viewPatient.html', patients = patient.query.filter_by().all())


@app.route("/addDiagostics",methods=["POST","GET"])
def addDiagostics():
    #if 'user' in session:
    if request.method == 'POST':
        ssn = int(request.form['ssn'])
        values = patient.query.filter_by(ws_ssn = ssn).first()
        
        daigonis_temp = daigonistics_temp.query.filter_by(ws_pat_id = ssn).all()
        prices = master_diagnosis.query.filter_by().all()
        for temp in daigonis_temp:
            new_dai = daigonistics(temp.ws_pat_id, temp.ws_diagn)
            db.session.add(new_dai)
        
        for temp in daigonis_temp:
            daigonistics_temp.query.filter_by(ws_pat_id = ssn).delete()
        
        #daigonis_temp.delete()
        #daigonistics_temp.__table__.drop()
        db.session.commit()
        if values == None:
            flash("No Patient found",category='error')
        daigonis = daigonistics.query.filter_by(ws_pat_id = ssn).all()
        return render_template('addDiagnostics.html',values=values,daigonis=daigonis,prices=prices)
    else:
        try:
            ssn = (request.args.get("ssn"))
            values = patient.query.filter_by(ws_ssn = ssn).first()
            daigonis = daigonistics.query.filter_by(ws_pat_id = ssn).all()
            daigonis_temp = daigonistics_temp.query.filter_by(ws_pat_id = ssn).all()
            prices = master_diagnosis.query.filter_by().all()
            return render_template('addDiagnostics.html',values=values,daigonis=daigonis,daigonis_temp=daigonis_temp,prices=prices)
        except: 
            return render_template('addDiagnostics.html',values = "")
    #return redirect(url_for('login')) 

@app.route("/issueMedicine",methods=["POST","GET"])
def issueMedicine():
    #if 'user' in session:
    if request.method == 'POST':
        ssn = int(request.form['ssn'])
        values = patient.query.filter_by(ws_ssn = ssn).first()
        medicine_temp = medicines_temp.query.filter_by(ws_pat_id = ssn).all()
        prices = master_medicine.query.filter_by().all()
        for temp in medicine_temp:
            new_med = medicines(temp.ws_pat_id, temp.ws_med_name,temp.ws_qty)
            db.session.add(new_med)
        
        for temp in medicine_temp:
            medicines_temp.query.filter_by(ws_pat_id = ssn).delete()
        
        #daigonis_temp.delete()
        #daigonistics_temp.__table__.drop()
        db.session.commit()
        if values == None:
            flash("No Patient found",category='error')
        daigonis = daigonistics.query.filter_by(ws_pat_id = ssn).all()
        return render_template('issueMedicines.html',values=values,daigonis=daigonis,prices=prices)
    else:
        try:
            ssn = (request.args.get("ssn"))
            values = patient.query.filter_by(ws_ssn = ssn).first()
            medicine = medicines.query.filter_by(ws_pat_id = ssn).all()
            medicine_temp = medicines_temp.query.filter_by(ws_pat_id = ssn).all()
            prices = master_medicine.query.filter_by().all()
            return render_template('issueMedicines.html',values=values,medicine=medicine,medicine_temp=medicine_temp,prices=prices)
        except: 
            return render_template('issueMedicines.html',values = "")
    #return redirect(url_for('login')) 

@app.route("/addNewDiagostics",methods=["POST","GET"])
def addNewDiagostics():
    if request.method == 'POST':
        ssn = int(request.form['ssn'])
        diagn = request.form['daign']
        print(diagn)
        new_daignosis = daigonistics_temp(ssn,diagn)
        db.session.add(new_daignosis)
        db.session.commit()
        return redirect(url_for('addDiagostics'))
    else:
        ssn = (request.args.get("ssn"))
        daigonsis_list = master_diagnosis.query.filter_by().all()
        return render_template('addNewDiagostics.html',ssn=ssn,daigonsis_list=daigonsis_list)

@app.route("/issueNewMedicine",methods=["POST","GET"])
def issueNewMedicine():
    if request.method == 'POST':
        ssn = int(request.form['ssn'])
        med_name = request.form['med_name']
        med_qty = request.form['med_qty']
        prices = master_medicine.query.filter_by(ws_med_name=med_name).first()
        if prices.ws_med_qty <= int(med_qty):
            flash("Not enough Medicines",category='error')
            medicines_list = master_medicine.query.filter_by().all()
            return render_template('issueNewMedicines.html',ssn=ssn,medicines_list=medicines_list)
        new_medicine = medicines_temp(ssn,med_name,med_qty)
        db.session.add(new_medicine)
        db.session.commit()
        return redirect(url_for('issueMedicine'))
    else:
        ssn = (request.args.get("ssn"))
        medicines_list = master_medicine.query.filter_by().all()
        return render_template('issueNewMedicines.html',ssn=ssn,medicines_list=medicines_list)
    
@app.route('/finalBilling',methods=["POST","GET"])
def finalBilling():
    if request.method == 'POST':
        return f"Thank You"
    else :
        ssn = (request.args.get("ssn"))
        values = patient.query.filter_by(ws_ssn = ssn).first()
        medicine = medicines.query.filter_by(ws_pat_id = ssn).all()
        daigonis = daigonistics.query.filter_by(ws_pat_id = ssn).all()
        medicine_prices = master_medicine.query.filter_by().all()
        daigonis_prices = master_diagnosis.query.filter_by().all()
        return render_template('finalBilling.html',
                               values=values,
                               medicine=medicine,
                               daigonis=daigonis,
                               medicine_prices=medicine_prices,
                               daigonis_prices=daigonis_prices)
    return f"Worked"
    





@app.route("/view")
def view():
    return render_template("view.html", values = users.query.all())



@app.route('/addDaignois')
def addDaignois():
    new_daignosis = master_diagnosis('CBP','2000')
    db.session.add(new_daignosis)
    new_daignosis = master_diagnosis('Lipid','1500')
    db.session.add(new_daignosis)
    new_daignosis = master_diagnosis('ECG','3000')
    db.session.add(new_daignosis)
    new_daignosis = master_diagnosis('Echo','4000')
    db.session.add(new_daignosis)
    db.session.commit()
    return f"Successfully created a new Daignosis"

@app.route('/addPatientDaignois')
def addPatientDaignois():
    new_daignosis = daigonistics(111,'CBP')
    db.session.add(new_daignosis)
    new_daignosis = daigonistics(111,'Lipid')
    db.session.add(new_daignosis)
    db.session.commit()
    return f"Successfully created a new Daignosis"

@app.route('/addMedicine')
def addMedicine():
    new_medicine = master_medicine("Acebutolol", 30,55)
    db.session.add(new_medicine)
    new_medicine = master_medicine("Corgard", 30,2000)
    db.session.add(new_medicine)
    new_medicine = master_medicine("Tenormin", 30,100)
    db.session.add(new_medicine)    
    db.session.commit()
    return f"Added 3 new medicines"

@app.route('/addPatientMedicine')
def addPatientMedicine():
    new_medicine = medicines(111,"Acebutolol", 30)
    db.session.add(new_medicine)
    db.session.commit()
    return f"Added 3 new medicines"

@app.route('/adduser')
def adduser():
    new_user = users("Sandeep","123456")
    db.session.add(new_user)
    new_user = users("Dibyasha","123456")
    db.session.add(new_user)
    new_user = users("Sanjay","123456")
    db.session.add(new_user)
    new_user = users("Satrupa","123456")
    db.session.add(new_user)
    new_user = users("Suchitra","123456")
    db.session.add(new_user)
    db.session.commit()
    return f"Users added"



if __name__ == "__main__":
    webbrowser.open('http://127.0.0.1:5000/')
    db.create_all()
    app.run(use_debugger=False,use_reloader=False)