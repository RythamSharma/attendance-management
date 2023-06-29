from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance_record.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class AttendanceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"AttendanceRecord(name={self.name}, roll={self.roll}, subject={self.subject}, status={self.status})"

class RolltoName(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(80), nullable=False)


qrs_generated=[]

@app.route('/addRoll', methods=['GET','POST'])
def add():
    name="naman"
    student = RolltoName(roll_number=45, name="naman")
    student2 = RolltoName(roll_number=26, name="kavya")
    student3 = RolltoName(roll_number=2, name="gagan")
    db.session.add(student)
    db.session.add(student2)
    db.session.add(student3)
    db.session.commit()
    return "added"


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    roll_number = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Student %r>' % self.username





@app.route('/add_student')
def add_student():
    # create a new student
    
    new_student2 = Student(username='kavya', password='1234', roll_number='26')


    # add the new student to the database
   
    db.session.add(new_student2)
   
    db.session.commit()

    return 'New student added to the database!'
roll_no = 0
per=0
sub="N/A"
@app.route('/log', methods=['POST','GET'])
def login():
    print("yea")
    print(request.form)
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    if(username=="faculty" and password=="5678"):
        return "teacher"

    student = Student.query.filter_by(username=username, password=password).first()
    print(student)
    if student:
        print("FOUND")
        print(student.roll_number)
        global roll_no
        roll_no=student.roll_number;

        return "success "+student.roll_number;
    else:
        return "failed"


@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/loginus')
def loginus():
    return render_template('login.html')


@app.route('/tryon')
def tryon():
    return render_template('tryon.html')

@app.route('/studash')
def studash():
   
    print(str(roll_no)+" printed")
    return render_template('studash.html',sub=sub,per=per)
@app.route('/teacher')
def teacher():
    return render_template('teacherportal.html')

@app.route('/qrscanner')
def qrscanner():
    global per
    per=100
    global sub
    sub="Computer Networks" 
    return render_template("qrscanner.html")
@app.route('/qrgen')
def qrgen():
    return render_template('qrcode.html')

@app.route('/qrtimeover')
def qrtime():
    return "TIME EXPIRED"

@app.route('/attend')
def add_attendance_record():
    print(roll_no)
    a = request.url
    b=a.split('=')
    if(b[1] in qrs_generated):
        return "old qr"
    else:
        qrs_generated.append(b[1])
        print(qrs_generated)
   
    student = RolltoName.query.filter_by(roll_number=int(roll_no)).first()
    print(student)
    record = AttendanceRecord(name=student.name, roll=student.roll_number, subject="COMPUTER NETWORKS", status="Present")
    db.session.add(record)
    db.session.commit()
    get_attendance_records()
    return "success"

@app.route('/clear_table')
def clear_table():
    db.session.query(AttendanceRecord).delete()
    db.session.commit()
    return 'Table cleared'

@app.route('/attendance')
def attendance():
    records = get_attendance_records()
    print(records)
    return render_template('attendancelist.html', records=records)

def get_attendance_records():
    records = AttendanceRecord.query.all()
    record_list = []
    for record in records:
        record_dict = {
            'name': record.name,
            'roll': record.roll,
            'subject': record.subject,
            'status': record.status
        }
        record_list.append(record_dict)
    print(record_list)
    return record_list



if __name__ == '__main__':
    
    app.run(debug=True)
    