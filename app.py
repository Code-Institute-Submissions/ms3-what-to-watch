import os
from flask import (
    Flask, flash, render_template,
    redirect, request, url_for)
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
    movies = mongo.db.movies.find().sort("rating", -1,).limit(5)
    genres = list(mongo.db.genres.find().sort("genre_name", 1))
    return render_template("public.html", movies=movies, genres=genres)


@app.route("/movies/all")
def get_movies():
    movies = list(mongo.db.movies.find().sort("genre_name", 1))
    genres = list(mongo.db.genres.find().sort("genre_name", 1))
    return render_template("movies.html", movies=movies, genres=genres)


@app.route("/movie/add", methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        mongo.db.movies.insert_one(request.form.to_dict())
        flash("You Have Added A Movie")

    genres = mongo.db.genres.find().sort("genre_name", 1)
    return render_template("add_movie.html", genres=genres)


@app.route("/movie/<movie_id>/edit", methods=["GET", "POST"])
def edit_movie(movie_id):
    if request.method == "POST":
        mongo.db.movies.update(
            {"_id": ObjectId(movie_id)}, request.form.to_dict())
        flash("You Have Updated A Movie Info")

    movie = mongo.db.movies.find_one({"_id": ObjectId(movie_id)})
    genres = mongo.db.genres.find().sort("genre_name", 1)
    return render_template("edit_movie.html", movie=movie, genres=genres)


@app.route("/movie/<movie_id>/delete")
def delete_movie(movie_id):
    mongo.db.movies.remove({"_id": ObjectId(movie_id)})
    flash("You Have Deleted A Movie")
    return redirect(url_for("get_home"))


@app.route("/genre/<genre_name>/movies")
def get_genre_movies(genre_name):
    movies = list(mongo.db.movies.find({"genre_name": genre_name}))
    return render_template(
        "genre_movies.html", genre_name=genre_name, movies=movies)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
