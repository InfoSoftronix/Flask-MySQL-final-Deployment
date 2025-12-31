from flask import Flask,render_template,redirect,request,jsonify,url_for
app=Flask(__name__)

from flask_mysqldb import MySQL

import os

app.config['MYSQL_DB'] = os.getenv("MYSQL_DB", "employee_db")
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER", "root")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD", "root")
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST", "localhost")
app.config['MYSQL_PORT'] = int(os.getenv("MYSQL_PORT", 3306))

mysql=MySQL(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add")
def addEmployee():
    return render_template("registration.html")

@app.route("/reg",methods=["GET","POST"])
def register():
    if request.method=="POST":
        eid=request.form["eid"]
        ename=request.form["ename"]
        esal=request.form["esal"]
        eaddr=request.form["eaddr"]
        egender=request.form["egender"]

        con=mysql.connection.cursor()
        query="insert into employee(eid,ename,esal,eaddr,egender) values(%s,%s,%s,%s,%s)"
        con.execute(query,(eid,ename,esal,eaddr,egender))
    
        mysql.connection.commit()
        con.close()
    return redirect(url_for("index"))


@app.route("/show")
def show():
    con=mysql.connection.cursor()
    query="select * from employee"
    con.execute(query)
    employee=con.fetchall()
    mysql.connection.commit()
    return render_template("show.html",employee=employee)

@app.route("/delete/<int:eid>")
def deleteEmloyee(eid):
    con=mysql.connection.cursor()
    query="delete from employee where eid=%s"
    con.execute(query,(eid,))
    mysql.connection.commit()

    return redirect(url_for("show"))


@app.route("/edit/<int:eid>")
def editEmloyee(eid):
    con=mysql.connection.cursor()
    query="select * from employee where eid=%s"
    con.execute(query,(eid,))
    employee=con.fetchone()
    mysql.connection.commit()

    return render_template("edit.html",emp=employee)

@app.route("/update",methods=["GET","POST"])
def updateEmployee():
    if request.method=="POST":
        eid=request.form["eid"]
        ename=request.form["ename"]
        esal=request.form["esal"]
        eaddr=request.form["eaddr"]
        egender=request.form["egender"]

        con=mysql.connection.cursor()
        query="update employee set ename=%s,esal=%s,eaddr=%s,egender=%s where eid=%s"
        con.execute(query,(ename,esal,eaddr,egender,eid))
    
        mysql.connection.commit()
        con.close()
    return redirect(url_for("show"))


    


if __name__ == '__main__':
    app.run(debug=True)