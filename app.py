# config
import datetime
import googlemaps
from flask import Flask, flash, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null

niewiem = False
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

API_KEY = "Kluczyk"
 
class Point:
    def __init__(self, id, name, coordinates):
        self.id = id
        self.name = name
        self.coordinates = coordinates

class Road:
    def __init__(self, id, origin_id, destination_id, distance):
        self.id = id
        self.origin_id = origin_id 
        self.destination_id = destination_id
        self.distance = distance


client = googlemaps.Client(API_KEY)

# ----------------------------------------------------------------

class Localizations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String, nullable=False)
    kordy = db.Column(db.String, nullable=False)

@app.route("/")
def index():
    query = Localizations.query.all()
    if len(query) == 0:
        query = "nie ma nic wariacie"
    nn = []
    return render_template("index.html", query=query, niewiem=niewiem)

@app.route("/delete")
def delete():
    fajnie = str(request.args['id'])
    Localizations.query.filter_by(id=fajnie).delete()
    db.session.commit()
    return redirect("/")


@app.route("/add", methods=["GET", "POST"])
def fajnie():
    if request.method == "POST":
        kordys = request.form["cords"]
        city_get = request.form["city"]
        new_task = Localizations(kordy=kordys, city=city_get)
        db.session.add(new_task)
        db.session.commit()
    return redirect("/")

roads_list = []
nieiwem = []

@app.route("/road")
def road():
    points = []
    query = Localizations.query.all()
    for i in query:
        kordynaty = i.kordy
        id = i.id
        city = i.city
        points.append(Point(id, city, kordynaty))
        roads = []
    for p in points:
        for destination in points:
            if p != destination:
                directions_result = client.directions(      origin= p.coordinates, 
                                                            destination=destination.coordinates, 
                                                            mode = "driving", 
                                                            avoid="ferries")

                distance =  directions_result[0]['legs'][0]['distance']
                roads.append(Road(1, p.id, destination.id, distance['value']))
    for i in points:
        print(i.name, i.coordinates)
    def fajnie(a, x, roads):
        for r in roads:
            if r.origin_id == a.id and r.destination_id == x.id:
                return r.distance

    def first(points):
        return next(iter(points))

    def nearest_neighbour(a, points):
        return min(points, key=lambda x: fajnie(a,x, roads))

    def nn_tour():
        start = first(points)
        tour = [start]
        unvisited = set(set(points) - {start})
        while unvisited: 
            c = nearest_neighbour(tour[-1], unvisited)
            tour.append(c)
            unvisited.remove(c)
        return tour

    nn = nn_tour()
    niewiem = True
    return render_template("index.html",query=query ,niewiem=niewiem, nn=nn)

if __name__ == '__main__':
    app.run(debug=True)