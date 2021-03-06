import certifi
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta


from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.timeAttack


app = Flask(__name__)

SECRET_KEY = 'SPARTA'

@app.route('/')
def home():
    # token_receive = request.cookies.get('mytoken')
    # try:
        # payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    return render_template('index.html')
    # except jwt.ExpiredSignatureError:
    #     return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    # except jwt.exceptions.DecodeError:
    #     return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login_page():
   return render_template('login.html')


# 회원가입
@app.route('/sign_up', methods=['POST'])
def sign_up():
    email_receive = request.form['email_give']
    pw_receive = request.form['pw_give']
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    doc = {
        "email": email_receive,  # 아이디
        "pw": pw_hash,  # 비밀번호
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    email_receive = request.form['email_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'email': email_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': email_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})



if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)
