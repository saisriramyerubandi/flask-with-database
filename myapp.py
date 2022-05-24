from flask import Flask, render_template,request
import psycopg2
import os
app = Flask(__name__)


def database_connection():
    connect = psycopg2.connect("dbname=digitalmusic user=postgres password=########", host="127.0.0.1", port="5432")
    return connect

@app.route("/", methods=['GET', 'POST'])
def homeresults():
    if request.method == 'POST':
        sql_query = request.form['sql_query'] 
        #sql = f'select * from albums where artist={sql_query}'
        if(sql_query[0]=='s'):
            connect = database_connection()
            cursor = connect.cursor()
            cursor.execute(sql_query)
            results = cursor.fetchall()
            #connect.commit()
            cursor.close()
            connect.close()
            return render_template('homepage.html',results=results,cur=cursor)
        else:
            connect = database_connection()
            cursor = connect.cursor()
            cursor.execute(sql_query)
            #results = cursor.fetchall()
            connect.commit()
            cursor.close()
            connect.close()
            #return render_template('homepage.html',results=results,cur=cursor)
            return render_template('homepage.html')

    else:
        return render_template('homepage.html')

@app.route("/albums", methods=['GET','POST'])
def albums():
    if request.method == 'POST':
        sql_query = request.form['sql_query'] 
        #text = '{sql_query}'
        sql = f"""select * from album where artistid = (select artistid from artist where name = '%s')""" %(sql_query)
        connect = database_connection()
        cursor = connect.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        connect.close()
        return render_template('albums.html',results=results,cur=cursor)
    else:
        return render_template('albums.html')

@app.route("/shop", methods=['GET','POST'])
def shop():
    if request.method == 'POST':
        firstname = request.form['firstname'] 
        lastname= request.form['lastname']
        #print(request.form)
        address= request.form['address']
        postalcode= request.form['postalcode']
        phonenumber= request.form['phonenumber']
        email= request.form['email']
        albumname = request.form['albumname']
        #customerid = 60
        #print(firstname, lastname)

        #text = '{sql_query}'
        #sql = f"""select * from album where artistid = (select artistid from artist where name = {sql_query})"""
        sql = f""" insert into customer(firstname , lastname, address, postalcode,phone,email) values ('%s','%s','%s','%s','%s','%s')""" %(firstname,lastname,address,postalcode,phonenumber,email)

        connect = database_connection()
        cursor = connect.cursor()
        cursor.execute(sql)
        #results = cursor.fetchall()
        #results = f"""Hurray! Your Oder for {albumname} has been recieved"""
        connect.commit()
        cursor.close()
        connect.close()
        results = f"""We have recived your order for %s""" %(albumname)
        return render_template('shopsuccess.html',results = results)
    else:
        return render_template('shop.html')        


@app.route("/team")
def team():
    
        return render_template('team.html')
   

if __name__ == "__main__":
    app.run()