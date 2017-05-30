from flask import Flask, render_template, json, request
from werkzeug import generate_password_hash, check_password_hash
from flaskext.mysql import MySQL
from flask import session

app = Flask(__name__)
app.secret_key = 'squirrels like to play in the park.'

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'scraper'
app.config['MYSQL_DATABASE_PASSWORD'] = '42Ir&fdds'
app.config['MYSQL_DATABASE_DB'] = 'scraper'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

@app.route("/")
def main():
	return render_template('index.html')

@app.route('/showSignin')
def showSignin():
    return render_template('sign_in.html')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
 
 
 
        # connect to mysql
 
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('validateLogin',(_username,))
        data = cursor.fetchall()
 
        if len(data) > 0:
            if check_password_hash(str(data[0][3]),_password):
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')
 
 
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()

 


@app.route('/showSignUp')
def showSignUp():
    return render_template('sign_up.html')

@app.route('/signUp',methods=['POST'])
def signUp():
 
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
 
    # validate the received values
    if _name and _email and _password:
        _hashed_password = generate_password_hash(_password)
        cursor.callproc('createUser',(_name,_email,_hashed_password))
        data = cursor.fetchall()
        if len(data) is 0:
            conn.commit()
            return json.dumps({'message':'User created successfully !'})
    else:
        return json.dumps({'error':str(data[0])})

if __name__ == "__main__":
    app.run(host='10.8.46.3')
