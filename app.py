import datetime
import os
import random
import re
import shutil
import time
from datetime import timedelta

import libtorrent as lt
from flask import render_template, request, url_for, flash, redirect, session, jsonify
from flask_mail import Mail, Message
from flask_migrate import Migrate
from py1337x import py1337x
from sqlalchemy import desc, asc
from werkzeug.security import check_password_hash, generate_password_hash

from models import create_app, db, Torrents, DownloadedTorrentList, Users, Admins, DownloadHistory, Files
from templates import Templates
from torrent_history_and_downloads import history, currently_downloading
from get_torrent_details import get_torrent_details

from video_converter import convert_to_mp4

app = create_app()
migrate = Migrate(app, db, render_as_batch=True)

email_reg = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
valid_email = "Enter a Valid Email"


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if 'username' in session and session["role"] == "admin":
        return redirect(url_for('users_list'))
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        admin_exists = Admins.query.filter_by(username=username).first()
        if admin_exists:
            if admin_exists.username == username and check_password_hash(admin_exists.password, password):
                session["username"] = admin_exists.username
                session["role"] = admin_exists.role

                session.permanent = True
                app.permanent_session_lifetime = timedelta(minutes=5)
                flash(f"Welcome {admin_exists.username}", category='success')
                return redirect(url_for('users_list'))

        flash('Username or password is incorrect', category='error')
        return render_template(Templates.admin_login)
    return render_template(Templates.admin_login)


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if 'username' in session and session["role"] == "user":
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]

        user_exists = Users.query.filter_by(email=email).first()
        if user_exists:
            if user_exists.email == email and check_password_hash(user_exists.password, password):
                session["username"] = user_exists.email
                session["role"] = user_exists.role

                session.permanent = True
                app.permanent_session_lifetime = timedelta(minutes=5)
                flash(f"Welcome {user_exists.email}", category='success')

                return redirect(url_for('index'))
            flash('Email or password is incorrect', category='error')
            return render_template(Templates.user_login)
        flash('Email or password is incorrect', category='error')
        return render_template(Templates.user_login)

    return render_template(Templates.user_login)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('index'))


@app.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if request.method == 'POST':
        userpass = request.form["password"]

        confirm_userpass = request.form["confirm_password"]
        hash_pass = generate_password_hash(userpass)
        if not re.match(email_regex, request.form["email"]):
            flash("Invalid Email", category='error')
            return render_template(Templates.register_admin)

        if userpass != confirm_userpass:
            flash("Password does not match", category='error')
            return render_template(Templates.register_admin)
        pass_regex = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$"
        if not re.match(pass_regex, userpass):
            flash("Password must contain Minimum eight characters, at least one letter and one number:",
                  category='error')
            return render_template(Templates.register_admin)
        get_admin = Admins.query.filter_by(email=request.form["email"]).first()
        otp_generate = random.randrange(111111, 999999)
        if get_admin:
            if not get_admin.verified:
                get_admin.email = request.form["email"]
                get_admin.password = hash_pass
                get_admin.otp = otp_generate
                now = datetime.datetime.now()
                current_time = now.strftime("%y-%m-%d %H:%M:%S")
                get_admin.otp_expires_at = str(
                    datetime.datetime.strptime(current_time, "%y-%m-%d %H:%M:%S") + timedelta(minutes=5))
                db.session.commit()
                send_mail(request.form["email"], role="admin")
                flash("OTP sent to" + ' ' + get_admin.email, category='success')
                return render_template(Templates.verifyOtp, user=get_admin.email, role="admin")
            flash("Email Already in use.", category='error')
            return render_template(Templates.register_admin)
        else:
            add_new_admin = Admins(username=request.form["username"], email=request.form["email"],
                                   password=hash_pass, role="admin", otp=None, otp_flag=False,
                                   otp_expires_at=None, verified=False)
            db.session.add(add_new_admin)
            db.session.commit()

            send_mail(request.form["email"], role="admin")
            # flash("OTP sent to" + ' ' + request.form["email"], category='success')

            return render_template(Templates.verifyOtp, user=request.form["email"], role="admin")

    return render_template(Templates.register_admin)


@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if request.method == 'POST':

        userpass = request.form["password"]

        confirm_userpass = request.form["confirm_password"]
        hash_pass = generate_password_hash(userpass)
        if not re.match(email_regex, request.form["email"]):
            flash("Invalid Email", category='error')
            return render_template(Templates.register_user)

        if userpass != confirm_userpass:
            flash("Password does not match", category='error')
            return render_template(Templates.register_user)
        pass_regex = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$"
        if not re.match(pass_regex, userpass):
            flash("Password must contain Minimum eight characters, at least one letter and one number:",
                  category='error')
            return render_template(Templates.register_user)
        get_user = Users.query.filter_by(email=request.form["email"]).first()
        otp_generate = random.randrange(111111, 999999)
        if get_user:
            if not get_user.verified:
                get_user.email = request.form["email"]
                get_user.password = hash_pass
                get_user.otp = otp_generate
                now = datetime.datetime.now()
                current_time = now.strftime("%y-%m-%d %H:%M:%S")
                get_user.otp_expires_at = str(
                    datetime.datetime.strptime(current_time, "%y-%m-%d %H:%M:%S") + timedelta(minutes=5))
                db.session.commit()
                send_mail(request.form["email"], role="user")
                flash("OTP sent to" + ' ' + get_user.email, category='success')
                return render_template(Templates.verifyOtp, user=get_user.email, role="user")
            flash("Email Already in use.", category='error')
            return render_template(Templates.register_user)
        else:
            add_new_user = Users(email=request.form["email"],
                                 password=hash_pass, role="user", otp=None, otp_flag=False,
                                 otp_expires_at=None, verified=False)
            db.session.add(add_new_user)
            db.session.commit()

            send_mail(request.form["email"], role="user")
            # flash("OTP sent to" + ' ' + request.form["email"], category='success')

            return render_template(Templates.verifyOtp, user=request.form["email"], role="user")
    return render_template(Templates.register_user)


