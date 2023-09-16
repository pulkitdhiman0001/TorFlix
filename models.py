import enum

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import ProductionConfig

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    # config development configuration for flask app
    app.config.from_object(ProductionConfig)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


class Admins(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String())
    role = db.Column(db.String(100))
    otp = db.Column(db.String(10))
    otp_flag = db.Column(db.Boolean, default=False)
    otp_expires_at = db.Column(db.String(100))

    def __init__(self, username, email, password, role, otp, otp_flag, otp_expires_at):
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.otp = otp
        self.otp_flag = otp_flag
        self.otp_expires_at = otp_expires_at


class Users(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String())
    role = db.Column(db.String())
    otp = db.Column(db.String(10))
    otp_flag = db.Column(db.Boolean, default=False)
    otp_expires_at = db.Column(db.String(100))
    verified = db.Column(db.Boolean, default=False)

    def __init__(self, email, password, role, otp, otp_flag, otp_expires_at, verified):
        self.email = email
        self.password = password
        self.role = role
        self.otp = otp
        self.otp_flag = otp_flag
        self.otp_expires_at = otp_expires_at
        self.verified = verified


class Torrents(db.Model):
    __tablename__ = "Torrents"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10000))
    torrent_id = db.Column(db.Integer)
    category = db.Column(db.String(1000))
    status = db.Column(db.String(100))
    thumbnail = db.Column(db.String(10000))
    download_percentage = db.Column(db.Float(), default=0.0)
    download_details = db.Column(db.String(10000), default='0.0')
    downloaded_path = db.Column(db.String(1000), default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user = db.relationship("Users")
    conversion_details = db.Column(db.String(), default=None)
    conversion_percentage = db.Column(db.Float(), default=0.0)
    conversion_flag = db.Column(db.Boolean(), default=False)
    no_of_files = db.Column(db.Integer)

    def __init__(self, name, torrent_id, category, status, thumbnail, download_percentage, download_details,
                 downloaded_path, user_id, conversion_details, conversion_percentage, no_of_files):
        self.name = name
        self.torrent_id = torrent_id
        self.category = category
        self.status = status
        self.thumbnail = thumbnail
        self.download_percentage = download_percentage
        self.download_details = download_details
        self.downloaded_path = downloaded_path
        self.user_id = user_id
        self.conversion_details = conversion_details
        self.conversion_percentage = conversion_percentage
        self.no_of_files = no_of_files


class DownloadedTorrentList(db.Model):
    __tablename__ = "DownloadedTorrentList"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user = db.relationship("Users")
    name = db.Column(db.String(10000))
    torrent_id = db.Column(db.Integer, unique=True)
    category = db.Column(db.String(1000))
    thumbnail = db.Column(db.String(10000))
    downloaded_path = db.Column(db.String(1000), default=None)
    no_of_files = db.Column(db.Integer)
    conversion_flag = db.Column(db.Boolean(), default=False)

    def __init__(self, user_id, name, torrent_id, category, thumbnail, downloaded_path, no_of_files):
        self.user_id = user_id
        self.name = name
        self.torrent_id = torrent_id
        self.category = category
        self.thumbnail = thumbnail
        self.downloaded_path = downloaded_path
        self.no_of_files = no_of_files


class Files(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    torrent_fk = db.Column(db.Integer, db.ForeignKey('DownloadedTorrentList.id'))
    torrent = db.relationship("DownloadedTorrentList")
    file_path = db.Column(db.String)

    def __init__(self, torrent, file_path):
        self.torrent = torrent
        self.file_path = file_path


#
class DownloadHistory(db.Model):
    __tablename__ = "DownloadHistory"
    id = db.Column(db.Integer, primary_key=True)
    torrent_id = db.Column(db.Integer)

    def __init__(self, torrent_id):
        self.torrent_id = torrent_id
