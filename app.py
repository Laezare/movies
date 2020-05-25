from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask import render_template


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/movies'

db = SQLAlchemy(app)


class Movie(db.Model):
    __searchable__ = ['title', 'overview']
    __tablename__ = 'movies_metadata'
    adult = db.Column(db.Text)
    belongs_to_collection = db.Column(db.Text)
    budget = db.Column(db.Integer())
    genres = db.Column(db.Text)
    homepage = db.Column(db.Text)
    id = db.Column(db.Integer, primary_key=True)
    imdb_id = db.Column(db.Text)
    original_language = db.Column(db.Text)
    original_title = db.Column(db.Text)
    overview = db.Column(db.Text)
    popularity = db.Column(db.Float)
    poster_path = db.Column(db.Text)
    production_companies = db.Column(db.Text)
    production_countries = db.Column(db.Text)
    release_date = db.Column(db.Text)
    revenue = db.Column(db.Integer())
    runtime = db.Column(db.Float)
    spoken_languages = db.Column(db.Text)
    status = db.Column(db.Text)
    tagline = db.Column(db.Text)
    title = db.Column(db.Text)
    video = db.Column(db.Text)
    vote_average = db.Column(db.Float)
    vote_count = db.Column(db.Integer())

    def __init__(self, adult, belongs_to_collection, budget, genres, homepage, id, imdb_id, original_language, original_title, overview, popularity, poster_path, production_companies, production_countries, release_date, revenue, runtime, spoken_languages, status, tagline, title, video, vote_average, vote_count):
        self.adult = adult
        self.belongs_to_collection = belongs_to_collection
        self.budget = budget
        self.genres = genres
        self.homepage = homepage
        self.id = id
        self.imdb_id = imdb_id
        self.original_language = original_language
        self.original_title = original_title
        self.overview = overview
        self.popularity = popularity
        self.poster_path = poster_path
        self.production_companies = production_companies
        self.production_countries = production_countries
        self.release_date = release_date
        self.revenue = revenue
        self.runtime = runtime
        self.spoken_languages = spoken_languages
        self.status = status
        self.tagline = tagline
        self.title = title
        self.video = video
        self.vote_average = vote_average
        self.vote_count = vote_count


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('next'):
            popular_movies = Movie.query.order_by(Movie.vote_average.desc()).limit(5).all()
            recent_movies = Movie.query.order_by(Movie.release_date.desc()).limit(5).all()
            movies = Movie.query.order_by(func.rand()).limit(8)
            return render_template('index.html', pageTitle='Home', movies=movies, recent_movies=recent_movies,
                                   popular_movies=popular_movies)
        elif request.form.get('movie_id'):
            movie_id = request.form.get('movie_id')
            return redirect(url_for("detail", movie_id=movie_id))
    else:
        popular_movies = Movie.query.order_by(Movie.vote_average.desc()).limit(5).all()
        recent_movies = Movie.query.order_by(Movie.release_date.desc()).limit(5).all()
        movies = Movie.query.order_by(func.rand()).limit(8)
        return render_template('index.html', pageTitle='Home', movies=movies, recent_movies=recent_movies,
                               popular_movies=popular_movies)


@app.route('/movie<movie_id>', methods=['GET', 'POST'])
def detail(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()
    return render_template('movie.html', pageTitle='Détail', movie=movie)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        if request.form.get('movie_id'):
            movie_id = request.form.get('movie_id')
            return redirect(url_for("detail", movie_id=movie_id))
        else:
            form = request.form
            search_value = form['search_string']
            search = "%{0}%".format(search_value)
            if len(search) > 2:
                results = Movie.query.filter(Movie.title.like(search)).all()
                return render_template('search.html', pageTitle='Search', movies=results, search=search_value)
            else:
                return '<h1>Search function need more than 2 characters</h1>'
    else:
        return render_template('search.html', pageTitle='Search')


if __name__ == '__main__':
    app.run(debug=True)
