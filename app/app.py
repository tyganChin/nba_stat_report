## Name    : app.py
## Author  : Tygan Chin
## Purpose : Runs the flask application for the website. Displays the home page
##           when website is first accessed and displays player reports when
##           requests are made through get requests.

from flask import Flask, render_template, request, jsonify
import subprocess
from modules.setHome import setHome

# Create a Flask instance
app = Flask(__name__)

# home page
@app.route('/')
def home():
    setHome()
    return render_template('home.html')

# takes in a player id and returns the html page of the players report
@app.route('/submit', methods=['GET'])
def submit():

    # ensure player id was recieved
    player_id = request.args.get('id')
    if not player_id:
        app.logger.error("No player ID received!")
    else:
        app.logger.debug(f"Received player ID: {player_id}")

    # run the script to generate the report
    result = subprocess.run(
        ["python3", "modules/getInfo.py", player_id],
        text=True,
        capture_output=True
    )

    # debugging inforation
    app.logger.debug("Subprocess output: " + result.stdout)
    app.logger.error("Subprocess error: " + result.stderr)

    # render the template generated by the script to display to user
    return render_template('index.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)