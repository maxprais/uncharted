import os
import webapp2
import jinja2
import random
from google.appengine.ext import ndb
import json


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Song(ndb.Model):

    id = ndb.IntegerProperty()
    song_title = ndb.StringProperty()
    song_id = ndb.StringProperty()
    user_name = ndb.StringProperty()
    user_id = ndb.StringProperty()
    user_image = ndb.StringProperty()
    song_image = ndb.StringProperty()
    song_url = ndb.StringProperty()
    likes = ndb.IntegerProperty()
    duration = ndb.StringProperty()
    sharing = ndb.StringProperty()
    genre = ndb.StringProperty()
    bpm = ndb.StringProperty()
    waveform_url = ndb.StringProperty()
    playback_count = ndb.StringProperty()



class SaveSong(webapp2.RequestHandler):

    def post(self):
        song_id = self.request.get('song-id')
        qry = Song.query(Song.song_id == song_id).fetch()

        if len(qry) == 0:
            id = self.request.get('id')
            song_title = self.request.get('song-title')
            song_id = self.request.get('song-id')
            user_name = self.request.get('user-name')
            user_id = self.request.get('user-id')
            user_image = self.request.get('user-image')
            song_image = self.request.get('song-image')
            song_url = self.request.get('song-url')
            sharing = self.request.get('sharing')
            genre = self.request.get('genre')
            bpm = self.request.get('bpm')
            waveform_url = self.request.get('waveform-url')
            playback_count = self.request.get('playback-count')
            duration = self.request.get('duration')

            new_song = Song()
            new_song.populate(id=int(id), song_title=song_title, song_id=song_id, user_name=user_name, user_id=user_id,
                              user_image=user_image, song_image=song_image, song_url=song_url, likes=0, sharing = sharing, genre = genre, bpm = bpm,
                              waveform_url = waveform_url, playback_count = playback_count, duration = duration)
            new_song.put()


class Player(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('pages/player.html')
        self.response.write(template.render())

class About(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('pages/about.html')
        self.response.write(template.render())

class Artist(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('pages/artist.html')
        self.response.write(template.render())

class UpdateSongLikes(webapp2.RequestHandler):

    def post(self):
        song_id = self.request.get('song-id')

        # find_song_qry = Song.query(Song.song_id == song_id)
        #likes = ndb.gql("SELECT likes FROM Song WHERE song_id = %s" % song_id )
        song = Song.query(Song.song_id == int(song_id)).fetch(1)[0]
        # likes = qry.likes + 1
        song.likes += 1
        song.put()


class GetSong(webapp2.RequestHandler):

    def get(self):
        all_songs = Song.query().fetch()
        size = len(all_songs)
        random_index = random.randint(0, size-1)
        qry = all_songs[random_index]

        # song_query = ndb.gql("SELECT song_id FROM Song where id=%s" % song_choice).fetch(1)
        # song_query = ndb.gql("SELECT song_id FROM Song LIMIT 1").fetch(1)

        self.response.headers['Content-Type'] = 'application/json'
        obj = { 'song_id': qry.song_id,
                'id': qry.id,
                'song_title': qry.song_title,
                'user_name': qry.user_name,
                'user_id': qry.user_id,
                'user_image': qry.user_image,
                'song_image': qry.song_image,
                'song_url': qry.song_url,
                'likes': qry.likes }
        self.response.out.write(json.dumps(obj))

class GetAllSongs(webapp2.RequestHandler):

    def get(self):
        qry = Song.query().fetch()
        songdict = []
        for song in qry:
            obj = { 'song_id': song.song_id,
                'id': song.id,
                'song_title': song.song_title,
                'user_name': song.user_name,
                'user_id': song.user_id,
                'user_image': song.user_image,
                'song_image': song.song_image,
                'song_url': song.song_url,
                'likes': song.likes }
            songdict.append(obj)

        self.response.out.write(json.dumps(songdict))


class RemoveSong(webapp2.RequestHandler):

    def post(self):
        song_id = self.request.get('song-id')
        qry = Song.query(Song.song_id == int(song_id)).fetch(1)[0]
        qry.key.delete()


class WorkAroundHandler(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('workaround.html')
        self.response.write(template.render())


class AdminPage(webapp2.RequestHandler):

    def post(self):
        password = self.request.get('password')

        if password == 'dothechanchan':
            self.response.out.write('true')
        else:
            self.response.out.write(json.dumps('false'))


    def get(self):
        template = JINJA_ENVIRONMENT.get_template('pages/admin.html')
        self.response.write(template.render())



app = webapp2.WSGIApplication([
    ('/', About),
    ('/radio', Player),
    ('/about', About),
    ('/artist', Artist),
    ('/song', GetSong),
    ('/allsongs', GetAllSongs),
    ('/admin', AdminPage),
    ('/likesong', UpdateSongLikes),
    ('/savesong', SaveSong),
    ('/removesong', RemoveSong),
    ('/populateDB', WorkAroundHandler)
], debug=True)

