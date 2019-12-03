from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from Hdu_Bro_Driver import Hdu_Bro_Driver
from Hdu_Bro_Request import Hdu_Bro_Request, crack_code
import json, os, time

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you-will-never-guess!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/hdu_bro_help?charset=UTF8MB4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cors = CORS(app, supports_credentials=True)
db = SQLAlchemy(app)

# 接口使用情况
IterfaceUsed = 75
@app.route('/getIterfaceUsed')
def getIterfaceUsed():
    global IterfaceUsed
    return str(IterfaceUsed)

@app.route('/Iterface_Use')
def Iterface_Use():
    global IterfaceUsed
    IterfaceUsed += 1
    return 'Iterface_Use success'


class Student(db.Model):
    StudentNum = db.Column(db.String(8), primary_key=True)
    StudentToken = db.Column(db.String(36), nullable=False)
    StudentName = db.Column(db.String(10), nullable=False)
    StudentDept = db.Column(db.String(20),)
    StudentMajor = db.Column(db.String(20),)
    StudentClass = db.Column(db.String(8),)
    
    def __init__(self, StudentNum, StudentToken, StudentName, StudentDept, StudentMajor, StudentClass):
        self.StudentNum = StudentNum
        self.StudentToken = StudentToken
        self.StudentName = StudentName
        self.StudentDept = StudentDept
        self.StudentMajor = StudentMajor
        self.StudentClass = StudentClass

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/hdu_login', methods=['POST'])
def hdu_login():
    data = request.get_json()
    student_num = data['studentnum']
    passwd = data['password']
    if not Student.query.filter_by(StudentNum=student_num).all():
        # 调用Selenium自动登陆账户，获取个人信息和token
        try:
            bro = Hdu_Bro_Driver(headless=True)
            bro.driver.get('https://skl.hduhelp.com/#/call/course')
            bro.login(student_num, passwd)
            user_info = bro.get_user_info()
            print('用户信息:')
            print(user_info)
            token = bro.get_token()
            print('token: ',token)
        except Exception as e:
            print(e)
            return 'failed!'
        finally:
            bro.driver.quit()
        # 将登陆的账户添加至数据库中，仅记录个人信息和token，不记录密码，
        # Student(StudentNum, StudentToken, StudentName, StudentDept, StudentMajor, StudentClass)
        student = Student(user_info[1], token, user_info[0], user_info[2], user_info[3], user_info[4])
        db.session.add(student)
        db.session.commit()
    return 'hdu_login success!'

@app.route('/deleteAccount', methods=['POST'])
def delete_student():
    studentnum = request.get_json()['studentnum']
    delete_stu = Student.query.filter_by(StudentNum=studentnum).first()
    db.session.delete(delete_stu)
    db.session.commit()
    return 'deleteAccount success!'

@app.route('/getAccounts')
def getAccounts():
    students = Student.query.order_by(Student.StudentNum).all()
    Accounts = []
    for student in students:
        a = {}
        a['name'] = student.StudentName
        a['studentnum'] = student.StudentNum
        a['token'] = student.StudentToken
        Accounts.append(a)
    return json.dumps(Accounts)

@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    checkCode = data['checkCode']
    tokens = data['tokens']
    res = []
    for token in tokens:
        student = Student.query.filter_by(StudentToken=token).first()
        bro = Hdu_Bro_Request(token)
        bro.code_check_in(checkCode)
        while True:
            img_stream = bro.create_code_img()
            valid_code = crack_code(img_stream)
            #print(valid_code)
            valid_state = bro.valid_code(valid_code)
            if valid_state == 200:
                res.append({
                    'type': 'success',
                    'content': student.StudentName+'，签到成功!'
                })
                break
            elif valid_state == 400:
                continue
            elif valid_state == 401:
                res.append({
                    'type': 'warning',
                    'content': student.StudentName+'，签到码无效!'
                })
                break
            else:
                res.append({
                    'type': 'warning',
                    'content': valid_state
                })
                break
    return json.dumps(res)

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000)