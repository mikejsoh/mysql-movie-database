from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from front import front_blueprint
import mysql.connector

app = Flask(__name__)

app.register_blueprint(front_blueprint)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/staff")
def welcome():
    return render_template("staff.html")

@app.route("/staff/movies")
def movieLoad():

    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()

    query = ("select * from Movie order by MovieName")
    cursor.execute(query)

    movies = cursor.fetchall()
    cursor.close()
    cnx.close()

    return render_template('movies.html', movies=movies)

@app.route("/staff/genres")
def genreLoad():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()

    query = ("select MovieName,Genre FROM Movie INNER JOIN Genre ON Movie.MovieID=Genre.MovieID order by Genre;")
    cursor.execute(query)

    genres = cursor.fetchall()
    cursor.close()
    cnx.close()

    return render_template('genres.html', genres=genres)

@app.route("/staff/rooms")
def roomLoad():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()

    query = ("SELECT * FROM Rooms")
    cursor.execute(query)

    rooms = cursor.fetchall()
    cursor.close()
    cnx.close()

    return render_template('rooms.html', rooms=rooms)

@app.route("/staff/showings")
def showingLoad():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()

    query = ("SELECT * FROM Showing ORDER BY ShowingDateTime")
    cursor.execute(query)

    showings = cursor.fetchall()
    cursor.close()
    cnx.close()

    return render_template('showings.html', showings=showings)

@app.route("/staff/customers")
def customerLoad():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()

    query = ("SELECT * FROM Customer")
    cursor.execute(query)

    customers = cursor.fetchall()
    cursor.close()
    cnx.close()

    return render_template('customers.html', customers=customers)

@app.route("/staff/attend")
def attendLoad():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()

    query = ("select * from Attend")
    query = ("select Customer.FirstName, Customer.LastName, Showing.ShowingID, Showing.ShowingDateTime, Movie.MovieID, Movie.MovieName, Attend.Rating from Customer join Attend on Customer.CustomerID = Attend.CustomerID join Showing on Showing.ShowingID = Attend.ShowingID join Movie on Movie.MovieID = Showing.MovieID order by Attend.Rating")
    cursor.execute(query)

    attends = cursor.fetchall()
    cursor.close()
    cnx.close()

    return render_template('attend.html', attends=attends)

# Start of Movie Functions
@app.route("/staff/addmovie", methods=['POST'])
def addMovie():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    insert_stmt = (
        "INSERT INTO Movie (MovieID, MovieName, YearReleased) "
        "VALUES (%s, %s, %s)"
    )

    data = (request.form['MovieID'], request.form['MovieName'], request.form['YearReleased'])
    cursor.execute(insert_stmt,data)
    cnx.commit()
    cnx.close()
    return redirect(url_for('movieLoad'))

@app.route("/staff/editmovie", methods=['GET','POST'])
def editMovie():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    insert_stmt = "update Movie set MovieName = %s, YearReleased = %s where MovieID = %s"

    data = (request.form['MovieName'], request.form['YearReleased'], request.form['MovieID'])
    cursor.execute(insert_stmt, data)
    cnx.commit()
    cnx.close()
    return redirect(url_for('movieLoad'))

@app.route("/staff/deletemovie", methods=['POST'])
def deleteMovie():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    insert_stmt = "DELETE FROM Movie WHERE MovieID = %s"
    

    data = (request.form['MovieID'],)
    cursor.execute(insert_stmt,data)
    cnx.commit()
    cnx.close()
    return redirect(url_for('movieLoad'))
# End of Movie Functions


# Start of Genre Functions
@app.route("/staff/addgenre", methods=['POST'])
def addGenre():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    insert_stmt = (
        "insert into Genre (Genre, MovieID) "
        "values (%s, %s)")

    data = (request.form['Genre'], request.form['MovieID'])
    cursor.execute(insert_stmt, data)
    cnx.commit()
    cnx.close()
    return redirect(url_for('genreLoad'))

@app.route("/staff/deletegenre", methods=['POST'])
def delGenre():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    insert_stmt = "delete from Genre where Genre = %s and MovieID = %s"

    data = (request.form['Genre'], request.form['MovieID'])
    cursor.execute(insert_stmt, data)
    cnx.commit()
    cnx.close()
    return redirect(url_for('genreLoad'))
# End of Genre Functions


# Start of Room Functions
@app.route("/staff/addroom", methods=['POST'])
def addRoom():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    insert_stmt = (
        "insert into Rooms (RoomNumber, Capacity) "
        "values (%s, %s)")

    data = (request.form['RoomNumber'], request.form['Capacity'])
    cursor.execute(insert_stmt, data)
    cnx.commit()
    cnx.close()
    return redirect(url_for('roomLoad'))

