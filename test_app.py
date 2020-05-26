import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from app import create_app
from models import setup_db, Actor, Movie

from datetime import datetime

from config import jwt

class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        """ Define test variables and initialize app """
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'casting'
        self.database_path = "postgres://{}@{}/{}".format('veronicakim', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.casting_assistant = jwt['casting_assistant']
        self.casting_director = jwt['casting_director']
        self.executive_producer = jwt['executive_producer']

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            self.db.create_all

    def tearDown(self):
        """ Executed after each test """
        pass

    '''
    Tests for GET /actors
    '''
    def test_get_paginated_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_get_paginated_actors_with_page_number(self):
        res = self.client().get('/actors?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_get_paginated_actors_with_page_number_casting_director(self):
        res = self.client().get('/actors?page=1',
            headers={
                'Authorization':'Bearer {}'.format(
                    self.casting_director
            )})
        
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_404_get_paginated_actors_beyond_valid_page(self):
        res = self.client().get('/actors?page=200')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Resource not found')

    '''
    Tests for GET /movies
    '''
    def test_get_paginated_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_get_paginated_movies_with_page_number(self):
        res = self.client().get('/movies?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_get_paginated_movies_with_page_number_exec_prod(self):
        res = self.client().get('/movies?page=1',
            headers={
                'Authorization':'Bearer {}'.format(
                    self.executive_producer
                )})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_404_get_paginated_movies_beyond_valid_page(self):
        res = self.client().get('/movies?page=200')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Resource not found')

    '''
    Tests for DELETE /actors
    '''
    def test_delete_actor_casting_director(self):
        res = self.client().delete('/actors/2',
            headers={
                'Authorization':'Bearer {}'.format(
                    self.casting_director
                )})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_delete_actor_casting_assistant(self):
        res = self.client().delete('/actors/4',
            headers={
                'Authorization':'Bearer {}'.format(
                    self.casting_assistant
                )})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'Not authorized for the current user')

    def test_404_delete_actor_exec_prod_nonexistant_actor(self):
        res = self.client().delete('/actors/999',
            headers={
                'Authorization':'Bearer {}'.format(
                    self.executive_producer
                )})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Resource not found')

    '''
    Tests for DELETE /movies
    '''
    def test_delete_movie_exec_prod(self):
        res = self.client().delete('/movies/2',
            headers={
                'Authorization':'Bearer {}'.format(
                    self.executive_producer
                )})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_delete_movie_casting_director(self):
        res = self.client().delete('/movies/1',
            headers={
                'Authorization':'Bearer {}'.format(
                    self.casting_director
                )})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'Not authorized for the current user')

    def test_404_delete_movie_exec_prod_nonexistant_movie(self):
        res = self.client().delete('/movies/999',
            headers={
                'Authorization':'Bearer {}'.format(
                    self.executive_producer
                )})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Resource not found')

    '''
    Tests for POST /actors
    '''
    def test_post_actor_casting_director(self):
        res = self.client().post('/actors',
            json={
                'name':'Emma Watson',
                'age':30,
                'gender':'F'
            },
            headers={
                'Authorization':'Bearer {}'.format(
                    self.casting_director
            )})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_post_actor_exec_prod_missing_fields(self):
        res = self.client().post('/actors',
            json={
                'name':'Will Smith'
            },
            headers={
                'Authorization':'Bearer {}'.format(
                    self.executive_producer
            )})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_401_post_actor_casting_assistant(self):
        res = self.client().post('/actors',
            json={
                'name':"I should'nt be added",
                'age':24,
                'gender':'M'
            },
            headers={
                'Authorization':'Bearer {}'.format(
                    self.casting_assistant
            )})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not authorized for the current user')


    '''
    Tests for POST /movies
    '''
    def test_post_movie_exec_prod(self):
        res = self.client().post('/movies',
            json={
                'title':'Avengers: Endgame',
                'date':'2019-04-26'
            },
            headers={
                'Authorization':'Bearer {}'.format(
                    self.executive_producer
            )})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_post_movie_exec_prod_missing_fields(self):
        res = self.client().post('/movies',
            json={
                'name':'Titanic'
            },
            headers={
                'Authorization':'Bearer {}'.format(
                    self.executive_producer
            )})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_401_post_movie_casting_director(self):
        res = self.client().post('/movies',
            json={
                'title':'Frozen',
                'date': '2013-11-27'
            },
            headers={
                'Authorization':'Bearer {}'.format(
                    self.casting_director
            )})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not authorized for the current user')


    '''
    Tests for PATCH /actors
    '''
    def test_patch_actor_exec_prod(self):
        res = self.client().patch('/actors/3',
            json={
                'age':29
            },
            headers={
                'Authorization':'Bearer {}'.format(
                    self.executive_producer
            )})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_401_patch_actor_casting_assistant(self):
        res = self.client().patch('/actors/2',
            json={
                'age':30
            },
            headers={
                'Authorization':'Bearer {}'.format(
                    self.casting_assistant
            )})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not authorized for the current user')

    def test_404_patch_actor_casting_director_nonexistant_actor(self):
        res = self.client().patch('/actors/99',
            json={
                'age':19
            },
            headers={
                'Authorization':'Bearer {}'.format(
                    self.casting_director
            )})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    '''
    Tests for PATCH /movies
    '''
    def test_patch_movie_casting_director(self):
        res = self.client().patch('/movies/3',
            json={
                'release_date': datetime(1988, 3, 11)
            },
            headers={
                'Authorization':'Bearer {}'.format(
                    self.casting_director
            )})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_patch_movie_casting_assistant(self):
        res = self.client().patch('/movies/2',
            json={
                'title': 'ChangeMe'
            },
            headers={
                'Authorization':'Bearer {}'.format(
                    self.casting_assistant
            )})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not authorized for the current user')

    def test_404_patch_movie_casting_director_nonexistant_actor(self):
        res = self.client().patch('/movies/99',
            json={
                'title': 'NewMovie'
            },
            headers={
                'Authorization':'Bearer {}'.format(
                    self.casting_director
            )})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

if __name__ == "__main__":
    unittest.main()
