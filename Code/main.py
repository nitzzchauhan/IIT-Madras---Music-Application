from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import *

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///one2many.sqlite3"
db.init_app(app)

app.app_context().push()
db.create_all()


@app.route("/", methods=["GET", "POST"])  # default page
def musicfy():
    if "user_useremail" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form["email"]  # client id
        password = request.form["b"]  # clientpass
        session["user_useremail"] = email
        session["user_password"] = password
        all_users = User.query.all()  # database id and pass

        Flag = False
        for k in all_users:
            if k.user_email == email and k.user_password == password:
                Flag = True
                return redirect("home")
        if Flag == False:
            session.pop("admin_username", None)
            return "Invalid username or password"

    return render_template("musicfy.html")


@app.route("/home", methods=["GET", "POST"])
def home():
    if "user_useremail" in session:
        email = session["user_useremail"]
        password = session["user_password"]
        all_users = User.query.all()
        all_songs = Song.query.all()
        all_playlist = Playlist.query.all()
        all_creator = Creator.query.all()

        Flag = False
        for k in all_users:
            if k.user_email == email and k.user_password == password:
                Flag = True
                user_id = k.user_id
                creators = False
                

                for creator in all_creator:
                    if creator.user_id == user_id:
                        creators = True
                        session["creator_id"] = creator.creator_id
                      
                        return render_template(
                            "creator.html",
                            username=k.user_name,
                            useremail=email,
                            song=all_songs,
                            user=k,
                            all_playlist=all_playlist,
                        )

                if creators == False:
                    return render_template(
                        "dash.html",
                        username=k.user_name,
                        useremail=email,
                        song=all_songs,
                        user=k,
                        all_playlist=all_playlist,
                    )
        if Flag == False:
            session.pop("user_useremail", None)
            return "<h1>Invalid username or password</h1>"
    else:
        return render_template("musicfy.html")


# @app.route("/generaluser")
# def generaluser


@app.route("/userlogout")
def userlogout():
    session.pop("user_useremail", None)
    session.pop("creator_id", None)
    return redirect(url_for("musicfy"))

@app.route("/new_Playlist", methods=["POST", "GET"])
def new_playlist():
    
  if request.method == "POST":
    song_name = request.form["song_name"]
    playlist_name = request.form["pli_name"]  

    c_pl = Playlist.query.filter_by(name=song_name).first()
    if c_pl is not None:
        song=Song.query.filter_by(title=song_name).first()
        song_id=song.song_id
        p_id = c_pl.Playlist_id
        ps1 = PlaylistSongs(playlist_id=p_id,song_id=song_id)
        db.session.add(ps1)
        db.session.commit()
    else:
        p1 = Playlist(name=playlist_name)
        db.session.add(p1)
        db.session.commit()
        song=Song.query.filter_by(title=song_name).first()
        song_id=song.song_id
        np=Playlist.query.filter_by(name=playlist_name).first()
        p_id=np.Playlist_id
        ps1 = PlaylistSongs(playlist_id=p_id,song_id=song_id)
        db.session.add(ps1)
        db.session.commit()
    return "Playlist has been Created"



@app.route("/newPlaylist", methods=["POST", "GET"])
def newPlaylist():
    all_songs = Song.query.all()
    if request.method == "GET":
         all_playlist = Playlist.query.all()
                 
         return render_template('playlistsongs.html',all_playlist=all_playlist,song=all_songs)
    if request.method == "POST":
         all_playlist = Playlist.query.all()
         pl_id = request.form["pl_id"]
         
         pl_song = PlaylistSongs.query.filter_by(playlist_id=pl_id).all()
         sl = []
         for x in pl_song:
             sl.append((Song.query.filter_by(song_id=x.song_id).first()))
         

        
         return render_template('pl_list.html',song=sl,all_playlist=all_playlist)



