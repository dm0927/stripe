from flask import Blueprint, jsonify, make_response, request, render_template

home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
def home_page():
    return render_template('home-page.html')