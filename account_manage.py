""" check validity of username and password, retrieve data when valid """
from flask import Blueprint, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager

test_login = LoginManager()
db = SQLAlchemy()

login = Blueprint("login", __name__)


class UserModel(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@test_login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))


@login.route("/test_login", methods=["POST", "GET"])
def t_login():
    if current_user.is_authenticated:
        return redirect("/true_monitor")

    if request.method == "POST":
        username = request.form["username"]
        user = UserModel.query.filter_by(username=username).first()
        if user is not None and user.check_password(request.form["password"]):
            login_user(user)
            return redirect("/true_monitor")

    return render_template("login.html")