mail = Mail(app)


@app.route('/verify-otp/<string:email>/<string:role>', methods=['GET', 'POST'])
def send_mail(email, role):
    if request.method == 'POST':

        otp_generate = random.randrange(111111, 999999)

        msg = Message("Request for OTP (One Time Password)",
                      sender="testing000123000@gmail.com",
                      recipients=[email])
        msg.body = f"Your One Time Password is {otp_generate}"

        mail.send(msg)
        if role == "user":
            get_user = Users.query.filter_by(email=email).first()
            if get_user:
                get_user.otp = otp_generate
                get_user.otp_flag = False
                now = datetime.datetime.now()
                current_time = now.strftime("%y-%m-%d %H:%M:%S")
                get_user.otp_expires_at = str(
                    datetime.datetime.strptime(current_time, "%y-%m-%d %H:%M:%S") + timedelta(minutes=5))

                db.session.commit()
                return render_template(Templates.verifyOtp, user=get_user.email, role="user")

            else:
                flash(f"No account found with the E-Mail: {request.form['email']}", category='error')
                return render_template(Templates.get_email)
        else:
            get_user = Admins.query.filter_by(email=email).first()
            if get_user:
                get_user.otp = otp_generate
                get_user.otp_flag = False
                now = datetime.datetime.now()
                current_time = now.strftime("%y-%m-%d %H:%M:%S")
                get_user.otp_expires_at = str(
                    datetime.datetime.strptime(current_time, "%y-%m-%d %H:%M:%S") + timedelta(minutes=5))

                db.session.commit()
                return render_template(Templates.verifyOtp, user=get_user.email)

            else:
                flash(f"No account found with the E-Mail: {request.form['email']}", category='error')
                return render_template(Templates.get_email)

    return render_template(Templates.get_email)


@app.route('/generate-new-otp', methods=['GET', 'POST'])
def generate_new_otp():
    email = request.form["user"]
    if request.method == "POST":
        otp_generate = random.randrange(111111, 999999)
        msg = Message("Request for OTP (One Time Password)",
                      sender="pulkitdhiman411@gmail.com",
                      recipients=[request.form["user"]])
        msg.body = f"Your One Time Password is {otp_generate}"
        mail.send(msg)

        if request.form["role"] == "user":
            get_user = Users.query.filter_by(email=request.form["user"]).first()
            get_user.otp = otp_generate
            get_user.otp_flag = False

            now = datetime.datetime.now()
            current_time = now.strftime("%y-%m-%d %H:%M:%S")
            get_user.otp_expires_at = datetime.datetime.strptime(current_time, "%y-%m-%d %H:%M:%S") + timedelta(
                minutes=5)

            db.session.commit()
            flash("Email With New OTP Sent", category='success')
            return render_template(Templates.verifyOtp, user=get_user.email, role="user")
        else:
            get_admin = Admins.query.filter_by(email=email).first()
            get_admin.otp = otp_generate
            get_admin.otp_flag = False

            now = datetime.datetime.now()
            current_time = now.strftime("%y-%m-%d %H:%M:%S")
            get_admin.otp_expires_at = datetime.datetime.strptime(current_time, "%y-%m-%d %H:%M:%S") + timedelta(
                minutes=5)

            db.session.commit()
            flash("Email With New OTP Sent", category='success')
            return render_template(Templates.verifyOtp, user=get_admin.email, role="admin")

    return render_template(Templates.verifyOtp, user=email)


@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == "POST":
        if request.form["role"] == "user":
            get_user = Users.query.filter_by(email=request.form["user"]).first()

            now = datetime.datetime.now()
            current_time = now.strftime("%y-%m-%d %H:%M:%S")

            db_date_time = datetime.datetime.strptime(str(get_user.otp_expires_at), "%Y-%m-%d %H:%M:%S")

            if get_user.otp != request.form['verify_otp']:
                flash('Invalid OTP.', category='error')
                return render_template(Templates.verifyOtp, user=get_user.email, role="user")

            if get_user.otp_flag is True:
                flash('OTP already used.', category='error')
                return render_template(Templates.verifyOtp, user=get_user.email, role="user")

            if datetime.datetime.strptime(current_time, "%y-%m-%d %H:%M:%S") > db_date_time:
                flash('OTP seems to be Expired.', category='error')
                return render_template(Templates.verifyOtp, user=get_user.email, role="user")

            else:
                get_user.otp_flag = True
                get_user.verified = True
                db.session.commit()
                flash('Account Created Successfully.', category='success')
                return redirect(url_for("user_login"))

        else:
            get_admin = Admins.query.filter_by(email=request.form["user"]).first()

            now = datetime.datetime.now()
            current_time = now.strftime("%y-%m-%d %H:%M:%S")

            db_date_time = datetime.datetime.strptime(str(get_admin.otp_expires_at), "%Y-%m-%d %H:%M:%S")

            if get_admin.otp != request.form['verify_otp']:
                flash('Invalid OTP.', category='error')
                return render_template(Templates.verifyOtp, user=get_admin.email, role="admin")

            if get_admin.otp_flag is True:
                flash('OTP already used.', category='error')
                return render_template(Templates.verifyOtp, user=get_admin.email, role="admin")

            if datetime.datetime.strptime(current_time, "%y-%m-%d %H:%M:%S") > db_date_time:
                flash('OTP seems to be Expired.', category='error')
                return render_template(Templates.verifyOtp, user=get_admin.email, role="admin")

            else:
                get_admin.otp_flag = True
                get_admin.verified = True
                db.session.commit()
                flash('Account Created Successfully.', category='success')
                return redirect(url_for('admin_login'))

    return render_template(Templates.verifyOtp)


