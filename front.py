from flask import Blueprint, Flask, render_template, request, redirect, url_for
import mysql.connector

front_blueprint = Blueprint('front', __name__)

@front_blueprint.route("/front")
def front():
    return render_template("front.html")

@front_blueprint.route("/front/search")
def searchLoad():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()

    query = ("select distinct Genre from Genre")
    cursor.execute(query)
    genres = cursor.fetchall()

    query = ("select date(ShowingDateTime) from Showing group by cast(ShowingDateTime as date)")
    cursor.execute(query)
    dates = cursor.fetchall()

    cursor.close()
    cnx.close()

    return render_template("search.html", genres=genres, dates=dates)

@front_blueprint.route("/front/submitgenre", methods=['GET','POST'])
def genreSearch():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()

    if request.form.get('check') == "True":
        insert_stmt = ("select * from Showing join Genre on Showing.MovieID=Genre.MovieID where Genre = %s order by TicketPrice")
    else:
        insert_stmt = ("select * from Showing join Genre on Showing.MovieID=Genre.MovieID where Genre = %s")

    data = (request.form.get('SelectedGenre'),)
    cursor.execute(insert_stmt, data)
    showings = cursor.fetchall()

    cnx.commit()
    cnx.close()
    return render_template("genresearch.html", showings=showings)

@front_blueprint.route("/front/submittitle", methods=['GET', 'POST'])
def titleSearch():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()

    query = ("select * from Showing join Movie on Showing.MovieID = Movie.MovieID where MovieName = %s")
    data = (request.form['MovieName'],)
    cursor.execute(query, data)
    showings = cursor.fetchall()

    cnx.commit()
    cnx.close()
    return render_template("titlesearch.html", showings=showings)

@front_blueprint.route("/front/submitdate", methods=['GET', 'POST'])
def dateSearch():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()

    query = ("select * from Showing where date(ShowingDateTime) between date(%s) and date(%s) group by ShowingDateTime")
    data = (request.form.get('StartDate'), request.form.get('EndDate'))
    cursor.execute(query,data)
    showings = cursor.fetchall()

    cnx.commit()
    cnx.close()
    return render_template("datesearch.html", showings=showings)

@front_blueprint.route("/front/submitshowings", methods=['GET', 'POST'])
def showingSearch():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()

    query = ("select *, COUNT(*) from Attend join Showing on Attend.ShowingID = Showing.ShowingID join Rooms on Showing.RoomNumber=Rooms.RoomNumber group by Attend.ShowingID having count(*)<Rooms.Capacity;")
    cursor.execute(query)
    showings = cursor.fetchall()

    cnx.commit()
    cnx.close()
    return render_template("showingsearch.html", showings=showings)


@front_blueprint.route("/front/attendshowing")
def attendShowingLoad():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()

    query = ("select * from Customer")
    cursor.execute(query)
    customers = cursor.fetchall()

    query = ("select ShowingID, ShowingDateTime, Movie.MovieName from Showing join Movie on Showing.MovieID = Movie.MovieID")
    cursor.execute(query)
    showings = cursor.fetchall()


    cursor.close()
    cnx.close()
    
    return render_template("attendshowing.html", customers=customers, showings=showings)


@front_blueprint.route("/front/submitattendshowing", methods=['GET','POST'])
def addAttendShowing():
    
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    insert_stmt = (
        "INSERT INTO Attend (CustomerID, ShowingID, Rating) "
        "VALUES (%s, %s, %s)"
    )

    cID = request.form.get('CustomerID')
    sID = request.form.get('ShowingID')


    data = (cID, request.form.get('ShowingID'), 'NULL')
    cursor.execute(insert_stmt, data)
    cnx.commit()
    cnx.close()
    return redirect(url_for('front.attendShowingLoad'))

@front_blueprint.route("/front/rateshowing")
def rateShowingLoad():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()

    query = ("select * from Customer")
    cursor.execute(query)
    customers = cursor.fetchall()

    query = ("select ShowingID, ShowingDateTime, Movie.MovieName from Showing join Movie on Showing.MovieID = Movie.MovieID")
    cursor.execute(query)
    showings = cursor.fetchall()


    cursor.close()
    cnx.close()
    
    return render_template("rateshowing.html", customers=customers, showings=showings)


@front_blueprint.route("/front/editrateshowing", methods=['GET','POST'])
def editRateShowing():
    
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    insert_stmt = (
        "UPDATE Attend SET Rating = %s WHERE CustomerID = %s AND ShowingID = %s"
    )


    data = (request.form['Rating'], request.form.get('CustomerID'), request.form.get('ShowingID'))
    cursor.execute(insert_stmt, data)
    cnx.commit()
    cnx.close()
    return redirect(url_for('front.rateShowingLoad'))


@front_blueprint.route("/front/ratedmovies")
def ratedMoviesLoad():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()

    query = ("select * from Customer")
    cursor.execute(query)
    customers = cursor.fetchall()

    cursor.close()
    cnx.close()
    
    return render_template("ratedmovies.html", customers=customers)


@front_blueprint.route("/front/showratedmovies", methods=['GET','POST'])
def showRatedMovies():
    
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    insert_stmt = (
        "select * from Attend join Showing on Attend.ShowingID=Showing.ShowingID join Movie on Showing.MovieID=Movie.MovieID where CustomerID=%s"
    )


    data = (request.form.get('CustomerID'),)
    cursor.execute(insert_stmt, data)
    movies = cursor.fetchall()
    
    cnx.commit()
    cnx.close()
    return render_template("showratedmovies.html", movies=movies, data=data)

@front_blueprint.route("/front/customerinfo")
def customerInfoLoad():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()

    query = ("select * from Customer")
    cursor.execute(query)
    customers = cursor.fetchall()

    cursor.close()
    cnx.close()
    
    return render_template("customerinfo.html", customers=customers)

@front_blueprint.route("/front/showcustomerinfo", methods=['GET','POST'])
def showCustomerInfo():
    
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    insert_stmt = ("select * from Customer where CustomerID=%s")
    data = (request.form.get('CustomerID'),)
    cursor.execute(insert_stmt,data)
    customers = cursor.fetchall()
    
    cnx.commit()
    cnx.close()
    return render_template("showcustomerinfo.html", customers=customers, data=data)
