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

# **Add a form to the application in `SI364W18_HW2.py`, using `WTForms` syntax. The class name should be `AlbumEntryForm`.**
# The `AlbumEntryForm` should have the following fields:
#
# * Text entry for an album name, whose label should be `Enter the name of an album:`, which should be **required**
# * Radio buttons with options: 1,2,3 -- representing how much the user likes the album, whose label should be: `How much do you like this album? (1 low, 3 high)`, which should be **required**
# * A submit button

class AlbumEntryForm(FlaskForm):
    albumname = StringField('Enter the name of an album! ', validators=[Required()])
    like = RadioField('How much do you like this album? (1 low, 3 high)', choices=[('1','1'),('2','2'),('3','3')],validators=[Required()])
    submit = SubmitField('Submit')

####################
###### ROUTES ######
####################

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

@app.route('/album_entry')
def entryfunc():
    entryform = AlbumEntryForm()
    return render_template('album_entry.html', form=entryform)

@app.route('/album_result', methods = ['GET', 'POST'])
def resultfunc():
    form = AlbumEntryForm()
    if request.method == 'POST' and form.validate_on_submit(): #form has to validate in order for this to work
        final = form.albumname.data
        number = form.like.data
        return render_template('album_data.html', albumname=final, like=number)


# **Then, add 2 more routes to the application:**
#
# * `/album_entry`, which should render the WTForm you just created (note that there is a raw HTML form in
# one of the provided templates, but THIS should rely on your WTForms form). It should send data to a
# template called `album_entry.html` (see Part 3). The form should look pretty much [like this]
# (https://www.dropbox.com/s/6mvt6d4b929vu0n/Screenshot%202018-01-15%2016.10.09.png?dl=0) **when you are done with Part 3.**

# * `/album_result`, which should render the results of what was submitted to the
# `AlbumEntryForm`, [like this](https://www.dropbox.com/s/vqi7ybmkdh7ca1q/Screenshot%202018-01-15%2016.07.38.png?dl=0)
# **when you are done with Part 3.** It should send data to a template called `album_data.html` (see Part 3).


if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
