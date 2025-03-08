from datetime import datetime
import random
import traceback
from flask import Flask, redirect, render_template, request, url_for, session
import pickle
import pandas as pd
import sqlite3
with open('pipe.pkl', 'rb') as file:
    pipe = pickle.load(file)
with open('random_forest_pipeline_model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)
teams = [
    'Australia', 'India', 'Bangladesh', 'New Zealand', 'South Africa',
    'England', 'West Indies', 'Afghanistan', 'Pakistan', 'Sri Lanka'
]
cities = [
    'Colombo', 'Mirpur', 'Johannesburg', 'Dubai', 'Auckland', 'Cape Town',
    'London', 'Pallekele', 'Barbados', 'Sydney', 'Melbourne', 'Durban',
    'St Lucia', 'Wellington', 'Lauderhill', 'Hamilton', 'Centurion',
    'Manchester', 'Abu Dhabi', 'Mumbai', 'Nottingham', 'Southampton',
    'Mount Maunganui', 'Chittagong', 'Kolkata', 'Lahore', 'Delhi',
    'Nagpur', 'Chandigarh', 'Adelaide', 'Bangalore', 'St Kitts', 'Cardiff',
    'Christchurch', 'Trinidad'
]
from sklearn.preprocessing import LabelEncoder
le_venue = LabelEncoder()
le_city = LabelEncoder()
venues = ['Rajiv Gandhi International Stadium, Uppal', 'Maharashtra Cricket Association Stadium', 
          'Saurashtra Cricket Association Stadium', 'Holkar Cricket Stadium', 'M Chinnaswamy Stadium', 
          'Wankhede Stadium', 'Eden Gardens', 'Feroz Shah Kotla', 'Punjab Cricket Association IS Bindra Stadium, Mohali', 
          'Green Park', 'Punjab Cricket Association Stadium, Mohali', 'Sawai Mansingh Stadium', 
          'MA Chidambaram Stadium, Chepauk', 'Dr DY Patil Sports Academy', 'Newlands', "St George's Park", 
          'Kingsmead', 'SuperSport Park', 'Buffalo Park', 'New Wanderers Stadium', 'De Beers Diamond Oval', 
          'OUTsurance Oval', 'Brabourne Stadium', 'Sardar Patel Stadium, Motera', 'Barabati Stadium', 
          'Vidarbha Cricket Association Stadium, Jamtha', 'Himachal Pradesh Cricket Association Stadium', 
          'Nehru Stadium', 'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium', 'Subrata Roy Sahara Stadium', 
          'Shaheed Veer Narayan Singh International Stadium', 'JSCA International Stadium Complex', 
          'Sheikh Zayed Stadium', 'Sharjah Cricket Stadium', 'Dubai International Cricket Stadium', 
          'M. A. Chidambaram Stadium', 'Feroz Shah Kotla Ground', 'M. Chinnaswamy Stadium', 'Rajiv Gandhi Intl. Cricket Stadium', 
          'IS Bindra Stadium', 'ACA-VDCA Stadium']
cities = ['Hyderabad', 'Pune', 'Rajkot', 'Indore', 'Bangalore', 'Mumbai', 'Kolkata', 'Delhi', 'Chandigarh', 'Kanpur', 
          'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth', 'Durban', 'Centurion', 'East London', 'Johannesburg', 
          'Kimberley', 'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala', 'Kochi', 'Visakhapatnam', 'Raipur', 
          'Ranchi', 'Abu Dhabi', 'Sharjah', 'Dubai', 'Mohali', 'Bengaluru']
iteams=['MI','KKR','RCB','DC','CSK','RR','DD','GL','KXIP','SRH','RPS','KTK','PW']
icities=['Hyderabad', 'Pune', 'Rajkot', 'Indore', 'Bangalore', 'Mumbai', 'Kolkata', 'Delhi', 'Chandigarh', 'Kanpur', 
          'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth', 'Durban', 'Centurion', 'East London', 'Johannesburg', 
          'Kimberley', 'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala', 'Kochi', 'Visakhapatnam', 'Raipur', 
          'Ranchi', 'Abu Dhabi', 'Sharjah', 'Dubai', 'Mohali', 'Bengaluru']
le_venue.fit(venues)
le_city.fit(cities)
encode = {'team1': {'MI':1,'KKR':2,'RCB':3,'DC':4,'CSK':5,'RR':6,'DD':7,'GL':8,'KXIP':9,'SRH':10,'RPS':11,'KTK':12,'PW':13},
          'team2': {'MI':1,'KKR':2,'RCB':3,'DC':4,'CSK':5,'RR':6,'DD':7,'GL':8,'KXIP':9,'SRH':10,'RPS':11,'KTK':12,'PW':13},
          'toss_winner': {'MI':1,'KKR':2,'RCB':3,'DC':4,'CSK':5,'RR':6,'DD':7,'GL':8,'KXIP':9,'SRH':10,'RPS':11,'KTK':12,'PW':13},
          'winner': {'MI':1,'KKR':2,'RCB':3,'DC':4,'CSK':5,'RR':6,'DD':7,'GL':8,'KXIP':9,'SRH':10,'RPS':11,'KTK':12,'PW':13,'Draw':14}}
toss_decision_mapping = {
    'bat': 0,
    'field': 1
}
tcities = [
    'Colombo', 'Mirpur', 'Johannesburg', 'Dubai', 'Auckland', 'Cape Town',
    'London', 'Pallekele', 'Barbados', 'Sydney', 'Melbourne', 'Durban',
    'St Lucia', 'Wellington', 'Lauderhill', 'Hamilton', 'Centurion',
    'Manchester', 'Abu Dhabi', 'Mumbai', 'Nottingham', 'Southampton',
    'Mount Maunganui', 'Chittagong', 'Kolkata', 'Lahore', 'Delhi',
    'Nagpur', 'Chandigarh', 'Adelaide', 'Bangalore', 'St Kitts', 'Cardiff',
    'Christchurch', 'Trinidad'
]
venue= [
    "R. Premadasa Stadium",
    "Sinhalese Sports Club Ground",
    "P Sara Oval",
    "Sher-e-Bangla National Cricket Stadium",
    "The Wanderers Stadium",
    "Dubai International Stadium",
    "Eden Park",
    "Newlands Cricket Ground",
    "Lord's",
    "The Oval",
    "Pallekele International Cricket Stadium",
    "Kensington Oval",
    "Sydney Cricket Ground (SCG)",
    "Melbourne Cricket Ground (MCG)",
    "Kingsmead",
    "Darren Sammy National Cricket Stadium",
    "Basin Reserve",
    "Central Broward Regional Park",
    "Seddon Park",
    "SuperSport Park",
    "Old Trafford",
    "Sheikh Zayed Stadium",
    "Wankhede Stadium",
    "Brabourne Stadium",
    "Trent Bridge",
    "Rose Bowl (Ageas Bowl)",
    "Bay Oval",
    "Zahur Ahmed Chowdhury Stadium",
    "Eden Gardens",
    "Gaddafi Stadium",
    "Arun Jaitley Stadium",
    "Vidarbha Cricket Association Stadium",
    "Punjab Cricket Association Stadium (Mohali)",
    "Adelaide Oval",
    "M. Chinnaswamy Stadium",
    "Warner Park",
    "Sophia Gardens",
    "Hagley Oval",
    "Queen's Park Oval"
]
app = Flask(__name__)
app.secret_key = 'your_secret_key'
def init_db():
    con = sqlite3.connect("users.db")
    c = con.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT 0 NOT NULL
        )
    """)
    con.commit()
    con.close()
init_db()
def init_feedback_db():
    con = sqlite3.connect("feedback.db")
    c = con.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at DATE DEFAULT (DATE('now'))
        )
    """)
    con.commit()
    con.close()