@app.route('/verify-otp/<string:user_email>', methods=['GET', 'POST'])
def send_mail_for_password_reset(user_email):
    if request.method == 'POST':

        get_user = Users.query.filter_by(email=user_email).first()

        if get_user:
            otp_generate = random.randrange(111111, 999999)

            msg = Message("Request for OTP (One Time Password)",
                          sender="testing000123000@gmail.com",
                          recipients=[user_email])
            msg.body = f"Your One Time Password is {otp_generate}"

            mail.send(msg)
            get_user.otp = otp_generate
            get_user.otp_flag = False
            now = datetime.datetime.now()
            current_time = now.strftime("%y-%m-%d %H:%M:%S")
            get_user.otp_expires_at = str(
                datetime.datetime.strptime(current_time, "%y-%m-%d %H:%M:%S") + timedelta(minutes=5))

            db.session.commit()
            return render_template(Templates.verifyOTPforaccountrecovery, user=get_user.email)

        else:
            flash(f"No account found with the E-Mail: {request.form['email']}", category='error')
            return render_template(Templates.get_email)
    return render_template(Templates.get_email)


@app.route('/verify_otp_for_account_recovery', methods=['GET', 'POST'])
def verify_otp_for_account_recovery():
    if request.method == "POST":

        get_user = Users.query.filter_by(email=request.form["user"]).first()

        now = datetime.datetime.now()
        current_time = now.strftime("%y-%m-%d %H:%M:%S")

        db_date_time = datetime.datetime.strptime(str(get_user.otp_expires_at), "%Y-%m-%d %H:%M:%S")

        if get_user.otp != request.form['verify_otp']:
            flash('Invalid OTP.', category='error')
            return render_template(Templates.verifyOTPforaccountrecovery, user=get_user.email)

        if get_user.otp_flag is True:
            flash('OTP already used.', category='error')
            return render_template(Templates.verifyOTPforaccountrecovery, user=get_user.email)

        if datetime.datetime.strptime(current_time, "%y-%m-%d %H:%M:%S") > db_date_time:
            flash('OTP seems to be Expired.', category='error')
            return render_template(Templates.verifyOTPforaccountrecovery, user=get_user.email)

        else:
            get_user.otp_flag = True
            get_user.verified = True
            db.session.commit()
            return render_template(Templates.reset_password, user=get_user.email)

    return render_template(Templates.verifyOTPforaccountrecovery)


@app.route('/account-recovery', methods=['GET', 'POST'])
def account_recovery():
    return render_template(Templates.get_email)


@app.route('/verification', methods=['GET', 'POST'])
def get_email():
    user_email = request.form["email"]

    user_exists = Users.query.filter_by(email=user_email).first()
    if user_exists:
        send_mail_for_password_reset(user_email=user_email)
        return render_template(Templates.verifyOTPforaccountrecovery, user=user_email)
    flash(f"No account found with the E-Mail: {user_email}", category='error')
    return render_template(Templates.get_email, user=user_email)


@app.route('/password-reset', methods=['GET', 'POST'])
def password_reset():
    if request.method == "POST":
        get_user = Users.query.filter_by(email=request.form["user"]).first()

        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if new_password != confirm_password:
            flash("Password doesn't match", category='error')
            return render_template(Templates.reset_password, user=get_user.email)
        pass_regex = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$"
        if not re.match(pass_regex, new_password):
            flash("Password must contain Minimum eight characters, at least one letter and one number:",
                  category='error')
            return render_template(Templates.reset_password, user=get_user.email)
        else:
            get_user.password = generate_password_hash(new_password)
            db.session.commit()
            flash('Password Changed Successfully', category='success')
            return redirect(url_for('user_login'))
    return render_template(Templates.reset_password)


torrents = py1337x(cache='py1337xCache', proxy="1377x.to")


@app.route('/users_list', methods=['GET', 'POST'])
def users_list():
    if 'username' in session and session["role"] == "admin":
        get_users = Users.query.all()

        final_list = []
        for user in get_users:
            user = Users.query.filter_by(id=user.id).first()
            movie = {"user_id": user.id, "movie_list": {}}

            if user:
                get_user_downloaded_content = DownloadedTorrentList.query.filter_by(user_id=user.id).all()

                if len(get_user_downloaded_content) > 0:

                    for content in get_user_downloaded_content:
                        torrent_info = torrents.info(torrentId=content.torrent_id)

                        if torrent_info["category"] not in movie["movie_list"]:
                            movie["movie_list"][torrent_info["category"]] = []

                            # Append the movie to the corresponding category list
                        movie["movie_list"][torrent_info["category"]].append(torrent_info)

                    final_list.append(movie)
                else:
                    movie.update({"movie_list": {}})
                    final_list.append(movie)

        return render_template(Templates.users_list, get_users=get_users, final_list=final_list,
                               )

    flash("Login Required", category="error")
    return redirect(url_for("admin_login"))


