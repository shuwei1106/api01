import flask
from flask import request, jsonify
from flask_restful import Api,Resource
from resource.user import Users, User
from resource.accounts import Accounts, Account
import pymysql
app = flask.Flask(__name__)
app.config['DEBUG'] = True
api = Api(app)
api.add_resource(Users, '/users')
api.add_resource(User, '/user/<id>')
api.add_resource(Accounts, '/bank-accounts')
api.add_resource(Account, '/bank-account/<id>')

@app.route('/',methods=['GET'])
def home():
    return "<h1>Hello World</h1>"

# 加密設定
@app.before_request
def auth():
    token = request.headers.get('auth')
    if token == '567':
        pass
    else:
        response = {'msg':'invalid token'}
        return response,401

# 檢查錯誤設定
@app.errorhandler(Exception)
def handle_error(error):
    status_code = 500
    if(type(error).__name__ == 'NotFound'):
        status_code = 400
    else:
        pass
    return {'msg': type(error).__name__}, status_code


@app.route('/account/<account_number>/deposit',methods=['POST'])
def deposit(account_number):
    db, cursor, account = get_account(account_number)
    money = request.values['money']
    balance = account['balance'] + int(money)
    sql = """
    Update test01.accounts Set balance = {} 
    where account_number = "{}"
    """.format(balance, account_number)
    cursor.execute(sql)
    db.commit()   
    db.close()
    response = {
        'result':True
    }
    return jsonify(response)

@app.route('/account/<account_number>/withdraw',methods=['POST'])
def withdraw(account_number):
    db, cursor, account = get_account(account_number)
    money = request.values['money']
    balance = account['balance'] - int(money)
    if balance < 0:
        response = {
            'result':False,
            'msg':'餘額不足'
        }
        code = 400

    else:
        sql = """
        Update test01.accounts Set balance = {} 
        where account_number = "{}"
        """.format(balance, account_number)
        cursor.execute(sql)
        db.commit()   
        db.close()
        response = {
            'result':True
        }
        code = 200
    return jsonify(response), code

        
def get_account(account_number):
    db = pymysql.connect('192.168.56.102','eason','671106','test01')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = """Select * From test01.accounts where account_number = "{}"
    """.format(account_number)
    cursor.execute(sql)
    return db, cursor, cursor.fetchone()


if __name__ == '__main__':
    app.run(port=5000)