init_feedback_db()
@app.route('/', methods=['GET'])
def home():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    username = session.get('username', 'Guest')
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        greeting = "Good Morning"
    elif 12 <= current_hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"
    return render_template('Home.html', username=username, greeting=greeting)
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        con = sqlite3.connect('users.db')
        c = con.cursor()
        statement = "SELECT * FROM users WHERE username = ? AND password = ?"
        c.execute(statement, (username, password))
        user=c.fetchone()
        if not user:
            return render_template('Login.html', error="Invalid credentials. Please try again.")
        else:
            session['logged_in'] = True
            session['username'] = username
            session['is_admin'] = user[4]
            return redirect(url_for('home'))
    return render_template('login.html')
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        con = sqlite3.connect('users.db')
        c = con.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = c.fetchone()
        if existing_user:
            return render_template('signup.html', error="Username already exists. Please try a different one.")
        is_admin = 1 if username == 'admin' else 0
        try:
            c.execute("INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)",
                      (username, email, password, is_admin))
            con.commit()
            return redirect(url_for('login'))
        except Exception as e:
            con.rollback()
            return render_template('signup.html', error="An error occurred. Please try again.")
        finally:
            con.close()
    return render_template('signup.html')
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['password']
        con = sqlite3.connect('users.db')
        c = con.cursor()
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        if user:
            c.execute("UPDATE users SET password = ? WHERE email = ?", (new_password, email))
            con.commit()
            con.close()
            return redirect(url_for('login'))
        else:
            con.close()
            return render_template('forgot.html', error="Email not found.")
    return render_template('forgot.html')