@app.route('/', methods=['GET', 'POST'])
def index():
    if "username" in session and session["role"] == "user":
        download_torrents_history = DownloadHistory.query.order_by(desc(DownloadHistory.id)).all()
        download_in_progress = Torrents.query.filter_by(status="Downloading").all()
        get_user_identity = Users.query.filter_by(email=session["username"]).first()
        torrent_history = history(download_torrents_history, torrents, DownloadedTorrentList,
                                  get_user_identity=get_user_identity.id)

        downloading = currently_downloading(download_in_progress, torrents, DownloadedTorrentList,
                                            get_user_identity=get_user_identity.email)

        trending = torrents.trending(week=True)

        items = trending["items"]

        movie_list = get_torrent_details(items, torrents)

        return render_template('index.html', movie_list=movie_list, torrent_history=torrent_history,
                               downloading=downloading, title="Trending", get_user_identity=get_user_identity.email)

    trending = torrents.trending(week=True)

    items = trending["items"]

    movie_list = get_torrent_details(items, torrents)

    return render_template('index.html', movie_list=movie_list, title="Trending")


@app.route('/torrents/category=<string:badge>', methods=['GET', 'POST'])
def badge_torrents(badge):
    if "username" in session:
        download_torrents_history = DownloadHistory.query.order_by(desc(DownloadHistory.id)).all()
        download_in_progress = Torrents.query.filter_by(status="Downloading").all()

        get_user_identity = Users.query.filter_by(email=session["username"]).first()
        torrent_history = history(download_torrents_history, torrents, DownloadedTorrentList,
                                  get_user_identity=get_user_identity.id)

        downloading = currently_downloading(download_in_progress, torrents, DownloadedTorrentList,
                                            get_user_identity=get_user_identity.id)

        get_trending = torrents.trending()
        items = get_trending["items"]
        movie_list = get_torrent_details(torrents=torrents, badge=badge, items=items)
        return render_template('index.html', movie_list=movie_list, title=badge.capitalize(), torrent_history=torrent_history, downloading=downloading, get_user_identity=get_user_identity)
    flash("Login Required", category="error")
    return redirect(url_for('user_login'))


@app.route('/search/page=<int:page_no>', methods=['GET', 'POST'])
def search_torrents(page_no=1):
    if "username" in session:

        if request.method == 'GET':
            download_torrents_history = DownloadHistory.query.order_by(desc(DownloadHistory.id)).all()
            download_in_progress = Torrents.query.filter_by(status="Downloading").all()

            get_user_identity = Users.query.filter_by(email=session["username"]).first()
            torrent_history = history(download_torrents_history, torrents, DownloadedTorrentList,
                                      get_user_identity=get_user_identity.id)

            downloading = currently_downloading(download_in_progress, torrents, DownloadedTorrentList,
                                                get_user_identity=get_user_identity.id)

            input_search_by_user = request.args['search'].lower()

            search = torrents.search(input_search_by_user, sortBy='seeders', page=page_no)

            items = search["items"]

            movie_list = get_torrent_details(items, torrents)

            return render_template('index.html', page_no=page_no, search=search,
                                   input_search_by_user=input_search_by_user,
                                   movie_list=movie_list, torrent_history=torrent_history, downloading=downloading,
                                   title=request.args['search'], get_user_identity=get_user_identity)
        return redirect(url_for('index'))

    input_search_by_user = request.args['search'].lower()

    search = torrents.search(input_search_by_user, sortBy='seeders', page=page_no)

    items = search["items"]

    movie_list = get_torrent_details(items, torrents)

    return render_template('index.html', page_no=page_no, search=search, input_search_by_user=input_search_by_user,
                           movie_list=movie_list,
                           title=request.args['search'])


