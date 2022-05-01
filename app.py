# made by akash


from flask import Flask, request, jsonify,url_for,redirect, make_response, request, render_template, session
import jwt
from datetime import datetime, timedelta
from functools import wraps
import sqlite3 as sql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'Message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return decorated


@app.route('/register')
def new_student():
   return render_template('signup.html')

@app.route('/adduser',methods = ['POST'])
def addrec():
   if request.method == 'POST':
      try:
        #  data=request.get_json()
        #  print(data)
        #  na=data["name"]
        #  em=data["email"]
        #  mo=data["mobile"]
        #  pa=data["password"]
         na = request.form['fullname']
         em = request.form['email']
         mo = request.form['number']
         pa = request.form['password']
         with sql.connect("database.db") as con:
            cur = con.cursor()
            print("Hello")
            cur.execute("INSERT INTO  newuser(name,email,mobile,password) VALUES (?,?,?,?)",(na,em,mo,pa) )
            con.commit()
            msg = "Record successfully added"
            print("added sucessfully")
      except:
         con.rollback()
         msg = "error in insert operation"
         print("not added")
      
      finally:
         return redirect(url_for("home"))
         con.close()

@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row  
   cur = con.cursor()
   cur.execute("select * from newuser")
   li=[]
   rows = cur.fetchall()
   for i in range(0,len(rows)):
    dict={}
    dict["name"]=rows[i][0]
    dict["email"]=rows[i][1]
    dict["mobile"]=rows[i][2]
    li.append(dict)

#    print(li)
   return make_response(jsonify(li))

@app.route('/login')
def login():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'logged in currently'

@app.route('/loggedin', methods=['POST'])
def loggedin():
    conn=sql.connect("database.db")
    curr=conn.cursor()
    # data=request.get_json()
    # print(data)
    uname=request.form['username']
    passw=request.form['password']
    # uname=data["username"]
    # passw=data["password"]
    print(uname)
    print(passw)
    curr.execute("SELECT * FROM newuser WHERE name=? and password=?",(uname,passw))
    rows=curr.fetchall()
    if len(rows)!=0:
        session['logged_in'] = True
        session["user"]=uname
        loggedin=True
        token = jwt.encode({
            'user': uname,
            # don't foget to wrap it in str function, otherwise it won't work [ i struggled with this one! ]
            'expiration': str(datetime.utcnow() + timedelta(seconds=60))
        },
            app.config['SECRET_KEY'])
        tokens = jsonify({'token': token.decode('utf-8')})
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))

@app.route('/home')
def home():
    login = False
    if session["logged_in"]==True:
        login=True
    return render_template("index.html",login=login)

@app.route('/')
def root():
    login = False
    return render_template("index.html",login=login)


@app.route('/logout')
def logout():
    session["logged_in"]=False
    session["user"]=""
    loggedin=False
    return redirect(url_for('home'))

@app.route("/cart")
def cart():
    if not session.get('logged_in'):
        return redirect(url_for("login"))
    else:
        return render_template("cart.html")




@app.route("/corona")
def corona():
    return render_template("corona.html")


@app.route("/aws")
def aws():
    return redirect("http://0.0.0.0:5001/load")
if __name__ == '__main__':
    app.run(debug = True , host="0.0.0.0")