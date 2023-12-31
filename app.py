#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import sys
import dateutil.parser
import babel
from flask import (
  Flask,
  render_template,
  request, flash,
  redirect, url_for
  )


from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from forms import *

from flask_migrate import Migrate
from datetime import datetime

from models import db, Artist, Venue, Show
from config import SQLALCHEMY_DATABASE_URI

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
moment = Moment(app)
db.init_app(app)
app.secret_key = "FSND_2023@Udacity"

migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  # Retrieve the 10 most recently listed artists
  recent_artists = Artist.query.order_by(Artist.id.desc()).limit(10).all()
  
  # Retrieve the 10 most recently listed venues
  recent_venues = Venue.query.order_by(Venue.id.desc()).limit(10).all()
  
  return render_template('pages/home.html', recent_artists=recent_artists, recent_venues=recent_venues)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  
  # data=[{
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "venues": [{
  #     "id": 1,
  #     "name": "The Musical Hop",
  #     "num_upcoming_shows": 0,
  #   }, {
  #     "id": 3,
  #     "name": "Park Square Live Music & Coffee",
  #     "num_upcoming_shows": 1,
  #   }]
  # }, {
  #   "city": "New York",
  #   "state": "NY",
  #   "venues": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }]
  
  
  # Query the database to fetch venue information
  venues = Venue.query.all()

  # Create a data structure to store the venue information
  data = []
  cities = set()

  for venue in venues:
      city_state = (venue.city, venue.state)

      if city_state not in cities:
          cities.add(city_state)
          data.append({
              "city": venue.city,
              "state": venue.state,
              "venues": []
          })

      # Find the city index in the data list
      city_index = next((index for index, item in enumerate(data) if item["city"] == venue.city and item["state"] == venue.state), None)


      if city_index is not None:
          data[city_index]["venues"].append({
              "id": venue.id,
              "name": venue.name
          })

  return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  
  search_term = request.form.get('search_term', '')
  
  # Retrieve the search results
  results = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()

  # Prepare the data for rendering
  response = {
    'count': len(results),
    'data': results
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  
  # data1={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #   "past_shows": [{
  #     "artist_id": 4,
  #     "artist_name": "Guns N Petals",
  #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 2,
  #   "name": "The Dueling Pianos Bar",
  #   "genres": ["Classical", "R&B", "Hip-Hop"],
  #   "address": "335 Delancey Street",
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "914-003-1132",
  #   "website": "https://www.theduelingpianos.com",
  #   "facebook_link": "https://www.facebook.com/theduelingpianos",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 3,
  #   "name": "Park Square Live Music & Coffee",
  #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
  #   "address": "34 Whiskey Moore Ave",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "415-000-1234",
  #   "website": "https://www.parksquarelivemusicandcoffee.com",
  #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #   "past_shows": [{
  #     "artist_id": 5,
  #     "artist_name": "Matt Quevedo",
  #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [{
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 1,
  # }

  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  
  # Retrieve venue data from the database
  venue = Venue.query.get(venue_id)

  # Retrieve upcoming shows for the venue
  current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
  upcoming_shows = db.session.query(Show.c.start_time, Artist.id, Artist.name, Artist.image_link). \
    join(Artist).filter(Show.c.venue_id == venue_id, Show.c.start_time > current_time).all()

  # Retrieve past shows for the venue
  past_shows = db.session.query(Show.c.start_time, Artist.id, Artist.name, Artist.image_link). \
    join(Artist).filter(Show.c.venue_id == venue_id, Show.c.start_time < current_time).all()

  # Convert the retrieved shows into the required format
  upcoming_shows_data = []
  past_shows_data = []

  for show_time, artist_id, artist_name, artist_image_link in upcoming_shows:
      show_data = {
          'artist_id': artist_id,
          'artist_name': artist_name,
          'artist_image_link': artist_image_link,
          'start_time': show_time
      }
      upcoming_shows_data.append(show_data)

  for show_time, artist_id, artist_name, artist_image_link in past_shows:
      show_data = {
        'artist_id': artist_id,
        'artist_name': artist_name,
        'artist_image_link': artist_image_link,
        'start_time': show_time
    }
      past_shows_data.append(show_data)

  # Prepare the venue data for rendering
  venue_data = {
    'id': venue.id,
    'name': venue.name,
    'genres': venue.genres,
    'address': venue.address,
    'city': venue.city,
    'state': venue.state,
    'phone': venue.phone,
    'website': venue.website_link,
    'facebook_link': venue.facebook_link,
    'seeking_talent': venue.seeking_talent,
    'seeking_description': venue.seeking_description,
    'image_link': venue.image_link,
    'website_link': venue.website_link,
    'past_shows': past_shows_data,
    'upcoming_shows': upcoming_shows_data,
    'past_shows_count': len(past_shows_data),
      'upcoming_shows_count': len(upcoming_shows_data)
  }
  return render_template('pages/show_venue.html', venue=venue_data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  
  try:
    form = VenueForm(request.form)

    if form.validate():
      name = form.name.data
      city = form.city.data
      state = form.state.data
      address = form.address.data
      phone = form.phone.data
      genres = form.genres.data
      image_link = form.image_link.data
      facebook_link = form.facebook_link.data
      website_link = form.website_link.data
      seeking_talent  = form.seeking_talent.data
      seeking_description  = form.seeking_description.data
    
      venue = Venue(name=name, city=city, state=state, address=address, phone=phone,genres=genres,
        image_link=image_link, facebook_link=facebook_link, website_link=website_link,
        seeking_talent=seeking_talent, seeking_description=seeking_description)
      
      db.session.add(venue)
      db.session.commit()

      # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    else:
      # Handle form validation errors
      print(sys.exc_info())
      flash(form.errors)
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  finally:
    db.session.close()
  return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['POST', 'DELETE'])
def delete_venue(venue_id):
  
  if request.method == 'POST' or request.method == 'DELETE':
    venue = Venue.query.get(venue_id)
    if not venue:
      print(sys.exc_info())
      flash('Venue not found.')
      return redirect(url_for('index'))
    try:
      db.session.delete(venue)
      db.session.commit()
      # on successful db insert, flash success
      flash('Venue successfully deleted.')
    except:
      db.session.rollback()
      # on unsuccessful db insert, flash an error instead.
      print(sys.exc_info())
      flash('An error occurred. Venue could not be deleted')
    finally:
      db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------

@app.route('/artists')
def artists():
  artists = Artist.query.all()
  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]
  return render_template('pages/artists.html', artists=artists)


@app.route('/artists/search', methods=['POST'])
def search_artists():
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  
  search_term = request.form.get('search_term', '')
  
  # Retrieve the search results
  results = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()

  # Prepare the data for rendering
  response = {
    'count': len(results),
    'data': results
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  
  # data1={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "past_shows": [{
  #     "venue_id": 1,
  #     "venue_name": "The Musical Hop",
  #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 5,
  #   "name": "Matt Quevedo",
  #   "genres": ["Jazz"],
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "300-400-5000",
  #   "facebook_link": "https://www.facebook.com/mattquevedo923251523",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "past_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  #   "genres": ["Jazz", "Classical"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "432-325-5432",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 3,
  # }
  # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  
  # Retrieve artist data from the database
  artist = Artist.query.get(artist_id)

  current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
  
  # Retrieve upcoming shows for the artist
  upcoming_shows = db.session.query(Show.c.start_time, Venue.id, Venue.name, Venue.image_link). \
    join(Venue).filter(Show.c.artist_id == artist_id, Show.c.start_time > current_time).all()

  # Retrieve past shows for the artist
  past_shows = db.session.query(Show.c.start_time, Venue.id, Venue.name, Venue.image_link). \
    join(Venue).filter(Show.c.artist_id == artist_id, Show.c.start_time < current_time).all()

  # Convert the retrieved shows into the required format
  upcoming_shows_data = []
  past_shows_data = []

  for show_time, venue_id, venue_name, venue_image_link in upcoming_shows:
      show_data = {
        'venue_id': venue_id,
        'venue_name': venue_name,
        'venue_image_link': venue_image_link,
        'start_time': show_time
      }
      upcoming_shows_data.append(show_data)

  for show_time, venue_id, venue_name, venue_image_link in past_shows:
      show_data = {
        'venue_id': venue_id,
        'venue_name': venue_name,
        'venue_image_link': venue_image_link,
        'start_time': show_time
      }
      past_shows_data.append(show_data)

  # Prepare the artist data for rendering
  artist_data = {
      'id': artist.id,
      'name': artist.name,
      'genres': artist.genres,
      'city': artist.city,
      'state': artist.state,
      'phone': artist.phone,
      'website': artist.website_link,
      'facebook_link': artist.facebook_link,
      'seeking_venue': artist.seeking_venue,
      'seeking_description': artist.seeking_description,
      'image_link': artist.image_link,
      'website_link': artist.website_link,
      'past_shows': past_shows_data,
      'upcoming_shows': upcoming_shows_data,
      'past_shows_count': len(past_shows_data),
      'upcoming_shows_count': len(upcoming_shows_data)
  }
  return render_template('pages/show_artist.html', artist=artist_data)


#  Update
#  ----------------------------------------------------------------

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  form = ArtistForm(request.form, artist)
  # artist={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }
  return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # artist record with ID <artist_id> using the new attributes
  try:
    artist = Artist.query.get(artist_id)
    form = ArtistForm(request.form, obj=artist)
    
    if form.validate():
      # Set default values for nullable fields if empty
      form.populate_obj(artist)
      db.session.commit()
      # on successful flash success
      flash('Artist info updated successfully!')
    else:
      # Handle form validation errors
      print(sys.exc_info())
      flash(form.errors)
  except:
    db.session.rollback()
    # on unsuccessful flash success
    print(sys.exc_info())
    flash('An error occurred when trying to update Artist Info!')
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(request.form, venue)
  # venue={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  # }
  return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # venue record with ID <venue_id> using the new attributes
  try:
    venue = Venue.query.get(venue_id)
    form = VenueForm(request.form, obj=venue)
    if form.validate():
      form.populate_obj(venue)
      db.session.commit()
      # on successful flash success
      flash('Venue info updated successfully!')
    else:
      # Handle form validation errors
      print(sys.exc_info())
      flash(form.errors)
  except:
    db.session.rollback()
    # on unsuccessful flash success
    print(sys.exc_info())
    flash('An error occured when try to update Venue Info!')
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  try:
    form = ArtistForm(request.form)

    if form.validate():
      name = form.name.data
      city = form.city.data
      state = form.state.data
      phone = form.phone.data
      genres = form.genres.data 
      image_link = form.image_link.data
      facebook_link = form.facebook_link.data
      website_link = form.website_link.data
      seeking_venue = form.seeking_venue.data
      seeking_description = form.seeking_description.data
    
      artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres,
        image_link=image_link, facebook_link=facebook_link, website_link=website_link,
        seeking_venue=seeking_venue, seeking_description=seeking_description)
      
      db.session.add(artist)
      db.session.commit()

      # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    else:
      # Handle form validation errors
      print(sys.exc_info())
      flash(form.errors)
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  finally:
    db.session.close()
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # Retrieve data from the show table
  shows = db.session.query(
      Artist.image_link.label('artist_image_link'),
      Show.c.start_time,
      Artist.name.label('artist_name'),
      Venue.name.label('venue_name'),
      Show.c.artist_id,
      Show.c.venue_id
    ).join(Show, Venue.id == Show.c.venue_id).join(Artist, Artist.id == Show.c.artist_id).all()
  
  # data=[{
  #   "venue_id": 1,
  #   "venue_name": "The Musical Hop",
  #   "artist_id": 4,
  #   "artist_name": "Guns N Petals",
  #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "start_time": "2019-05-21T21:30:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 5,
  #   "artist_name": "Matt Quevedo",
  #   "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "start_time": "2019-06-15T23:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-01T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-08T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-15T20:00:00.000Z"
  # }]
  return render_template('pages/shows.html', shows=shows)


@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form  
  try:
    form = ShowForm(request.form)
    
    if form.validate():
      insert_statement = Show.insert().values(
        venue_id=form.venue_id.data,
        artist_id=form.artist_id.data,
        start_time=form.start_time.data
      )
      db.session.execute(insert_statement)
      db.session.commit()
      # on successful db insert, flash success
      flash('Show was successfully listed!')
    else:
      # Handle form validation errors
      print(sys.exc_info())
      flash(form.errors)
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  finally:
    db.session.close()
  return render_template('pages/home.html')


@app.errorhandler(400)
def server_error(error):
  return render_template('errors/400.html'), 400

@app.errorhandler(401)
def server_error(error):
  return render_template('errors/401.html'), 401

@app.errorhandler(403)
def server_error(error):
  return render_template('errors/403.html'), 403

@app.errorhandler(404)
def not_found_error(error):
  return render_template('errors/404.html'), 404

@app.errorhandler(405)
def not_found_error(error):
  return render_template('errors/405.html'), 405

@app.errorhandler(409)
def not_found_error(error):
  return render_template('errors/409.html'), 409

@app.errorhandler(422)
def not_found_error(error):
  return render_template('errors/422.html'), 422

@app.errorhandler(500)
def server_error(error):
  return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
      Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
  app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
'''