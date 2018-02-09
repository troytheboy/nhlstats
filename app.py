from flask import Flask
from flask import render_template
from flask import request
# Add support for Bootstrap to make our app look pretty
from flask_bootstrap import Bootstrap

# import the postgres module
import psycopg2

# import goodies to make SELECT statments eaiser
# Returns values from a SELECT as a dictionary. Yay!
from psycopg2.extras import DictCursor

# Connect to the database using the dictionary cursor
# Replace your database, username, and password
# conn = psycopg2.connect("dbname= user= password=")

conn = psycopg2.connect("dbname=ericdkha password=info340 user=ericdkha host='127.0.0.1'")

# Create a cursor
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

app = Flask(__name__)

# Add support for Bootstrap to make our app look pretty
# Documentation at http://pythonhosted.org/Flask-Bootstrap/basic-usage.html
Bootstrap(app)

# Default route, so it's the homepage
@app.route('/')
def home():
    # Select all of the works from our databse
    cur.execute("SELECT t.team_name, t.team_id, t.founded, tl.city, tl.state_prov FROM team t, team_loc tl WHERE tl.city_id = t.team_city_id")
    team = cur.fetchall()
    cur.execute("SELECT p.player_id, p.fname, p.lname, p.team_id, t.team_name, p.pos_id FROM player p, team t WHERE p.team_id = t.team_id ORDER BY p.lname ASC")
    # Fetch them all at once
    # We will give this list to the template so it can build a table
    players = cur.fetchall()
    # Render the template with all of the variables
    return render_template('teams.html', players=players, team=team)

# Give details about a work
# URL format is work/<workid>
@app.route('/players.html', methods=['POST'])
@app.route('/team/<team_id>')
def team(team_id=None):
    if request.method == 'POST':
        team = request.form['team']
        cur.execute("SELECT t.team_id, t.team_name, t.founded, tl.city, tl.state_prov FROM team t, team_loc tl where t.team_id=%s AND t.team_city_id = tl.city_id", (team,))
        team_info = cur.fetchone()
        # Get information about the work
        cur.execute("SELECT p.player_id, p.fname, p.lname, p.total_points_scored, p.goals_made, p.assists_made, p.age, p.grit FROM player p, team t where p.team_id = %s AND p.team_id = t.team_id", (team,))
        player_info = cur.fetchall()
        return render_template('players.html', players=player_info, team=team_info)
    elif team_id:
        # Select all of the charaters from from the title
        #cur.execute("SELECT t.team_name, t.founded, tl.team_city, tl.state_prov FROM team t, team_loc tl WHERE tl.city_id = t.team_city_id")
        cur.execute("SELECT t.team_id, t.team_name, t.founded, tl.city, tl.state_prov FROM team t, team_loc tl where t.team_id=%s AND t.team_city_id = tl.city_id", (team_id,))
        team_info = cur.fetchone()
        # Get information about the work
        cur.execute("SELECT p.player_id, p.fname, p.lname, p.total_points_scored, p.goals_made, p.assists_made, p.age, p.grit FROM player p, team t where p.team_id = %s AND p.team_id = t.team_id", (team_id,))
        player_info = cur.fetchall()
        # Render the template with all of the variables
        return render_template('players.html', players=player_info, team=team_info)
    else:
        # We didn't get a workid
        home()

@app.route('/player/<player_id>')
def player(player_id=None):
    if player_id:
        # Select all of the charaters from from the title
        #cur.execute("SELECT t.team_name, t.founded, tl.team_city, tl.state_prov FROM team t, team_loc tl WHERE tl.city_id = t.team_city_id")
        cur.execute("SELECT * FROM player p, team t where p.player_id=%s AND p.team_id = t.team_id", (player_id,))
        player_info = cur.fetchone()
        # Get information about the work
        #cur.execute("SELECT p.fname, p.lname, p.total_points_scored, p.goals_made, p.assists_made, p.age, p.grit FROM player p, team t where p.team_id = %s AND p.team_id = t.team_id", (team_id,))
        #player_info = cur.fetchall()
        # Render the template with all of the variables
        return render_template('player.html', player=player_info)
    else:
        # We didn't get a workid
        home()



if __name__ == '__main__':
    app.run(debug=True)