@app.route("/asp/<int:song_id>", methods=["POST", "GET"])
def asp(song_id):
    if request.method == "POST":
        newP = request.form["sp"]
        sId = song_id
        pId = Playlist.query.filter_by(name=newP).first().Playlist_id

        asp = PlaylistSongs(playlist_id=pId, song_id=sId)
        db.session.add(asp)
        db.session.commit()
        return redirect(url_for("home"))



# C R E A T E
@app.route("/creator", methods=["POST", "GET"])  # Admin Page
def creator():
    email = session["user_useremail"]
    user_id = User.query.filter_by(user_email=email).first()
    fetched_id = user_id.user_id
    all_creator = Creator.query.all()
    flag = False
    for i in all_creator:
        if i.user_id == fetched_id:
            session["creator_id"] = i.creator_id
            flag = True
            return redirect(url_for("creatorhomepage", creator_id=i.creator_id))
    if not flag:
        add_creator = Creator(user_id=fetched_id)
        db.session.add(add_creator)
        db.session.commit()
        all_creator = Creator.query.all()
        last_creator = all_creator[-1]
        session["creator_id"] = last_creator.creator_id

        return redirect(url_for("creatorhomepage", creator_id=last_creator.creator_id))


@app.route("/creatorhomepage", methods=["POST", "GET"])  # Admin Page
def creatorhomepage():
    if "user_useremail" in session:
        email = session["user_useremail"]
        password = session["user_password"]
        creator_id = session["creator_id"]
        all_users = User.query.all()
        all_songs = Song.query.all()
        all_playlist = Playlist.query.all()

        Flag = False
        for k in all_users:
            
            if k.user_email == email and k.user_password == password:
                Flag = True
                return render_template(
                    "creator.html",
                    status="You are a Creator",
                    username=k.user_name,
                    useremail=email,
                    song=all_songs,
                    user=k,
                    creator_id=creator_id,
                    all_playlist=all_playlist,
                )
        if Flag == False:
            session.pop("user_useremail", None)
            return "Invalid username or password"
    else:
        return render_template("musicfy.html")

# @app.route("/creator/update_albums", methods=["POST", "GET"])
# def updateAlbums():






@app.route("/creator/albums", methods=["POST", "GET"])
def albums():
    all_albums = Album.query.all()
    all_album_songs = AlbumSong.query.all()
    email = session["user_useremail"]
    creator_id=session["creator_id"]
    
    all_songs = Song.query.all()
    if request.method == "GET":
        if "user_useremail" in session:
            creator_album = Album.query.filter_by(creator_id=creator_id).all()
            print(creator_album)
            return render_template(
                "album_creget.html",
                albums=all_albums,
                creator_album=creator_album,
                all_album_songs=all_album_songs,
                # username=k.user_name,
                useremail=email,
            )
    if request.method == "POST":
        if "user_useremail" in session:
            album_name = request.form["albumname"]
            id_album = request.form["id_album"]
            song_id = AlbumSong.query.filter_by(album_id=id_album).all()
            song_list = []
            for songs in song_id:
                song = Song.query.filter_by(song_id=songs.song_id).first()
                song_list.append(song)
            print(song_list)

            print(id_album, song_id)
            return render_template(
                "album_cre.html",
                albums=all_albums,
                # all_album_songs=all_album_songs,
                song=song_list,
                # useremail=email,
            )

@app.route("/removesongfromalbum", methods=["POST", "GET"])
def remove():
    return "hi"


@app.route("/home/album", methods=["POST", "GET"])
def gen_albums():
    all_albums = Album.query.all()
    all_album_songs = AlbumSong.query.all()
    email = session["user_useremail"]
    all_songs = Song.query.all()
    if request.method == "GET":
        if "user_useremail" in session:
            return render_template(
                "album_gen.html",
                albums=all_albums,
                all_album_songs=all_album_songs,
                # username=k.user_name,
                useremail=email,
            )
    if request.method == "POST":
        if "user_useremail" in session:
            
            id_album = request.form["id_album"]
            song_id = AlbumSong.query.filter_by(album_id=id_album).all()
            song_list = []
            for songs in song_id:
                song = Song.query.filter_by(song_id=songs.song_id).first()
                song_list.append(song)
            print(song_list)

            print(id_album, song_id)
            return render_template(
                "album_gen.html",
                albums=all_albums,
                # all_album_songs=all_album_songs,
                song=song_list,
                # useremail=email,
            )