@app.route('/T20home',methods=['GET'])
def T20home():
    return render_template('T20home.html')
@app.route('/T20home/Score', methods=['GET', 'POST'])
def Score():
    prediction = None
    if request.method == 'POST':
        batting_team = request.form['batting_team']
        bowling_team = request.form['bowling_team']
        city = request.form['city']
        current_score = int(request.form['current_score'])
        overs = float(request.form['overs'])
        wickets = int(request.form['wickets'])
        last_five = int(request.form['last_five'])
        balls_left = 120 - (overs * 6)
        wickets_left = 10 - wickets
        current_run_rate = current_score / overs
        input_df = pd.DataFrame(
            {'batting_team': [batting_team], 
             'bowling_team': [bowling_team], 
             'city': [city], 
             'current_score': [current_score], 
             'balls_left': [balls_left], 
             'wicket_left': [wickets_left], 
             'current_run_rate': [current_run_rate], 
             'last_five': [last_five]}
        )
        result = pipe.predict(input_df)
        prediction = int(result[0])
    return render_template('T20Score.html', 
                           teams=sorted(teams), 
                           cities=sorted(cities), 
                           prediction=prediction)
def encode_input(value, mapping, encoder=None):
    if encoder:
        if value in encoder.classes_:
            return encoder.transform([value])[0]
        else:
            print(f"Warning: Unknown category '{value}' encountered. Encoding as -1.")
            return -1
    return mapping.get(value, -1)
@app.route('/T20home/MatchDetails', methods=['GET', 'POST'])
def MatchDetails():
    team1_mapping = {team: idx for idx, team in enumerate(teams)}
    team2_mapping = {team: idx for idx, team in enumerate(teams)}
    toss_winner_mapping = {team: idx for idx, team in enumerate(teams)}
    winner_mapping = {team: idx for idx, team in enumerate(teams)}
    toss_decision_mapping = {"bat": 0, "field": 1}
    prediction = None
    team1 = team2 = None
    if request.method == 'POST':
        try:
            team1 = request.form.get('team1')
            team2 = request.form.get('team2')
            toss_winner = request.form.get('toss')
            venue = request.form.get('venue')
            city = request.form.get('city')
            toss_decision = request.form.get('toss_decision')
            team1_encoded = encode_input(team1, team1_mapping)
            team2_encoded = encode_input(team2, team2_mapping)
            toss_winner_encoded = encode_input(toss_winner, toss_winner_mapping)
            venue_encoded = encode_input(venue, None, le_venue)
            city_encoded = encode_input(city, None, le_city)
            toss_decision_encoded = encode_input(toss_decision, toss_decision_mapping)
            print(f"Encoded inputs: team1={team1_encoded}, team2={team2_encoded}, toss_winner={toss_winner_encoded}, venue={venue_encoded}, city={city_encoded}, toss_decision={toss_decision_encoded}")
            if -1 in {team1_encoded, team2_encoded, toss_winner_encoded, venue_encoded, city_encoded, toss_decision_encoded}:
                raise ValueError("Invalid input data. Please check your selections.")
            input_df = pd.DataFrame({
                'team1': [team1_encoded],
                'team2': [team2_encoded],
                'venue': [venue_encoded],
                'toss_winner': [toss_winner_encoded],
                'city': [city_encoded],
                'toss_decision': [toss_decision_encoded]
            })
            result = loaded_model.predict(input_df)
            prediction_encoded = round(result[0])
            print(f"Model prediction: {prediction_encoded}")
            if prediction_encoded == team1_encoded:
                winner = team1
            elif prediction_encoded == team2_encoded:
                winner = team2
            else:
                winner = random.choice([team1, team2])
            return render_template('Match.html', teams=teams, venues=le_venue.classes_, cities=le_city.classes_, prediction=winner,selected_team1=team1, selected_team2=team2)
        except Exception as e:
            error_msg = traceback.format_exc()
            print(f"Error occurred: {error_msg}")
            return render_template('Match.html', prediction="Error processing the input.", teams=teams, venues=le_venue.classes_, cities=le_city.classes_,selected_team1=team1, selected_team2=team2)
    else:
        return render_template('Match.html', teams=teams, venues=le_venue.classes_, cities=le_city.classes_, prediction=None)
