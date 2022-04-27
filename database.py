import sqlite3
conn = sqlite3.connect('database.db')
cur = conn.cursor()
# cur.execute('CREATE TABLE createuser (name TEXT, email TEXT, mobile TEXT,address TEXT,password TEXT)')
cur.execute("DELETE from newuser where name='Dhruv'")
conn.close()
