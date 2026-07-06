from flask import Blueprint, render_template

ui_blueprint = Blueprint("ui", __name__)


@ui_blueprint.route("/")
def home():
    return render_template("index.html")
