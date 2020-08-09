from flask import Flask, render_template,request,redirect, url_for,session,flash
import sqlite3
import os
app = Flask(__name__)
app.secret_key = 'shourya'

@app.route('/')
def index():
	return render_template("dashboard.html")

'''
@app.route("/savedetails",methods = ["POST","GET"])  
def saveDetails():  
    msg = "msg"  
    if request.method == "POST":  
        try:  
            name = request.form["name"]  
            email = request.form["email"]  
            password = request.form["password"]  
            with sqlite3.connect("fantasy league.db") as con:  
                cur = con.cursor()  
                cur.execute("INSERT into Players (name, email, password) values (?,?,?)",(name,email,password))  
                con.commit()  
                msg = "SignUp Successful"  
        except:  
            con.rollback()  
            msg = "Error while Signing up. Try Again"  
        finally:  
            status = False
            return render_template("new.html",msg = msg,status=status)  
            con.close()  
'''

@app.route('/queries')
def queries():
    con = sqlite3.connect("site.db")
    con.row_factory = sqlite3.Row 
    cur = con.cursor() 
    cur.execute("select * from queries_table")
    rows = cur.fetchall()
    return render_template("query.html",rows = rows)



@app.route('/addmodify',methods = ["POST","GET"])
def add_modify():
    msg = "msg"  
    if request.method == "POST":  
        t_id = request.form["t_id"]  
        s_id = request.form["s_id"]
        t_name = request.form["t_name"]  
        s_name = request.form["s_name"]
        loc = request.form["loc"]  
  
        with sqlite3.connect("site.db") as con:  
            cur = con.cursor()  
            cur.execute("INSERT into Teacher_details (Teacher_id,School_id, teacher_name, School_name, Location) values (?,?,?,?,?)",(t_id, s_id, t_name, s_name, loc))  
            con.commit()  
            msg = "Successful" 
        con.close()   
    return render_template("add-modify.html",msg = msg)  
         

@app.route('/school_details')
def school_details():
	con = sqlite3.connect("site.db")
	con.row_factory = sqlite3.Row 
	cur = con.cursor() 
	cur.execute("select * from School_Table")
	rows = cur.fetchall()
	return render_template("school_details.html",rows = rows)


@app.route('/schools')
def schools():
	con = sqlite3.connect("site.db")
	con.row_factory = sqlite3.Row 
	cur = con.cursor() 
	cur.execute("select * from Teacher_details")
	rows = cur.fetchall()
	return render_template("schools.html",rows = rows)


@app.route("/schools/1")  
def prog1(): 
    return render_template("progress.html")


@app.route("/schools/2")  
def prog2(): 
    return render_template("progress2.html")      

if __name__ == '__main__':
	app.run(debug=True)