@app.route('/download/<string:magnet_link>/<int:torrent_id>', methods=['GET', 'POST'])
def download_torrents(magnet_link, torrent_id):
    if 'username' in session and session["role"] == "user":

        check_if_exists_in_torrents = Torrents.query.filter_by(torrent_id=torrent_id).first()

        get_torrent_info = torrents.info(torrentId=torrent_id)

        print(get_torrent_info)

        if get_torrent_info["magnetLink"] is None:
            flash("Something went wrong. THere is an issue with this torrent or is deleted form the server.",
                  category="error")
            # return redirect(url_for("search_torrents", page_no=1))
            search = request.args.get("search", '')
            search_query = search
            return redirect(url_for("search_torrents", page_no=1, search=search_query))

        get_user_identity = Users.query.filter_by(email=session["username"]).first()
        if not check_if_exists_in_torrents:
            check_if_torrent_exists_in_history = DownloadHistory.query.filter_by(torrent_id=torrent_id).first()
            if not check_if_torrent_exists_in_history:
                add_downloaded_torrent_to_download_history = DownloadHistory(torrent_id=torrent_id,
                                                                             user_id=get_user_identity.id)
                db.session.add(add_downloaded_torrent_to_download_history)
                db.session.commit()

            get_user_identity = Users.query.filter_by(email=session["username"]).first()

            get_torrent = torrents.info(torrentId=torrent_id)
            thumbnail = str(get_torrent["thumbnail"])

            link = magnet_link
            ses = lt.session()
            ses.listen_on(6881, 6891)
            params = {

                'save_path': os.path.join('static', 'downloadedTemp', str(session["username"]), str(torrent_id)),
                'storage_mode': lt.storage_mode_t(2),

            }

            handle = lt.add_magnet_uri(ses, link, params)
            ses.start_dht()

            begin = time.time()

            while not handle.has_metadata():
                time.sleep(1)

            check_if_torrent_exists = Torrents.query.filter_by(torrent_id=torrent_id).first()

            if check_if_torrent_exists:
                get_torrent.status = "Downloading..."
                db.session.commit()
            else:
                add_torrent = Torrents(name=str(handle.name()), torrent_id=torrent_id, status="Downloading",
                                       thumbnail=None, download_percentage=0, download_details=None,
                                       downloaded_path=None, user_id=get_user_identity.id,
                                       category=get_torrent["category"],
                                       conversion_details=None, conversion_percentage=0.0, no_of_files=None)
                db.session.add(add_torrent)
                db.session.commit()

            while handle.status().state != lt.torrent_status.seeding:

                s = handle.status()

                state_str = ['queued', 'checking', 'downloading metadata', 'downloading', 'finished', 'seeding',
                             'allocating']

                percentage = '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s ' % \
                             (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers,
                              state_str[s.state])
                print(percentage)
                get_torrent = Torrents.query.filter_by(torrent_id=torrent_id).first()
                if get_torrent:
                    get_torrent.download_details = str(percentage)
                    get_torrent.download_percentage = s.progress * 100
                    get_torrent.thumbnail = thumbnail
                    db.session.commit()
                else:
                    get_torrent.download_percentage = 0.0
                    db.session.commit()
                time.sleep(5)

            end = time.time()

            get_torrent.status = "Downloaded"
            get_torrent.download_percentage = 100.00

            db.session.commit()

            get_torrent = torrents.info(torrentId=torrent_id)

            if not os.path.exists(
                    os.path.join('static', 'downloadedTorrents', str(session["username"]), str(get_torrent['category']),
                                 str(torrent_id))):
                os.makedirs(
                    os.path.join('static', 'downloadedTorrents', str(session["username"]), str(get_torrent['category']),
                                 str(torrent_id)))

            source_dir = os.path.join('static', 'downloadedTemp', str(session["username"]), str(torrent_id))
            target_dir = os.path.join('static', 'downloadedTorrents', str(session["username"]),
                                      str(get_torrent['category']), str(torrent_id))

            final_file_path = ''
            get_torrent_form_torrents = Torrents.query.filter_by(torrent_id=torrent_id).first()

            media = ["Movies", "TV", "Anime", "Music", "Documentaries"]

            games_apps = ["Games", "Apps"]

            if os.path.isdir(source_dir):
                if any([x in str(get_torrent["category"]) for x in media]):
                    file_count = 0

                    media_file_extensions = ['mkv', 'mp4', 'flac', 'ogg', 'webm', 'flv', 'ogv', 'ogg', 'avi', 'wmv',
                                             'mov', 'mp3']
                    for root, dirs, files in os.walk(source_dir):
                        for file in files:
                            file_extension = file.split('.')[-1]
                            if file_extension in media_file_extensions:
                                file_path = os.path.join(root, file)
                                file_count += 1

                    add_to_downloaded_torrent_list = DownloadedTorrentList(name=str(handle.name()),
                                                                           torrent_id=torrent_id,
                                                                           thumbnail=thumbnail,
                                                                           category=get_torrent['category'],
                                                                           downloaded_path=get_torrent_form_torrents.downloaded_path,
                                                                           user_id=get_user_identity.id,
                                                                           no_of_files=file_count)
                    db.session.add(add_to_downloaded_torrent_list)
                    db.session.commit()
                    downloaded_torrent = DownloadedTorrentList.query.filter_by(torrent_id=torrent_id).first()

                    for root, dirs, files in os.walk(source_dir):
                        for file in files:
                            file_extension = file.split('.')[-1]
                            if file_extension in media_file_extensions:
                                file_path = os.path.join(root, file)
                                shutil.move(os.path.join(file_path), target_dir)

                                add_file_path_to_db_files = Files(file_path=os.path.join(target_dir, file),
                                                                  torrent=downloaded_torrent)
                                db.session.add(add_file_path_to_db_files)
                                db.session.commit()

                    get_torrent_form_torrents.no_of_files = file_count
                    db.session.commit()
                    shutil.rmtree(os.path.join('static', 'downloadedTemp', str(session["username"]), str(torrent_id)))
                    flash(f"'{str(get_torrent['name'])}' Ready To Watch !", category='success')
                    return redirect(url_for('my_list'))

                elif any([x in str(get_torrent["category"]) for x in games_apps]):
                    print("in games_apps")
                    file_names = os.listdir(source_dir)
                    for file_name in file_names:
                        shutil.move(os.path.join(source_dir, file_name), target_dir)
                        final_file_path = final_file_path + target_dir + '/' + file_name
                        torrent_downloaded_path = os.path.join('downloadedTorrents', str(session["username"]),
                                                               str(get_torrent['category']),
                                                               str(torrent_id), file_name)
                        get_torrent_form_torrents.downloaded_path = torrent_downloaded_path
                        add_to_downloaded_torrent_list = DownloadedTorrentList(name=str(handle.name()),
                                                                               torrent_id=torrent_id,
                                                                               thumbnail=thumbnail,
                                                                               category=get_torrent['category'],
                                                                               downloaded_path=torrent_downloaded_path,
                                                                               user_id=get_user_identity.id)
                        db.session.add(add_to_downloaded_torrent_list)
                        db.session.commit()
                    shutil.rmtree(os.path.join('static', 'downloadedTemp', str(session["username"]), str(torrent_id)))
                    flash(f"'{str(get_torrent['name'])}' Ready To Watch !", category='success')
                    return redirect(url_for('my_list'))
            else:

                source_dir = os.path.join('static', 'downloadedTemp', str(session["username"]), str(torrent_id))

                if any([x in str(get_torrent["category"]) for x in media]):
                    print("in second media")
                    file_count = 0

                    media_file_extensions = ['mkv', 'mp4', 'flac', 'ogg', 'webm', 'flv', 'ogv', 'ogg', 'avi', 'wmv',
                                             'mov', 'mp3']
                    for root, dirs, files in os.walk(source_dir):
                        for file in files:
                            file_extension = file.split('.')[-1]
                            if file_extension in media_file_extensions:
                                file_path = os.path.join(root, file)
                                file_count += 1

                    add_to_downloaded_torrent_list = DownloadedTorrentList(name=str(handle.name()),
                                                                           torrent_id=torrent_id,
                                                                           thumbnail=thumbnail,
                                                                           category=get_torrent['category'],
                                                                           downloaded_path=get_torrent_form_torrents.downloaded_path,
                                                                           user_id=get_user_identity.id,
                                                                           no_of_files=file_count)
                    db.session.add(add_to_downloaded_torrent_list)
                    db.session.commit()
                    downloaded_torrent = DownloadedTorrentList.query.filter_by(torrent_id=torrent_id).first()

                    for root, dirs, files in os.walk(source_dir):
                        for file in files:
                            # file_extension = os.path.splitext(file)[1].lower()
                            file_extension = file.split('.')[-1]
                            if file_extension in media_file_extensions:
                                print('adding to files')
                                file_path = os.path.join(root, file)
                                shutil.move(os.path.join(file_path), target_dir)

                                add_file_path_to_db_files = Files(file_path=os.path.join(target_dir, file),
                                                                  torrent=downloaded_torrent)
                                db.session.add(add_file_path_to_db_files)
                                db.session.commit()

                    get_torrent_form_torrents.no_of_files = file_count
                    db.session.commit()
                    shutil.rmtree(os.path.join('static', 'downloadedTemp', str(session["username"]), str(torrent_id)))
                    flash(f"'{str(get_torrent['name'])}' Ready To Watch !", category='success')
                    return redirect(url_for('my_list'))

        return redirect(url_for('index'))
    return redirect(Templates.user_login)


