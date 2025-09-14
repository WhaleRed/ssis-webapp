from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/colleges')
def colleges():
  return render_template("college.html")

@app.route('/programs')
def programs():
  return render_template("program.html")

@app.route('/students')
def students():
  return render_template("student.html")