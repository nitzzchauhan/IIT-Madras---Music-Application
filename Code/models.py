from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    user_id = db.Column(db.Integer, autoincrement=True, nullable=True, primary_key=True)
    user_name = db.Column(db.String(15), nullable=False)
    user_email = db.Column(db.String(15), unique=True, nullable=True)
    user_password = db.Column(db.String(15), nullable=True)
    ratings = db.relationship("Rating", backref="user", lazy=True)
    creators = db.relationship("Creator",backref="creators",lazy=True)


class Song(db.Model):
    song_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(20))
    artist = db.Column(db.String(30))
    genre = db.Column(db.String(40))
    album = db.Column(db.String(60))
    path = db.Column(db.String(20000))
    song_date = db.Column(db.DateTime, default=datetime.utcnow)
    # rating = db.Column(db.Integer)
    lyrics = db.Column(db.Text(), nullable=False)

    ratings = db.relationship("Rating", backref="song", lazy=True)
    PlaylistSongs = db.relationship("PlaylistSongs",backref="sSongs")
    album_songs = db.relationship("AlbumSong", backref='album', cascade="all, delete-orphan")


# Admin model
class Admin(db.Model):
    admin_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(15), nullable=False)


# Rating Model
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey("song.song_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)


# create Playlist
class Playlist(db.Model):
    Playlist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique= True)    
    PlaylistSongs = db.relationship("PlaylistSongs", backref="pSongs")
   
# create PlaylistSongs
class PlaylistSongs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.Playlist_id'),)
    song_id = db.Column(db.Integer, db.ForeignKey('song.song_id'),)

# C R E A T O R
class Creator(db.Model):
    creator_id = db.Column(db.Integer, autoincrement=True, nullable=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False, unique=True)
    


#C R E A T E A L B U M
class Album(db.Model):
    album_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('creator.creator_id'))
    title = db.Column(db.String(30), nullable=False, unique=True)   
    album_date = db.Column(db.DateTime, default=datetime.utcnow)
    Album_songs = db.relationship("AlbumSong", backref='albumsongs', cascade="all, delete-orphan")

#A L B U M S O N G
class AlbumSong(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.song_id'))
    album_id = db.Column(db.Integer, db.ForeignKey('album.album_id'))





    
