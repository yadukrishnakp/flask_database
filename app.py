from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


# home page in here we can add student details
@app.route('/')
def home():
    return render_template('home.html')


# add home student details into database
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


# fetching all student details
@app.route('/api/student', methods=['GET', 'POST'])
def student():
    with sqlite3.connect("student.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM student_details")
        rows = c.fetchall()
        return render_template('result.html', rows=rows)


# checking student is in database
@app.route('/api/student/<roll_no>/marks/add/', methods=['GET', 'POST'])
def add_mark(roll_no):
    with sqlite3.connect("student.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM student_details WHERE roll_number=?", (roll_no,))
        stud = c.fetchone()
        if stud:
            return render_template('add_mark.html', stud=stud[0])
        else:
            return render_template('result.html', invalid='invalid input, check roll number')


# storing student mark in to database
@app.route('/api/student/added/marks', methods=['GET', 'POST'])
def updated_mark():
    if request.method == "POST":
        s_roll_no = request.form["student_roll_no"]
        s_mark = request.form["student_mark"]
        with sqlite3.connect("student.db") as conn:
            c = conn.cursor()
            result = c.execute("SELECT * FROM student_mark_table WHERE roll_no=?", (s_roll_no,))
            result = result.fetchone()
            if result:
                return render_template('result.html', mark_exist='mark already added')
            else:
                # c.execute(
                #     'create table student_mark_table(roll_no integer not null,mark text not null)')
                c.execute("insert into student_mark_table values(?,?)", (s_roll_no, s_mark))
                conn.commit()
                return render_template('result.html', success='mark added')


# fetching mark of a particular student
@app.route('/api/student/<roll_no>/marks/', methods=['GET', 'POST'])
def show_mark(roll_no):
    with sqlite3.connect("student.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM student_mark_table WHERE roll_no=?", (roll_no,))
        stud = c.fetchone()

        if stud:
            return render_template('result.html', student_mark=stud)
        else:
            return render_template('result.html', invalid='invalid input, check roll number')


# fetching mark details of all students, sorting on marks into grades and also calculating distinction percentage,
# first class percentage and pass percentage
@app.route('/api/student/results/', methods=['GET', 'POST'])
def show_final_mark():
    with sqlite3.connect("student.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM student_mark_table")
        stud = c.fetchall()
        length = len(stud)
        a = 0
        b = 0
        c = 0
        d = 0
        e = 0
        f = 0
        for i in stud:
            if 100 >= int(i[1]) >= 91:
                a = a + 1
            elif 90 >= int(i[1]) >= 81:
                b = b + 1
            elif 80 >= int(i[1]) >= 71:
                c = c + 1
            elif 70 >= int(i[1]) >= 61:
                d = d + 1
            elif 61 >= int(i[1]) >= 55:
                e = e + 1
            else:
                f = f + 1
        distinction_percentage = (a / length) * 100
        first_class_percentage = ((b + c) / length) * 100
        pass_percentage = ((length - f) / length) * 100
    return render_template('final_result.html', a=a, b=b, c=c, d=d, e=e, f=f, length=length,
                           distinction_percentage=distinction_percentage, first_class_percentage=first_class_percentage,
                           pass_percentage=pass_percentage)


if __name__ == '__main__':
    app.run(debug=True)
