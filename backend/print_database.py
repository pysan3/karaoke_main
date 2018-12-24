import sqlite3

con = sqlite3.connect('./database.sqlite3')
cur = con.cursor()
result = cur.execute("select * from users").fetchall()
for des in cur.description:
    print(des[0])
for x in result:
    print(x)

print('done')

con.close()