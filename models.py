import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
from config import heroku_db

database_name = "casting"
user = 'veronicakim'
host = 'localhost'
port = '5432'
database_path = "postgres://{}@{}:{}/{}".format(
    heroku_db['user'],
    heroku_db['host'],
    port,
    heroku_db['database_name'])

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


'''
Association table to join Movies with Actors
'''
association_table = db.Table('association',
                             Column('movie_id', db.Integer, db.ForeignKey(
                                 'Movie.id'), primary_key=True),
                             Column('actor_id', db.Integer, db.ForeignKey(
                                 'Actor.id'), primary_key=True)
                             )

'''
Movies
'''


class Movie(db.Model):
    __tablename__ = 'Movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(String)
    release_date = db.Column(db.DateTime())
    actors = db.relationship(
        'Actor',
        secondary=association_table,
        back_populates='movies'
    )

    # actors = db.relationship('Actor', secondary=association_table,
    #    backref=db.backref('movies', lazy=True))

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def addActor(self, actor):
        self.actors.append(actor)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': [actor.id for actor in self.actors]
        }


'''
Actors
'''


class Actor(db.Model):
    __tablename__ = 'Actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.CHAR)
    movies = db.relationship(
        'Movie',
        secondary=association_table,
        back_populates='actors'
    )

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def addMovie(self, movie):
        self.movies.append(movie)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': [movie.id for movie in self.movies]
        }


def addDummyData():
    movie0 = Movie(
        title="Avengers:Endgame",
        release_date=datetime(2019, 4, 26)
    )
    movie0.insert()
    movie0.update()

    movie1 = Movie(
        title="Parasite",
        release_date=datetime(2019, 10, 5)
    )
    movie1.insert()
    movie1.update()

    movie2 = Movie(
        title="Spider-Man: Far From Home",
        release_date=datetime(2019, 7, 2)
    )
    movie2.insert()
    movie2.update()

    movie3 = Movie(
        title="Titanic",
        release_date=datetime(1997, 12, 19)
    )
    movie3.insert()
    movie3.update()

    movie4 = Movie(
        title="Aladdin",
        release_date=datetime(2019, 5, 24)
    )
    movie4.insert()
    movie4.update()

    movie5 = Movie(
        title="Before Sunset",
        release_date=datetime(2004, 7, 2)
    )
    movie5.insert()
    movie5.update()

    movie6 = Movie(
        title="Harry Potter and the Deathly Hallows - Part I",
        release_date=datetime(2010, 11, 19)
    )
    movie6.insert()
    movie6.update()

    movie7 = Movie(
        title="Harry Potter and the Deathly Hallows - Part II",
        release_date=datetime(2011, 7, 15)
    )
    movie7.insert()
    movie7.update()

    movie8 = Movie(
        title="Home Alone",
        release_date=datetime(1990, 11, 16)
    )
    movie8.insert()
    movie8.update()

    movie9 = Movie(
        title="About Time",
        release_date=datetime(2013, 11, 1)
    )
    movie9.insert()
    movie9.update()

    movie10 = Movie(
        title="If Only",
        release_date=datetime(2004, 7, 15)
    )
    movie10.insert()
    movie10.update()

    movie11 = Movie(
        title="Avengers: Infinity War",
        release_date=datetime(2018, 4, 27)
    )
    movie11.insert()
    movie11.update()

    movie12 = Movie(
        title="Les Miserables",
        release_date=datetime(2012, 12, 25)
    )
    movie12.insert()
    movie12.update()

    actor = Actor(
        name="Jeremy Renner",
        age=49,
        gender="M"
    )
    actor.insert()
    actor.movies.append(movie0)
    actor.movies.append(movie11)
    actor.update()

    actor = Actor(
        name="Daniel Radcliffe",
        age=30,
        gender="M"
    )
    actor.insert()
    actor.movies.append(movie6)
    actor.movies.append(movie7)
    actor.update()

    actor = Actor(
        name="Tom Holland",
        age=23,
        gender="M"
    )
    actor.insert()
    actor.movies.append(movie0)
    actor.movies.append(movie2)
    actor.movies.append(movie11)
    actor.update()

    actor = Actor(
        name="Jennier Love Hewitt",
        age=41,
        gender="F"
    )
    actor.insert()
    actor.update()

    actor = Actor(
        name="Robert Downey Jr.",
        age=55,
        gender="M"
    )
    actor.insert()
    actor.movies.append(movie0)
    actor.movies.append(movie11)
    actor.update()

    actor = Actor(
        name="Chris Evans",
        age=38,
        gender="M"
    )
    actor.insert()
    actor.movies.append(movie0)
    actor.movies.append(movie11)
    actor.update()

    actor = Actor(
        name="Scarlett Johansson",
        age=35,
        gender="F"
    )
    actor.insert()
    actor.movies.append(movie0)
    actor.movies.append(movie11)
    actor.update()

    actor = Actor(
        name="Gwyneth Paltrow",
        age=47,
        gender="F"
    )
    actor.insert()
    actor.update()

    actor = Actor(
        name="Macaulay Culkin",
        age=39,
        gender="M"
    )
    actor.insert()
    actor.movies.append(movie8)
    actor.update()

    actor = Actor(
        name="Rupert Grint",
        age=31,
        gender="M"
    )
    actor.insert()
    actor.movies.append(movie6)
    actor.movies.append(movie7)
    actor.update()

    actor = Actor(
        name="Naomi Scott",
        age=27,
        gender="F"
    )
    actor.insert()
    actor.movies.append(movie4)
    actor.update()

    actor = Actor(
        name="Will Smith",
        age=51,
        gender="M"
    )
    actor.insert()
    actor.movies.append(movie4)
    actor.update()
