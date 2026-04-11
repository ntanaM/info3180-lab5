"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app
from flask import render_template, request, jsonify, send_file, send_from_directory
import os
from .models import Movies 
from .forms import MovieForm
from . import db
from werkzeug.utils import secure_filename
from flask_wtf.csrf import generate_csrf
from flask_cors import CORS


CORS(app, supports_credentials=True)


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@app.route('/api/v1/movies', methods=['POST'])
def movies():
    form = MovieForm()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        poster = form.poster.data

        # Upload poster image
        filename = secure_filename(poster.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        poster.save(upload_path)

        # Save movie to DB
        movie = Movies(
            title = title,
            description = description,
            poster = filename,
        )

        db.session.add(movie)
        db.session.commit()

        return jsonify({
            "message": "Movie Added Successfully",
            "title": title,
            "description": description,
            "poster": filename
        }), 201
    

    return jsonify({"errors": form_errors(form)}), 400


@app.route('/api/v1/movies', methods=['GET'])
def get_movies():

    try:
        movie_lst = Movies.query.all()
        movies = []

        for movie in movie_lst:
            m = {
                "id": movie.id,
                "title": movie.title,
                "description": movie.description,
                "poster": f"/api/v1/posters/{movie.poster}"
            }

            movies.append(m)

        return jsonify({"movies": movies}), 200
    
    except Exception as e:
        return jsonify({"errors": str(e)}), 400


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/api/v1/posters/<filename>')
def uploads(filename):
    #upload_folder = os.path.join(os.getcwd(), 'uploads')
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


#@app.errorhandler(404)
#def page_not_found(error):
 #   """Custom 404 page."""
  #  return render_template('404.html'), 404


if __name__ == "__main__":
    print("UPLOAD_FOLDER:", app.config.get('UPLOAD_FOLDER'))
    print("SECRET_KEY set:", bool(app.config.get('SECRET_KEY')))
    print("UPLOAD_FOLDER:", app.config.get('UPLOAD_FOLDER'))
    print("UPLOAD_FOLDER full path:", os.path.abspath(app.config.get('UPLOAD_FOLDER')))