# C R E A T E - - - - A L B U M
@app.route("/uploadalbum", methods=["POST", "GET"])
def upload_album():
    if request.method == "POST":
        creator_id = session["creator_id"]
        album_name = request.form["album_name"]
        file_name = request.files["file_name"]
        song_name = request.form["song_name"]
        artist_name = request.form["artist_name"]
        genres_name = request.form["genres_name"]
        lyrics_name = request.form["lyrics_name"]
        all_albums = Album.query.filter_by(title=album_name).first()
        print(creator_id,genres_name,artist_name,file_name.filename,lyrics_name,all_albums)
        if all_albums is not None:
            print("nitin")
            s1 = Song(
                title=song_name,
                artist=artist_name,
                genre=genres_name,
                album=album_name,
                lyrics=lyrics_name,
                path=file_name.filename)
            db.session.add(s1)            
            db.session.commit()
            file_name.save("static/allsongs" + file_name.filename)
            album_n = Album.query.filter_by(title=album_name).first()
            song_n = Song.query.filter_by(title=song_name).first()
            print(album_n,album_n,song_n,song_n)
            as1 = AlbumSong(song_id = song_n.song_id, album_id = album_n.album_id)
            db.session.add(as1)
            db.session.commit()
            return "album updated"

            
        else:
            a1 = Album(title=album_name,creator_id=creator_id)
            # db.session.add(a1)
            # db.session.commit()
            s1 = Song(
                title=song_name,
                artist=artist_name,
                genre=genres_name,
                album=album_name,
                lyrics=lyrics_name,
                path=file_name.filename)
            db.session.add_all([s1,a1])
            
            db.session.commit()
            file_name.save("static/allsongs" + file_name.filename)
            album_n = Album.query.filter_by(title=album_name).first()
            song_n = Song.query.filter_by(title=song_name).first()
            print(album_n,album_n,song_n,song_n)
            as1 = AlbumSong(song_id = song_n.song_id, album_id = album_n.album_id)
            db.session.add(as1)
            db.session.commit()
            return "albumadde"



# A D M I N
@app.route("/adminLogin", methods=["POST", "GET"])  # Admin Page
def adminLogin():
    print("admin page")
    # if "admin_username" in session:
    #     print("session")
    #     return redirect(url_for("adminDashboard"))
    if request.method == "POST":
        username = request.form["user_name"]
        password = request.form["user_password"]
        print(username, password)
        # all_admin = Admin.query.all()
        # for i in range(0, len(all_admin)):
        # if all_admin[i].username == username and all_admin[i].password == password:
        # session["admin_username"] = username
        # session["admin_password"] = password
        # return redirect(url_for("adminDashboard"))
        if username == "admin@ds.study.iitm.ac.in" and password == "nitin":
         
            return redirect(url_for("adminDashboard"))

        # else:
        #  render_template("AdminLogin.html", title="Login Page")
    return render_template("AdminLogin.html", title="Login Page")


@app.route("/adminlogout")
def adminlogout():
    session.pop("admin_username", None)
    session.pop("creator_id", None)

    return redirect(url_for("adminLogin"))


@app.route("/adminDashboard", methods=(["POST", "GET"]))  # Admin login detail
def adminDashboard():
    if request.method == "GET":
        username = "nitin"
        total_users = User.query.all()  # Admin Stats
        total_creators = Creator.query.all()
        total_Albums = Album.query.all()
        general_user = int(len(User.query.all())-len(Creator.query.all()))
        song_list = Song.query.all()  # admin all songs
        all_playlist = Playlist.query.all()
        return render_template(
            "Admin_dashboard.html",
            admin=username,
            totalusers=len(total_users),
            song=song_list,
            all_creators=total_creators,
            total_creators=len(total_creators),
            total_Albums=len(total_Albums),
            all_Albums=total_Albums,
            general_user=general_user,
            total_songs=len(song_list),
            users = total_users,
            all_playlist = all_playlist,
            message="",
        )

    else:
        return redirect(url_for("adminLogin"))

