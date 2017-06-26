from flask import Flask, render_template, json, request, redirect,url_for,session,jsonify
from werkzeug import generate_password_hash, check_password_hash
from flaskext.mysql import MySQL
from flask import session
import re

app = Flask(__name__)
app.secret_key = 'squirrels like to play in the park.'

mysql = MySQL()
#SAUSAGE
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

@app.route('/home')
def userHome():
    if session.get('user'):

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('getItems',(session['email'],))
        entries = [dict(id=row[0], user=row[1],name=row[2], url=row[3], price= row[4],shipping= row[5],stock_no= row[6],status=row[7], last_updated = row[8], regex= row[9]) for row in cursor.fetchall()]

        return render_template('user_home.html',result=request.args.get('result'), success=request.args.get('success'), items = entries)
    else:
        return render_template('error.html',error = 'Unauthorized Access')


@app.route('/logout')
def logout():
    session.pop('user',None)
    session.pop('email',None)
    return redirect('/')

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
                session['email'] = _username
                return redirect('/home')
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
    return render_template('sign_up.html', result=request.args.get('result'), success=request.args.get('success'))

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
            return url_for('showSignin',result="Registration Successful. Please login: ",success=1)
        else:
            return url_for('showSignUp',result='Username already exists. :( ', success=0)
    else:
            return url_for('showSignUp', result = 'Error creating user. Please try again :(', success = 0)


@app.route('/add')
def showAddItem():
    return render_template('add_item.html')


@app.route('/add',methods=['POST'])
def addItem():
    url = request.form['inputUrl']

    urlCheck = re.search( r'[www.|\s?]([a-z]+)\.[com|co\.uk]+\/([\%0-9a-zA-Z-]+)', url, re.M|re.I)

    if urlCheck:
       item = urlCheck.group(2)
       if urlCheck.group(1) == 'wayfair':
           cursor.callproc('addItem',(url,session['email'], item))
           data = cursor.fetchall()
           if len(data) is 0:
               conn.commit()
               result = "Added: " + url
               return render_template('add_item.html', result = result, success = 1)
           else:
               return render_template('add_item.html', result = 'Item already added.', success = 0)
       else:
            result = "Only wayfair is supported for now."
            return render_template('add_item.html', result = result, success = 0)
    else:
       result = "Error adding link :("
       return render_template('add_item.html', result = result, success = 0)


@app.route('/delete/<name>')
def delete_item(name):
    print "NAME: " + name;
    cursor.callproc('deleteItem',(name,session['email']))
    data = cursor.fetchall()
    if len(data) is 0:
      conn.commit()
      return redirect(url_for('userHome', result = '', success = 1))
    else:
      return redirect(url_for('userHome', result = 'Error deleting item.', success = 0))

    



if __name__ == "__main__":
    app.run(host='10.8.46.3')
