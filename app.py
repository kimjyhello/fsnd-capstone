import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Actor, Movie, addDummyData, db_drop_and_create_all
from auth import AuthError, requires_auth
from datetime import datetime

RESULTS_PER_PAGE = 10

'''
Helper to paginate movies and actors
'''
def paginate_result(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * RESULTS_PER_PAGE
  end = start + RESULTS_PER_PAGE

  results = [result.format() for result in selection]
  current_list = results[start:end]

  return current_list


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  #db_drop_and_create_all()
  #addDummyData()

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
    return response

  '''
  Endpoint to handle GET requests 
  for all available movies
  '''
  @app.route('/movies')
  def get_movies():
    selection = Movie.query.all()
    current_page = paginate_result(request, selection)

    if len(current_page) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'movies': current_page,
      'total_movies': len(selection)
    }), 200

  '''
  Endpoint to handle GET requests 
  for all available actors
  '''
  @app.route('/actors')
  def get_actors():
    selection = Actor.query.all()
    current_page = paginate_result(request, selection)

    if len(current_page) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'actors': current_page,
      'total_actors': len(selection)
    }), 200


  '''
  Endpoint to handle DELETE requests
  for movie with movie_id
  '''
  @app.route('/movies/<int:m_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, m_id):
    errorcode = 0
    try:
      movie = Movie.query.get(m_id)

      if movie is None:
        errorcode = 404

      if errorcode == 0:
        movie.delete()
        selection = Movie.query.order_by(Movie.id).all()
        current_page = paginate_result(request, selection)

    except:
      errorcode = 422
    finally:
      if errorcode != 0:
        abort(errorcode)
      else:
        return jsonify({
          'success': True,
          'deleted': m_id,
          'movies': current_page,
          'total_movies': len(selection)
        }), 200


  '''
  Endpoint to handle DELETE requests
  for actor with actor_id
  '''
  @app.route('/actors/<int:a_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, a_id):
    errorcode = 0

    try:
      actor = Actor.query.get(a_id)

      if actor is None:
        errorcode = 404

      if errorcode == 0:
        actor.delete()
        selection = Actor.query.order_by(Actor.id).all()
        current_page = paginate_result(request, selection)
    except:
      errorcode = 422
    finally:
      if errorcode > 0:
        abort(errorcode)
      else:
        return jsonify({
          'success': True,
          'deleted': a_id,
          'actors': current_page,
          'total_actors': len(selection)
        }), 200


  '''
  Endpoint to handle POST requests
  for a new movie
  '''
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def add_movie(payload):
    body = request.get_json()
    errorcode = 0
    try:
      title = body.get('title', None)
      dateraw = body.get('date', None)

      if title is None or dateraw is None:
        errorcode = 400
      if title == '':
        errorcode = 400
      if dateraw == '':
        errorcode = 400

      if errorcode == 0:
        date = datetime.strptime(dateraw, '%Y-%m-%d')

        movie = Movie(
          title=title,
          release_date=date
        )
        movie.insert()
        movie.update()
    except:
      errorcode = 422
    finally:
      if errorcode != 0:
        abort(errorcode)
      else:
        return jsonify({
          'success': True,
          'movie': movie.format()
        }), 200

  '''
  Endpoint to handle POST requests
  for a new actor
  '''
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def add_actor(payload):
    body = request.get_json()
    errorcode = 0
    try:
      name = body.get('name', None)
      age = body.get('age', None)
      gender = body.get('gender', None)

      if name is None or age is None or gender is None:
        errorcode = 400
      elif name == '':
        errorcode = 400
      elif age == '':
        errorcode = 400
      elif len(gender) != 1:
        errorcode = 400

      if errorcode == 0:
        actor = Actor(
          name=name,
          age=age,
          gender=gender
        )
        
        actor.insert()
        actor.update()
    except:
      errorcode = 422
    finally:
      if errorcode != 0:
        abort(errorcode)
      else:
        return jsonify({
          'success': True,
          'actor': actor.format()
        }), 200


  '''
  Endpoint to handle PATCH requests
  for movie with movie_id
  '''
  @app.route('/movies/<int:m_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(payload, m_id):
    movie = Movie.query.get(m_id)

    errorcode = 0

    if movie is None:
      abort(404)
    body = request.get_json()

    try:
      title = body.get('title', None)
      dateraw = body.get('date', None)

      if title is not None and title != '':
        movie.title = title
      if dateraw is not None and dateraw != '':
        date = datetime.strptime(dateraw, '%Y-%m-%d')
        movie.release_date = date

      movie.update()
    except:
      errorcode = 422
    finally:
      if errorcode != 0:
        abort(errorcode)
      else:
        return jsonify({
          'success': True,
          'movie': movie.format()
        }), 200

  '''
  Endpoint to handle PATCH requests
  for actor with actor_id
  '''
  @app.route('/actors/<int:a_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(payload, a_id):
    actor = Actor.query.get(a_id)

    errorcode = 0

    if actor is None:
      abort(404)

    body = request.get_json()

    try:
      name = body.get('name', None)
      age = body.get('age', None)
      gender = body.get('gender', None)

      if name is not None and name != '':
        actor.name = name
      if age is not None and age != '':
        actor.age = age
      if gender is not None and gender != '':
        actor.gender = gender

      actor.update()

    except:
      errorcode = 422
    finally:
      if errorcode != 0:
        abort(errorcode)
      else:
        return jsonify({
          'success': True,
          'actor': actor.format()
        }), 200


  '''
  Endpoint to handle PATCH requests
  to add an actor to movie with movie_id
  '''
  @app.route('/movies/<int:m_id>/actors', methods=['PATCH'])
  @requires_auth('patch:movies')
  def add_actor_to_movie(payload, m_id):
    movie = Movie.query.get(m_id)

    errorcode = 0

    if movie is None:
      abort(404)
    body = request.get_json()

    try:
      a_id = body.get('actor_id', None)
      if a_id is None:
        errorcode = 400
      elif a_id == '':
        errorcode = 400

      actor = Actor.query.get(a_id)

      if actor is None:
        errorcode = 404

      if errorcode == 0:
        movie.actors.append(actor)
        movie.update()
    except:
      errorcode = 422
    finally:
      if errorcode != 0:
        abort(errorcode)
      else:
        return jsonify({
          'success': True,
          'movie': movie.format(),
          'actor': actor.format()
        }), 200

  
  '''
  Endpoint to handle PATCH requests
  to add a movie to actor with actor_id
  '''
  @app.route('/actors/<int:a_id>/movies', methods=['PATCH'])
  @requires_auth('patch:actors')
  def add_movie_to_actor(payload, a_id):
    actor = Actor.query.get(a_id)

    errorcode = 0

    if actor is None:
      abort(404)
    body = request.get_json()

    try:
      m_id = body.get('movie_id', None)
      if m_id is None:
        errorcode = 400
      elif m_id == '':
        errorcode = 400
      movie = Movie.query.get(m_id)

      if movie is None:
        errorcode = 404

      if errorcode == 0:
        actor.movies.append(movie)
        actor.update()
    except:
      errorcode = 422
    finally:
      if errorcode != 0:
        abort(errorcode)
      else:
        return jsonify({
          'success': True,
          'actor': actor.format()
        }), 200


  '''
  Error Handlers
  '''

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'Bad Request'
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'Resource not found'
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'Unprocessable'
    }), 422

  @app.errorhandler(401)
  def unauthorized(error):
    return jsonify({
      'success': False,
      'error': 401,
      'message': 'unauthorized'
    }), 401

  @app.errorhandler(AuthError)
  def auth_error(e):
    return jsonify({
      'success': False,
      'error': e.status_code,
      'code': e.error['code'],
      'message': e.error['description']
    }), e.status_code

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)