@app.route('/convert_video/<int:torrent_id>', methods=['GET', 'POST'])
def convert_video(torrent_id):
    if "username" in session:
        get_downloaded_torrent = DownloadedTorrentList.query.filter_by(torrent_id=torrent_id).first()
        get_files = Files.query.order_by(asc(Files.file_path)).filter_by(torrent_fk=get_downloaded_torrent.id).all()

        for i in get_files:
            print(i)

        for file in get_files:
            print(file.id)
            delimiter = file.file_path.split('/')[-1]
            parts = file.file_path.split(delimiter)
            convert_to_mp4(input_path=file.file_path,
                           output_path=os.path.join(parts[0],
                                                    f'{os.path.splitext(file.file_path)[0].split("/")[-1]}' +
                                                    file.file_path.split('.')[-1].replace(
                                                        file.file_path.split('.')[-1], '.mp4')),
                           torrent_id=torrent_id, filename=file.file_path.split('/')[-1], file_id=file.id)
        return redirect(url_for("global_downloads"))
    return redirect(url_for('user_login'))


@app.route('/download_torrent_to_client_device/<int:torrent_id>', methods=['GET', 'POST'])
def download_torrent_to_client_device(torrent_id):
    from flask import send_file
    from archive_torrent_files import archive_torrent
    if "username" in session:
        get_torrent_form_downloaded_torrent = DownloadedTorrentList.query.filter_by(torrent_id=torrent_id).first()

        get_torrent_files = Files.query.filter_by(torrent_fk=get_torrent_form_downloaded_torrent.id).all()

        get_no_of_files = len(get_torrent_files)

        if get_no_of_files > 1:

            files = []

            for file in get_torrent_files:
                files.append(file.file_path)

            archive = archive_torrent(archive_filename=get_torrent_form_downloaded_torrent.name, files_to_archive=files)
            print(archive, 'aaaa')

            return send_file(archive, as_attachment=True)

        get_torrent_file = Files.query.filter_by(torrent_fk=get_torrent_form_downloaded_torrent.id).first()
        file = get_torrent_file.file_path
        return send_file(file, as_attachment=True)
    return redirect(url_for('user_login'))


@app.route('/cancel_download/<int:torrent_id>', methods=['GET', 'POST'])
def cancel_download(torrent_id):
    if 'username' in session and session["role"] == "user":
        get_torrent_to_cancel = Torrents.query.filter_by(torrent_id=torrent_id).first()
        get_torrent_name = torrents.info(torrentId=torrent_id)

        if os.path.exists(
                os.path.isfile(os.path.join('static', 'downloadedTemp', str(session["username"]), str(torrent_id)))):
            if not os.path.isfile(os.path.join('static', 'downloadedTemp', str(session["username"]), str(torrent_id))):
                flash("Download Canceled !", category='success')
                shutil.rmtree(os.path.join('static', 'downloadedTemp', str(session["username"]), str(torrent_id)))
                print('one')
                db.session.delete(get_torrent_to_cancel)
                db.session.commit()
                return redirect(url_for('index'))

    flash("Login Required", category="error")
    return redirect(url_for('user_login'))


