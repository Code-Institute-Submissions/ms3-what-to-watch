# The code for app.py is from CI "Putting it all together" mini-project
import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def get_home():
    return render_template("public.html")


@app.route("/get_movies")
def get_movies():
    movies = list(mongo.db.movies.find())
    return render_template("movies.html", movies=movies)


@app.route("/add_movie", methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        mongo.db.movies.insert_one(request.form.to_dict())
        flash("You Have Added A Movie")
        return redirect("get_home")

    genres = mongo.db.genres.find().sort("genre_name", 1)
    return render_template("add_movie.html", genres=genres)


@app.route("/edit_movie/<movie_id>", methods=["GET", "POST"])
def edit_movie(movie_id):
    if request.method == "POST":
        mongo.db.movies.update(
            {"_id": ObjectId(movie_id)}, request.form.to_dict())
        flash("You Have Updated A Movie Info")

    movie = mongo.db.movies.find_one({"_id": ObjectId(movie_id)})
    genres = mongo.db.genres.find().sort("genre_name", 1)
    return render_template("edit_movie.html", movie=movie, genres=genres)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
