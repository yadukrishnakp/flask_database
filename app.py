from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/add_student', methods=['GET', 'POST'])
def add_details():
    if request.method == "POST":
        s_roll_no = request.form["student_roll_no"]
        s_name = request.form["student_name"]
        s_dob = request.form["student_dob"]
        with sqlite3.connect("student.db") as conn:
            try:
                c = conn.cursor()
                # c.execute(
                #     'create table student_details(roll_number integer not null primary key, name text not null,'
                #     'date_of_birth text not null)')
                #
                c.execute("insert into student_details values(?,?,?)", (s_roll_no, s_name, s_dob))
            except:
                conn.rollback()
                conn.commit()
        return redirect(url_for('home'))


@app.route('/api/student', methods=['GET', 'POST'])
def student():
    with sqlite3.connect("student.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM student_details")
        rows = c.fetchall()
        return render_template('result.html', rows=rows)





if __name__ == '__main__':
    app.run(debug=True)
