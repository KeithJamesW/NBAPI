import os
import psycopg2
from data_pull import cursor
from flask_sqlalchemy import SQLAlchemy  
from flask import Flask, request, abort, jsonify, render_template


   

app = Flask(__name__)


DB_USER = os.environ.get('HEROKU_DB_USER', 'lpjlpbcnqqtpmz')
DB_PASSWORD = os.environ.get('HEROKU_DB_PASSWORD', 'e55eacfef4a7efe891ee38416f1696148519b5d855c3573e35a16e521e51deb9')
DB_HOST = os.environ.get('HEROKU_DB_HOST', 'ec2-3-219-52-220.compute-1.amazonaws.com')
DB_HOST_IP = os.environ.get('HEROKU_DB_HOST_IP', '23.252.62.110')
DB_PORT = os.environ.get('HEROKU_DB_PORT', 5432)
DB_NAME = os.environ.get('HEROKU_DB_NAME', 'dbuljv1eqq4so7')

DATABASE_URL = os.environ.get('HEROKU_DB_URL', f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()




@app.route('/', methods=['GET'])
def home():
       
    return render_template("index.html")




@app.route("/players")
def db_read():
    
    
    player_ids = [("Giannis", "203507"),("Kevin", "201142"), ("Stephen", "201939"), ("Nikola", "203999"), 
    ("Joel", "203954"), ("Jayson", "1628369"), ("Luka", "1629029"), ("LeBron", "2544"), 
    ("Kawhi", "202695"), ("Ja", "1629630"), ("Devin", "1626164"), ("Jimmy", "202710"), ("James","201935"), 
    ("Karl-Anthony", "1626157"), ("Trae", "1629027"), ("Anthony", "203076"), ("Donovan", "1628378"), 
    ("Damian", "203081"), ("Bradley", "203078"), ("Paul", "202331")] 
    player_query = cursor.execute(f'SELECT individual_id, player_firstname, player_lastname, height_feet, height_inches, weight, position from nba_players;')
    results1 = cursor.fetchall()
    team_query = cursor.execute(f'SELECT full_name, conference, division from nba_teams;')
    result = cursor.fetchall()
    stats_query = cursor.execute(f'SELECT points_per_game, assists_per_game, rebounds_per_game, blocks_per_game, field_goal_percentage from player_game_stats;')
    results2 = cursor.fetchall()
    total_results= zip(result, results1, player_ids, results2)
    listed_results = list(total_results)
    print(listed_results)
    
    
    
    return render_template("", "200 OK", "players.html", player_ids=player_ids, result=result, results1=results1, results2=results2, listed_results=listed_results, total_results= zip(result, results1, player_ids, results2))  
   



    

    
    
   
    






