## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.





#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests
import json

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################




####################
###### ROUTES ######
####################

## Edit the `SI364_HW3.py` file inside the `HW3Part1` directory to add routes to
## the basic Flask application that will match the **provided** templates in the
## `templates` subdirectory inside the `HW3Part1` folder.
#
# * `http://localhost:5000/artistform` -> `artistform.html`
# * `http://localhost:5000/artistinfo` -> `artist_info.html`
# * `http://localhost:5000/artistlinks` -> `artist_links.html`
# * `http://localhost:5000/specific/song/<artist_name>` -> `specific_artist.html`

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artistform')
def artistformfunc():
    return render_template('artistform.html')

@app.route('/artistinfo')
def infofunc():
    baseurl = "https://itunes.apple.com/search?"

    artist = request.args.get('artist',"")
    pdict = {'term': artist, 'entity' : 'musicTrack'}
    jsonf = requests.get(baseurl, params = pdict)
    loaded = json.loads(jsonf.text)['results']
    #print(loaded)
    return render_template('artist_info.html', objects=loaded)

@app.route('/artistlinks')
def linksfunc():
    return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>')
def specificsongfunc(artist_name):
    baseurl = "https://itunes.apple.com/search?"
    pdict = {'term': artist_name, 'entity' : 'musicTrack'}
    req = requests.get(baseurl, params=pdict)
    results = json.loads(req.text)
    final = results['results']
    # print(results)
    # print(final)
    return render_template('specific_artist.html', results=final)





if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