@app.route('/IPLhome',methods=['GET'])
def IPLhome():
    return render_template('IPLhome.html')
@app.route('/IPLhome/score', methods=['GET', 'POST'])
def ipl():
    prediction = None
    if request.method == 'POST':
        batting_team = request.form['batting_team']
        bowling_team = request.form['bowling_team']
        city = request.form['city']
        current_score = int(request.form['current_score'])
        overs = float(request.form['overs'])
        wickets = int(request.form['wickets'])
        last_five = int(request.form['last_five'])
        balls_left = 120 - (overs * 6)
        wickets_left = 10 - wickets
        current_run_rate = current_score / overs
        input_df = pd.DataFrame(
            {'batting_team': [batting_team], 
             'bowling_team': [bowling_team], 
             'city': [city], 
             'current_score': [current_score], 
             'balls_left': [balls_left], 
             'wicket_left': [wickets_left], 
             'current_run_rate': [current_run_rate], 
             'last_five': [last_five]}
        )
        result = pipe.predict(input_df)
        prediction = int(result[0])
    return render_template('IPL.html', 
                           teams=sorted(iteams), 
                           cities=sorted(icities), 
                           prediction=prediction)
@app.route('/IPLhome/IPLMatch', methods=['GET', 'POST'])
def IPLMatch():
    encode['toss_decision'] = {
        'bat': 0,
        'field': 1
    }
    prediction = None
    if request.method == 'POST':
        try:
            team1 = request.form['team1']
            team2 = request.form['team2']
            toss_winner = request.form['toss']
            venue = request.form['venue']
            city = request.form['city']
            toss_decision = request.form['toss_decision']
            team1_encoded = encode['team1'].get(team1, -1)
            team2_encoded = encode['team2'].get(team2, -1)
            toss_winner_encoded = encode['toss_winner'].get(toss_winner, -1)
            venue_encoded = (
                le_venue.transform([venue])[0] if venue in le_venue.classes_ else -1
            )
            city_encoded = (
                le_city.transform([city])[0] if city in le_city.classes_ else -1
            )
            toss_decision_encoded = encode['toss_decision'].get(toss_decision, -1)
            input_df = pd.DataFrame({
                'team1': [team1_encoded],
                'team2': [team2_encoded],
                'venue': [venue_encoded],
                'toss_winner': [toss_winner_encoded],
                'city': [city_encoded],
                'toss_decision': [toss_decision_encoded]
            })
            result = loaded_model.predict(input_df)
            prediction_encoded = round(result[0])
            if prediction_encoded == team1_encoded:
                winner = team1
            elif prediction_encoded == team2_encoded:
                winner = team2
            else:
                winner = random.choice([team1, team2])
            return render_template(
                'IPLMatch.html',
                teams=list(encode['team1'].keys()),
                venues=le_venue.classes_,
                cities=le_city.classes_,
                prediction=winner,
                selected_team1=team1,
                selected_team2=team2
            )
        except Exception as e:
            print(f"Error occurred: {e}")
            return render_template(
                'IPLMatch.html',
                prediction="Error processing the input.",
                teams=list(encode['team1'].keys()),
                venues=le_venue.classes_,
                cities=le_city.classes_,
                selected_team1=team1,
                selected_team2=team2
            )
    return render_template(
        'IPLMatch.html',
        teams=list(encode['team1'].keys()),
        venues=le_venue.classes_,
        cities=le_city.classes_,
    )
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        username = session.get('username', 'Guest')
        email = request.form['email']
        message = request.form['message']
        con = sqlite3.connect('feedback.db')
        c = con.cursor()
        c.execute("INSERT INTO feedback (username, email, message) VALUES (?, ?, ?)",
                  (username, email, message))
        con.commit()
        con.close()
        session['feedback_submitted'] = True
        return redirect(url_for('feedback'))
    feedback_submitted = session.get('feedback_submitted', False)
    session.pop('feedback_submitted', None)
    return render_template('feedback.html', feedback_submitted=feedback_submitted)
@app.route('/view_feedback', methods=['GET'])
def view_feedback():
    if 'logged_in' not in session or session.get('is_admin') != 1:
        return redirect(url_for('login'))
    con = sqlite3.connect('feedback.db')
    c = con.cursor()
    c.execute("SELECT * FROM feedback ORDER BY created_at DESC")
    feedbacks = c.fetchall()
    con.close()
    return render_template('view_feedback.html', feedbacks=feedbacks)
@app.route('/Logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('is_admin', None)
    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True)