@app.route('/global_downloads', methods=['GET', 'POST'])
def global_downloads():
    if 'username' in session and session["role"] == "user":

        download_torrents_history = DownloadHistory.query.order_by(desc(DownloadHistory.id)).all()
        download_in_progress = Torrents.query.filter_by(status="Downloading").all()

        get_user_identity = Users.query.filter_by(email=session["username"]).first()
        torrent_history = history(download_torrents_history, torrents, DownloadedTorrentList,
                                  get_user_identity=get_user_identity.id)

        downloading = currently_downloading(download_in_progress, torrents, DownloadedTorrentList,
                                            get_user_identity=get_user_identity.id)

        get_list_of_downloaded_torrents = DownloadedTorrentList.query.all()

        recommendation = []

        unique_category = []

        for torrent in get_list_of_downloaded_torrents:
            torrent_info = torrents.info(torrentId=torrent.torrent_id)

            recommend = torrents.trending(category=torrent_info["category"])

            items = recommend["items"]

            if torrent_info["category"] not in unique_category:
                unique_category.append(torrent_info["category"])
                for movie in get_torrent_details(items, torrents, category=torrent_info["category"]):
                    recommendation.append(movie)

        movie_list = []

        for downloaded_torrents in get_list_of_downloaded_torrents:
            search = torrents.info(torrentId=downloaded_torrents.torrent_id)
            search["torrentId"] = downloaded_torrents.torrent_id
            search["no_of_files"] = downloaded_torrents.no_of_files
            search["user_id"] = downloaded_torrents.user_id
            search["conversion_flag"] = downloaded_torrents.conversion_flag

            files = Files.query.order_by(Files.file_path).filter_by(torrent_fk=downloaded_torrents.id).all()

            movie_list.append(search)
            search.update({'files': files})

        return render_template('my_list.html', movie_list=movie_list, recommendation=recommendation,
                               get_user_identity=get_user_identity,
                               downloading=downloading, torrent_history=torrent_history, title="Global Downloads")
    flash("Login Required", category="error")
    return redirect(url_for('user_login'))


@app.route('/my_list', methods=['GET', 'POST'])
def my_list():
    if 'username' in session and session["role"] == "user":

        download_torrents_history = DownloadHistory.query.order_by(desc(DownloadHistory.id)).all()
        download_in_progress = Torrents.query.filter_by(status="Downloading").all()

        get_user_identity = Users.query.filter_by(email=session["username"]).first()
        torrent_history = history(download_torrents_history, torrents, DownloadedTorrentList,
                                  get_user_identity=get_user_identity.id)

        downloading = currently_downloading(download_in_progress, torrents, DownloadedTorrentList,
                                            get_user_identity=get_user_identity.id)

        get_list_of_downloaded_torrents = DownloadedTorrentList.query.filter_by(user_id=get_user_identity.id).all()

        recommendation = []

        unique_category = []

        for torrent in get_list_of_downloaded_torrents:
            torrent_info = torrents.info(torrentId=torrent.torrent_id)

            recommend = torrents.trending(category=torrent_info["category"])

            items = recommend["items"]

            if torrent_info["category"] not in unique_category:
                unique_category.append(torrent_info["category"])
                for movie in get_torrent_details(items, torrents, category=torrent_info["category"]):
                    recommendation.append(movie)

        movie_list = []

        for downloaded_torrents in get_list_of_downloaded_torrents:
            search = torrents.info(torrentId=downloaded_torrents.torrent_id)
            search["torrentId"] = downloaded_torrents.torrent_id
            search["no_of_files"] = downloaded_torrents.no_of_files
            search["user_id"] = downloaded_torrents.user_id
            search["conversion_flag"] = downloaded_torrents.conversion_flag

            files = Files.query.order_by(Files.file_path).filter_by(torrent_fk=downloaded_torrents.id).all()

            movie_list.append(search)
            search.update({'files': files})

        return render_template(Templates.my_list, movie_list=movie_list, get_user_identity=get_user_identity,
                               downloading=downloading, recommendation=recommendation,
                               torrent_history=torrent_history, title="My List")
    flash("Login Required", category="error")
    return redirect(url_for('user_login'))


@app.route('/delete_torrent/<int:torrent_id>/<string:torrent_category>', methods=['GET', 'POST'])
def delete_watched_torrent(torrent_id, torrent_category):
    if 'username' in session and session["role"] == "user":

        check_if_torrent_download_exists = DownloadedTorrentList.query.filter_by(torrent_id=torrent_id).first()
        check_if_torrent_exists = Torrents.query.filter_by(torrent_id=torrent_id).first()

        get_user_identity = Users.query.filter_by(email=session["username"]).first()

        if check_if_torrent_exists and check_if_torrent_exists.user_id == get_user_identity.id:

            torrent_dir = os.path.join('static', 'downloadedTorrents', str(session["username"]), str(torrent_category),
                                       str(torrent_id))
            if os.path.isdir(torrent_dir):

                get_torrent_from_files_modal = Files.query.filter_by(
                    torrent_fk=check_if_torrent_download_exists.id).all()

                for file in get_torrent_from_files_modal:
                    db.session.delete(file)
                    db.session.commit()
                shutil.rmtree(torrent_dir)
                db.session.delete(check_if_torrent_download_exists)
                db.session.delete(check_if_torrent_exists)
                db.session.commit()

                flash("Torrent Deleted Successfully", category="success")
                return redirect(url_for('my_list'))
        flash("An Error occurred while deleting torrent.", category="error")
        return redirect(url_for('global_downloads'))
    return render_template(Templates.user_login)


@app.route('/<string:torrent_category>', methods=['GET', 'POST'])
def category(torrent_category):
    if "username" in session and session["role"] == "user":
        download_torrents_history = DownloadHistory.query.order_by(desc(DownloadHistory.id)).all()
        download_in_progress = Torrents.query.filter_by(status="Downloading").all()

        get_user_identity = Users.query.filter_by(email=session["username"]).first()
        torrent_history = history(download_torrents_history, torrents, DownloadedTorrentList,
                                  get_user_identity=get_user_identity.id)

        downloading = currently_downloading(download_in_progress, torrents, DownloadedTorrentList,
                                            get_user_identity=get_user_identity.id)

        search_torrent = torrents.trending(category=torrent_category, week=True)

        items = search_torrent["items"]

        movie_list = get_torrent_details(items, torrents)

        return render_template('index.html', movie_list=movie_list, downloading=downloading,
                               torrent_history=torrent_history, get_user_identity=get_user_identity,
                               title=torrent_category.capitalize())

    search_torrent = torrents.trending(category=torrent_category, week=True)

    items = search_torrent["items"]

    movie_list = get_torrent_details(items, torrents)

    return render_template('index.html', movie_list=movie_list,
                           title=torrent_category.capitalize())