@app.route("/staff/editroom", methods=['GET', 'POST'])
def editRoom():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    insert_stmt = "update Rooms set Capacity = %s where RoomNumber = %s"

    data = (request.form['Capacity'], request.form['RoomNumber'])
    cursor.execute(insert_stmt, data)
    cnx.commit()
    cnx.close()
    return redirect(url_for('roomLoad'))

@app.route("/staff/deleteroom", methods=['POST'])
def delRoom():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    insert_stmt = "DELETE FROM Rooms WHERE RoomNumber = %s"

    data = (request.form['RoomNumber'],)
    cursor.execute(insert_stmt, data)
    cnx.commit()
    cnx.close()
    return redirect(url_for('roomLoad'))
# End of Room Functions


# Start of Showings Functions
@app.route("/staff/addshowing", methods=['POST'])
def addShowing():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    insert_stmt = (
        "insert into Showing (ShowingID, ShowingDateTime, MovieID, RoomNumber, TicketPrice) "
        "values (%s, %s, %s, %s, %s)")

    data = (request.form['ShowingID'], request.form['ShowingDateTime'], request.form['MovieID'], request.form['RoomNumber'], request.form['TicketPrice'])
    cursor.execute(insert_stmt, data)
    cnx.commit()
    cnx.close()
    return redirect(url_for('showingLoad'))

@app.route("/staff/editshowing", methods=['GET','POST'])
def editShowing():
    cnx = mysql.connector.connect(user="root", database="MovieTheatre")
    cursor = cnx.cursor()
    insert_stmt = "update Showing set ShowingDateTime = %s, TicketPrice = %s where (MovieID = %s and RoomNumber = %s and ShowingID = %s)"

    data = (request.form['ShowingDateTime'], request.form['TicketPrice'], request.form['MovieID'], request.form['RoomNumber'], request.form['ShowingID'])
    cursor.execute(insert_stmt, data)
    cnx.commit()
    cnx.close()
    return redirect(url_for('showingLoad'))

@app.route("/staff/deleteshowing", methods=['POST'])
def delShowing():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    insert_stmt = "delete from Showing where ShowingID = %s and MovieID = %s and RoomNumber = %s"

    data = (request.form['ShowingID'], request.form['MovieID'], request.form['RoomNumber'])
    cursor.execute(insert_stmt, data)
    cnx.commit()
    cnx.close()
    return redirect(url_for('showingLoad'))
# End of Showings Functions


# Start of Customer Functions
@app.route("/staff/addcustomer", methods=['POST'])
def addCustomer():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    insert_stmt = (
        "insert into Customer (CustomerID, FirstName, LastName, Sex, Email) "
        "values (%s, %s, %s, %s, %s)")

    data = (request.form['CustomerID'], request.form['FirstName'], request.form['LastName'], request.form['Sex'], request.form['Email'])
    cursor.execute(insert_stmt, data)
    cnx.commit()
    cnx.close()
    return redirect(url_for('customerLoad'))

@app.route("/staff/editcustomer", methods=['GET', 'POST'])
def editCustomer():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    insert_stmt = "update Customer set FirstName = %s, LastName = %s, Sex = %s, Email = %s where CustomerID = %s"

    data = (request.form['FirstName'], request.form['LastName'], request.form['Sex'], request.form['Email'], request.form['CustomerID'])
    cursor.execute(insert_stmt, data)
    cnx.commit()
    cnx.close()
    return redirect(url_for('customerLoad'))

@app.route("/staff/deletecustomer", methods=['POST'])
def delCustomer():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    insert_stmt = "delete from Customer where CustomerID = %s"

    data = (request.form['CustomerID'],)
    cursor.execute(insert_stmt, data)
    cnx.commit()
    cnx.close()
    return redirect(url_for('customerLoad'))
# End of Customer Functions

# Start of SQL Injection
@app.route("/sqlinjection")
def sqlInjection():
    return render_template('sqlinjection.html')

@app.route("/showsqlinjection", methods=['GET', 'POST'])
def showSqlInjection():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    '''
    insert_stmt = "select * from Movie where MovieName=%s"
    data = (request.form['MovieName'],)
    cursor.execute(insert_stmt, data)
    '''
    data = (request.form['MovieName'],)
    cursor.execute("select * from Movie where MovieName='%s'" % data)

    movies = cursor.fetchall()
    #cnx.commit()
    cnx.close()

    return render_template('showsqlinjection.html',movies=movies)

# End of SQL Injection

'''
@app.route("/addattend", methods=['POST'])
def addAttend():
    cnx = mysql.connecto.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    insert_stmt = ("insert into Attend (CustomerID, ShowingID, Rating)"
        "values (%s, %s, %s)")

    data = (request.form['CustomerID'], request.form['ShowingID'], request.form['Rating'])
    cursor.execute(insert_stmt, data)
    cnx.commit()
    cnx.close()
    return redirect(url_for('attendLoad'))
'''

if (__name__) == "__main__":
    app.run(host="0.0.0.0", debug=True)