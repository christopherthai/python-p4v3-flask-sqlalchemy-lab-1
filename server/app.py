# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route("/")
def index():
    body = {"message": "Flask SQLAlchemy Lab 1"}
    return make_response(body, 200)


# Add views here
@app.route("/earthquakes/<int:id>")
def earthquake_by_id(id):
    earthquake = Earthquake.query.filter(Earthquake.id == id).first()

    if earthquake:
        body = earthquake.to_dict()
        status = 200
    else:
        body = {"message": f"Earthquake {id} not found."}
        status = 404

    return make_response(body, status)


# The route should have the form /earthquakes/magnitude/<float:magnitude>.
# The view should query the database to get all earthquakes having a magnitude greater than or equal to the parameter value, and return a JSON response containing the count of matching rows along with a list containing the data for each row.
@app.route("/earthquakes/magnitude/<float:magnitude>")
def earthquake_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    count = len(earthquakes)
    body = {
        "count": count,
        "quakes": [earthquake.to_dict() for earthquake in earthquakes],
    }
    return make_response(body, 200)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
