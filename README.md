# Full Stack Casting Agency Backend

This is the API for Casting Agency, where you can view the list of actors and movies and add, update and delete entries. 

# 
# Running the App Locally 
# 
### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

Working within a virtual environment is recommended whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, call the following function in config.py to drop and create the db:
  db_drop_and_create_all()
You may also add some dummy data using the following function in config.py:
  addDummyData()

## Running the server

From the directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to use the `app.py` file to find the application. 


# 
# API Documentation
# 

## Getting Started
- Base URL: The backend app is hosted at https://vj-casting-agency.herokuapp.com/
- Authentication: This app has three different roles with different permissions:
    - Casting Assistant
        - Has the same permissions as the general public with just the viewing permissions
        - Permissions:
            - GET /actors
            - GET /movies
    - Casting Director
        - Is able to add/remove/update actors and update movies in addition to all of the permissions a casting assistant has
        - Permissions:
            - POST /actors
            - DELETE /actors
            - PATCH /actors 
            - PATCH /movies
            - GET /actors
            - GET /movies
    - Executive Producer
        - Is able to add/remove movies in addition to all of the permissions a casting director has
        - Permissions:
            - POST /movies
            - DELETE /movies
            - GET /actors
            - GET /movies
            - POST /actors
            - DELETE /actors
            - PATCH /actors 
            - PATCH /movies


## Error Handling

- Errors are returned as JSON objects in the following format: 
    ```
    {
        "success": False, 
        "error": 404,
        "message": "Not found"
    }
    ```
- The API will return the following error types when requests fail:
    - 400: Bad Request
    - 401: unauthorized
    - 404: Resource not Found
    - 422: Unprocessable

## Resource Endpoint Library

- GET /movies
    - General: 
        - Returns a list of movies, success value, and total number of movies
        - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
    - Sample:
        - curl https://vj-casting-agency.herokuapp.com/movies
        ```
        {
            "movies": [
                {
                    "actors": [
                        1,
                        3,
                        5,
                        6,
                        7
                    ],
                    "id": 1,
                    "release_date": "Fri, 26 Apr 2019 00:00:00 GMT",
                    "title": "Avengers:Endgame"
                },
                {
                    "actors": [],
                    "id": 2,
                    "release_date": "Sat, 05 Oct 2019 00:00:00 GMT",
                    "title": "Parasite"
                }
            ],
            "success": true,
            "total_movies": 2
        }
        ```

- GET /actors
    - General: 
        - Returns a list of actors, success value, and total number of actors
        - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
    - Sample:
        - curl https://vj-casting-agency.herokuapp.com/actors
        ```
        {
            "actors": [
                {
                    "age": 49,
                    "gender": "M",
                    "id": 1,
                    "movies": [
                        1,
                        12
                    ],
                    "name": "Jeremy Renner"
                },
                {
                    "age": 30,
                    "gender": "M",
                    "id": 2,
                    "movies": [
                        7,
                        8
                    ],
                    "name": "Daniel Radcliffe"
                },
                {
                    "age": 23,
                    "gender": "M",
                    "id": 3,
                    "movies": [
                        1,
                        3,
                        12
                    ],
                    "name": "Tom Holland"
                }
            ],
            "success": true,
            "total_actors": 3
        }
        ```

- POST /movies
    - General:
        - Creates a new movie using the submitted title and release date
        - Returns the success value and the details of the movie that was just created
    - Sample:
        - curl --request POST 'https://vj-casting-agency.herokuapp.com/movies' --header 'Content-Type: application/json'
        --data-raw '{"title": "Harry Potter and the Half-Blood Prince" "date": "2009-07-15"}'
            ```
            {
                "movie": {
                    "actors": [],
                    "id": 14,
                    "release_date": "Wed, 15 Jul 2009 00:00:00 GMT",
                    "title": "Harry Potter and the Half-Blood Prince"
                },
                "success": true
            }
            ```

- POST /actors
    - General:
        - Creates a new actor using the submitted name, age, and gender info
        - Returns the success value and the details of the actor that was just added
    - Sample:
        - curl --request POST 'https://vj-casting-agency.herokuapp.com/actors' --header 'Content-Type: application/json'
        --data-raw '{"name": "Emma Watson", "age": 30, "gender": "F"}'
            ```
            {
                "actor": {
                    "age": 30,
                    "gender": "F",
                    "id": 13,
                    "movies": [],
                    "name": "Emma Watson"
                },
                "success": true
            }   
            ```