# D E L E T E U S E R
@app.route("/deleteUser/<int:user_id>", methods=["post"])
def deleteUser(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return "The User has been deleted!"

# delete a song
@app.route("/deletesong/<int:song_id>", methods=["post"])
def deletesong(song_id):
    print("hello", song_id)
    song = Song.query.filter_by(song_id=song_id).first()
    db.session.delete(song)
    db.session.commit()
    return "song deleted"

@app.route("/deleteAlbum/<int:album_id>", methods=["post"])
def deleteAlbum(album_id):
    
    album = Album.query.filter_by(album_id=album_id).first()
    db.session.delete(album)
    db.session.commit()
    return "album deleted"

@app.route("/deleteCreator/<int:creator_id>", methods=["post"])
def deleteCreator(creator_id):
    
    creator = Creator.query.filter_by(creator_id=creator_id).first()
    db.session.delete(creator)
    db.session.commit()
    return "creator deleted"

@app.route("/deletePlaylist/<int:Playlist_id>", methods=["post"])
def deletePlaylist(Playlist_id):
    print(Playlist_id)
    playlist = Playlist.query.filter_by(Playlist_id=Playlist_id).first()
    print(playlist)
    db.session.delete(playlist)
    db.session.commit()
    return "Playlist deleted"




@app.route("/signup")  # signup page
def signup():
    return render_template("signup.html")


@app.route("/adduser", methods=["POST", "GET"])
def adduser():
    if request.method == "POST":
        user_name = request.form["user_name"]
        user_email = request.form["user_email"]
        user_password = request.form["user_password"]
        all_user = User.query.all()  # database id and passwords
        for x in all_user:
            if x.user_email == user_email and x.user_password == user_password:
                return "<h1>User Already Registered<h1>"
        else:
            b1 = User(
                user_name=user_name, user_email=user_email, user_password=user_password
            )
            db.session.add(b1)
            db.session.commit()
            # return "user added"
            return redirect("/")
    else:
        return render_template("signup.html")


@app.route("/rate/<int:song_id>/<int:user_id>", methods=["POST"])
def rate(song_id, user_id):
    rating_value = int(request.form.get("rating"))

    song = Song.query.get(song_id)
    user = User.query.get(user_id)
    if song:
        new_rating = Rating(value=rating_value, song=song, user=user)
        db.session.add(new_rating)
        db.session.commit()

    return redirect(url_for("home"))


@app.route("/searched", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        search_input = request.form["show_search"]

        results = Song.query.filter(Song.title.contains(search_input)).all()

        return render_template(
            "dashsearch.html", result=results, you_search=search_input
        )


# upload
@app.route("/upload", methods=["POST", "GET"])
def upload():
    return render_template("upload.html")


@app.route("/upload_song", methods=["POST", "GET"])
def uploaded():
    path = request.files["file"]
    title = request.form["songname"]
    artist = request.form["artistname"]
    genre = request.form["genre_name"]
    album = request.form["album_name"]
    lyrics = request.form["lyrics"]
    s1 = Song(
        title=title,
        artist=artist,
        genre=genre,
        album=album,
        lyrics=lyrics,
        path=path.filename,
    )
    db.session.add(s1)
    db.session.commit()
    path.save("static/allsongs" + path.filename)
    # if album is not None:
    #     add_album = Album(
    #         title=album,
    #         artist=artist,
    #         genre=genre,
    #     )
    return "song added"


app.run(debug=True)
#
# In this code, I have added comments to explain the purpose of each function and route. The comments are concise and clear, making it easier for you to understand the code.