@app.route('/watch_download_torrents/<string:torrent_id>/<int:file_id>', methods=['GET', 'POST'])
def watch_download_torrents(torrent_id, file_id):
    if 'username' in session and session["role"] == "user":

        download_torrents_history = DownloadHistory.query.order_by(desc(DownloadHistory.id)).all()
        download_in_progress = Torrents.query.filter_by(status="Downloading").all()

        get_user_identity = Users.query.filter_by(email=session["username"]).first()
        torrent_history = history(download_torrents_history, torrents, DownloadedTorrentList,
                                  get_user_identity=get_user_identity.id)

        downloading = currently_downloading(download_in_progress, torrents, DownloadedTorrentList,
                                            get_user_identity=get_user_identity.id)

        get_torrent = DownloadedTorrentList.query.filter_by(torrent_id=torrent_id).first()
        search_related_torrents = torrents.info(torrentId=torrent_id)
        if search_related_torrents["genre"] is not None:
            search_related = torrents.trending(search_related_torrents['genre'][0])
            print(search_related, search_related_torrents["genre"])
        else:
            search_related = torrents.top()

        items = search_related["items"]

        if len(items) < 1:
            search_related = torrents.top()
            items = search_related["items"]

        movie_list = get_torrent_details(items, torrents)

        get_file_to_watch = Files.query.filter_by(id=file_id).first()

        file_path = str(get_file_to_watch.file_path.split('static/')[1])

        old_file_name = file_path.split('/')[-1]
        split_ext = old_file_name.split('.')[-1]
        new_file_name = old_file_name.split(split_ext)[0].replace('.', ' ')

        get_torrent_category = DownloadedTorrentList.query.filter_by(torrent_id=torrent_id).first()
        audio_torrent_info = torrents.info(torrentId=torrent_id)

        if get_torrent_category.category == "Music" and not get_file_to_watch.file_path.split('/')[-1].endswith('.mp3'):
            file_path = str(get_file_to_watch.file_path)

            from audio_conversion import audio_conversion

            convert = audio_conversion(file_id=file_id, input_file=file_path,
                                       output_file=file_path.replace(file_path.split('.')[-1], 'mp3'),
                                       ext=file_path.split('.')[-1])

            file_path = convert

            return render_template('playvideo.html', new_file_name=new_file_name, file_path=file_path,
                                   downloading=downloading,
                                   get_torrent=get_torrent, audio_torrent_info=audio_torrent_info,
                                   movie_list=movie_list,
                                   torrent_history=torrent_history, get_user_identity=get_user_identity,
                                   mimetype='video/mp4')
        print(get_torrent.conversion_flag, movie_list)
        if not get_torrent.conversion_flag and not get_torrent_category.category == "Music":
            flash("Dealing with torrents with different formats is a tricky task. If there is any issue with plathe video (like no video showing, or audio not playing),"
                  "you can fix the issue in 'My List' section. just select the movie you want to watch and click on the "
                  "wrench icon (Processing may take some time). or simply you can download the movie to your device and "
                  "can play with your favourite media player.", category="success")
            return render_template('playvideo.html', new_file_name=new_file_name, file_path=file_path,
                                   downloading=downloading,
                                   get_torrent=get_torrent, audio_torrent_info=audio_torrent_info,
                                   movie_list=movie_list,
                                   torrent_history=torrent_history, get_user_identity=get_user_identity,
                                   mimetype='video/mp4')
        return render_template('playvideo.html', new_file_name=new_file_name, file_path=file_path,
                               downloading=downloading,
                               get_torrent=get_torrent, audio_torrent_info=audio_torrent_info, movie_list=movie_list,
                               torrent_history=torrent_history, get_user_identity=get_user_identity,
                               mimetype='video/mp4')
    return redirect(url_for('user_login'))


@app.route('/check_if_exists/<int:torrent_id>', methods=['GET', 'POST'])
def check_if_exists(torrent_id):
    get_torrent = Torrents.query.filter_by(torrent_id=torrent_id).first()

    if get_torrent:
        if get_torrent.download_percentage == 100:
            res = {'condition': True,
                   'conversion_flag': get_torrent.conversion_flag}

            return jsonify(res)
        else:
            res = {'condition': False}

            return jsonify(res)
    else:
        res = {'condition': False}

        return jsonify(res)


@app.route('/get_download_status/<int:torrent_id>', methods=['GET', 'POST'])
def get_download_status(torrent_id):
    get_torrent = Torrents.query.filter_by(torrent_id=torrent_id).first()

    get_session_user = Users.query.filter_by(email=session["username"]).first()

    if get_torrent:
        res = {'condition': True,
               'status': get_torrent.status,
               'download_details': get_torrent.download_details,
               'percentage': get_torrent.download_percentage,
               'conversion_details': get_torrent.conversion_details,
               'conversion_percentage': get_torrent.conversion_percentage,
               'conversion_flag': get_torrent.conversion_flag,
               'user_id': get_torrent.user_id,
               'session_id': get_session_user.id,
               }
        return jsonify(res)
    else:
        res = {'condition': False, }
        return jsonify(res)


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', threaded=True)