- DELETE /movies/{m_id}
    - General:
        - Deletes the movie of the given ID if it exists
        - Returns the id of the deleted movie, success value, the new total number of movies, and the list of movies based on current page number
    - Sample:
        - curl https://vj-casting-agency.herokuapp.com/movies/16 -X DELETE 
            ```
            "deleted": 17,
            "movies": [
                {
                    "actors": [
                        1,
                        3,
                        5,
                        6,
                        7
                    ],
                    "id": 1,
                    "release_date": "Fri, 26 Apr 2019 00:00:00 GMT",
                    "title": "Avengers:Endgame"
                },
                {
                    "actors": [],
                    "id": 2,
                    "release_date": "Sat, 05 Oct 2019 00:00:00 GMT",
                    "title": "Parasite"
                },
                {
                    "actors": [
                        3
                    ],
                    "id": 3,
                    "release_date": "Tue, 02 Jul 2019 00:00:00 GMT",
                    "title": "Spider-Man: Far From Home"
                }
            ],
            "success": true,
            "total_movies": 3
            }
            ```

- DELETE /actors/{a_id}
    - General:
        - Deletes the actor of the given ID if it exists. 
        - Returns the id of the deleted actor, success value, the new total number of actors, and the list of actors based on current page number
    - Sample:
        - curl https://vj-casting-agency.herokuapp.com/actors/14 -X DELETE 
            ```
        {
            "actors": [
                {
                    "age": 49,
                    "gender": "M",
                    "id": 1,
                    "movies": [
                        1,
                        12
                    ],
                    "name": "Jeremy Renner"
                },
                {
                    "age": 30,
                    "gender": "M",
                    "id": 2,
                    "movies": [
                        7,
                        8
                    ],
                    "name": "Daniel Radcliffe"
                }
            ],
            "deleted": 14,
            "success": true,
            "total_actors": 2
        }
            ```

- PATCH /movies/{m_id}
    - General:
        - Updates the movie with the given ID if it exists using the submitted information
        - Returns the success value and the details of the updated movie
    - Sample:
        - curl 'https://vj-casting-agency.herokuapp.com/movies/1' -X PATCH --header 'Content-Type: application/json' -d '{"title": "Avengers: Endgame"}'
        ```
        {
            "movie": {
                "actors": [
                    1,
                    3,
                    5,
                    6,
                    7
                ],
                "id": 1,
                "release_date": "Fri, 26 Apr 2019 00:00:00 GMT",
                "title": "Avengers: Endgame"
            },
            "success": true
        }
        ```
    
- PATCH /actors/{a_id}
    - General:
        - Updates the actor with the given ID if it exists using the submitted information
        - Returns the success value and the details of the updated actor
    - Sample:
        - curl 'https://vj-casting-agency.herokuapp.com/actors/5' -X PATCH --header 'Content-Type: application/json' -d '{"age":55}'
        ```
        {
            "actor": {
                "age": 55,
                "gender": "M",
                "id": 5,
                "movies": [
                    12,
                    1
                ],
                "name": "Robert Downey Jr."
            },
            "success": true
        }
        ```

- PATCH /movies/{m_id}/actors
    - General:
        - Adds the actor with the submitted ID to the movie with the given ID if both exist
        - Returns the success value and details on the movie that was just updated and the actor that was just added
    - Sample:
        - curl 'https://vj-casting-agency.herokuapp.com/movies/14/actors' -X PATCH --header 'Content-Type: application/json' -d '{"actor_id":2}'
        ```
        {
            "actor": {
                "age": 30,
                "gender": "M",
                "id": 2,
                "movies": [
                    7,
                    8,
                    14
                ],
                "name": "Daniel Radcliffe"
            },
            "movie": {
                "actors": [
                    2
                ],
                "id": 14,
                "release_date": "Wed, 15 Jul 2009 00:00:00 GMT",
                "title": "Harry Potter and the Half-Blood Prince"
            },
            "success": true
        }
        ```

- PATCH /actors/{a_id}/movies
    - General:
        - Adds the movie with the submitted ID to the actor with the given ID if both exist
        - Returns the success value and details on the actor that was just updated and the movie that was just added
    - Sample:
        - curl 'https://vj-casting-agency.herokuapp.com/actors/4/movies' -X PATCH --header 'Content-Type: application/json' -d '{"movie_id":11}'
        ```
        {
            "actor": {
                "age": 41,
                "gender": "F",
                "id": 4,
                "movies": [
                    11
                ],
                "name": "Jennier Love Hewitt"
            },
            "success": true
        }
        ```

## Testing
To run the tests, populate the database and run
```
python test_app.py
```
