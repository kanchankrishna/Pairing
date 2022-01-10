from flask import Flask, flash, render_template, request
from apscheduler.scheduler import Scheduler
import sqlite3 as sql
import atexit


app = Flask(__name__)
app.secret_key = "random string"

class MatchingInterest:  
    def __init__(interest, addname, addstore, addhobby, addlang, addsibling, addSports, addGrade):  
        interest.addname = addname  
        interest.addstore = addstore
        interest.addhobby = addhobby
        interest.addlang = addlang
        interest.addsibling = addsibling
        interest.addSports = addSports
        interest.addSubject = addSubject
        interest.addGrade = addGrade

@app.route("/about")
def show_about():
    return render_template("about.html")

@app.route("/match")
def cancel_reservation():
    return render_template("match.html")

@app.route("/")
def home():
    conn = sql.connect("database.db")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS characteristics (name TEXT, store TEXT, hobby TEXT, Languages TEXT, Siblings TEXT, Sports TEXT, Subjects TEXT, Grades TEXT )"
        )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS reviews (reviews TEXT)"
        )
    conn.commit()
    conn.close()
    return render_template("homepage.html")


@app.route("/aftermatch", methods=["POST", "GET"])
def match():
    name = request.form['name']
    store = request.form['store']
    hobby = request.form.get('hobby')
    first_language = request.form.get('Languages')
    siblings = request.form.get('Siblings')
    sport = request.form.get('Sports')
    subject = request.form.get('Subjects')
    grade = request.form.get('Grades')
    #get the selected values that will be compared to another user's values
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute(" SELECT * FROM characteristics WHERE name  = ? or store= ? or hobby = ? or Languages = ? or siblings =? or Sports = ? and Subjects = ? and Grades = ?", [name, store, hobby, first_language, siblings, sport, subject, grade])
    rows = cur.fetchall()
    nothingmatched="false"
    if len(rows) == 0:
       nothingmatched="true"
       cur.execute(" SELECT * FROM characteristics")
       rows = cur.fetchall() 
    
    cur.execute("INSERT INTO characteristics (name,store,hobby,Languages, Siblings, Sports, Subjects, Grades) VALUES (?,?,?,?,?,?,?,?)",
                    (
                        name,
                        store,
                        hobby,
                        first_language,
                        siblings,
                        sport,
                        subject,
                        grade
                    ),
                )
    con.commit()
    #interestlist = []  
  
    # for dbrow in rows: 
     #   if (name== dbrow["name"]):
      #      addname=true;     
      #  if (store==dbrow["store"]):
       #     addstore=true;
     #   if (hobby==dbrow["hobby"]):
       #     addhobby=true;
       # if (first_language==dbrow["Languages"]):
        #    addlang=true
     #   if (siblings==dbrow["Siblings"]):
       #     addsibling=true
      #  if (sport==dbrow["Sports"]):
      #      addSports=true
       # if (subject==dbrow["Subjects"]):
       #     addSubject=true
       # if (grade==dbrow["Grades"]):
        #    addGrade=true
       # MatchingInterest(addname, addstore, addhobby, addlang, addsibling, addSports, addSubject, addGrade) 
    return render_template("matchedinterests.html", rows=rows, nothingmatched=nothingmatched)

@app.route("/viewmatches")
def view_matches():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute(" SELECT * FROM characteristics")
    #WHERE name  = ? or store= ? or hobby = ? or Languages = ? or siblings =? or Sports = ? and Subjects = ? and Grades = ?", [name, store, hobby, first_language, siblings, sport, subject, grade])
    rows = cur.fetchall()
    return render_template("matchedinterests.html", rows=rows)

@app.route("/reviews")
def view_reviews():
    return render_template("reviews.html")


@app.route('/savereviews', methods = ["POST"])
def save_reviews():
    if request.method == "POST":
        user_review = request.form["theuserreview"]
        conn = sql.connect("database.db")
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO reviews (reviews) VALUES (?)",
            (user_review,)
        )
        conn.commit()
        flash(
            "Thank you for submitting your review! Enjoy the app.")
        return render_template("reviews.html")





if __name__ == "__main__":
    app.run(debug=True)

