from http.client import OK
import json
from operator import contains
import requests
import csv
import os
import psycopg2


DB_USER = os.environ.get('HEROKU_DB_USER', 'lpjlpbcnqqtpmz')
DB_PASSWORD = os.environ.get('HEROKU_DB_PASSWORD', 'e55eacfef4a7efe891ee38416f1696148519b5d855c3573e35a16e521e51deb9')
DB_HOST = os.environ.get('HEROKU_DB_HOST', 'ec2-3-219-52-220.compute-1.amazonaws.com')
DB_HOST_IP = os.environ.get('HEROKU_DB_HOST_IP', '23.252.62.110')
DB_PORT = os.environ.get('HEROKU_DB_PORT', 5432)
DB_NAME = os.environ.get('HEROKU_DB_NAME', 'dbuljv1eqq4so7')

DATABASE_URL = os.environ.get('HEROKU_DB_URL', f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()




def request(url, headers, method='GET'):
  try:
    r = requests.request(method=method, headers=headers, url=url)
    if r.status_code == 200:
      r.status_message = OK
      return r.json()
    else:
      return {'error_status': r.status_code, 'error_message': r.text}
  except Exception as e:
    return {'error_status': 500, 'error_message': str(e)}


def request_stats(url, method='GET'):
  try:
    r = requests.request(method=method, url=url)
    if r.status_code == 200:
      return r.json()
    else:
      return {'error_status': r.status_code, 'error_message': r.text}
  except Exception as e:
    return {'error_status': 500, 'error_message': str(e)}


def parse_data(response, player_name):
  if not response or not response.get('data'):
    print(f'API error - empty results for {player_name}.')
    return
  if response.get('error_status'):
    print(f'API error - for {player_name}, error message: {response["error_message"]}, error status: {response["error_status"]}.')
    return
  return response['data'][0]


def parse_stats_data(response, player_individual_id):
  if not response or not response.get('data'):
    print(f'API error - empty results for {player_individual_id}.')
    return
  if response.get('error_status'):
    print(f'API error - for {player_individual_id}, error message: {response["error_message"]}, error status: {response["error_status"]}.')
    return
  return response['data']


player_individual_ids = []
def insert_query_for_nba_players_table(data):
  
  individual_id = data['id']
  player_individual_ids.append(individual_id)
  player_firstname = data['first_name']
  player_lastname = data['last_name']
  player_height_feet = data['height_feet']
  player_height_inches = data['height_inches']
  player_weight_pounds = data['weight_pounds']
  player_position = data['position']
  nba_player_insert_query = f"INSERT INTO nba_players(individual_id, player_firstname, player_lastname, height_feet, height_inches, weight, position) VALUES ('{individual_id}', '{player_firstname}', '{player_lastname}', '{player_height_feet}', '{player_height_inches}', '{player_weight_pounds}', '{player_position}');"
  return nba_player_insert_query

player_ids = []

def insert_query_for_nba_teams_table(data):
  
  team_id = data['team']['id']
  player_ids.append(team_id)
  team_name = data['team']['name']
  team_full_name = data['team']['full_name']
  team_abbreviation = data['team']['abbreviation']
  team_city = data['team']['city']
  team_conference = data['team']['conference']
  team_division = data['team']['division']
  nba_teams_insert_query = f"INSERT INTO nba_teams(name, full_name, abbreviation, city, conference, division) VALUES ('{team_name}', '{team_full_name}', '{team_abbreviation}', '{team_city}', '{team_conference}', '{team_division}');"
  return nba_teams_insert_query


def insert_query_for_nba_player_stats_table(data):
  
  points_per_game = data[0]['pts']
  assists_per_game = data[0]['ast']
  rebounds_per_game = data[0]['dreb'] + data[0]['oreb']
  blocks_per_game = data[0]['blk']
  field_goal_percentage = data[0]['fg_pct']
  nba_stats_insert_query = f"INSERT INTO player_game_stats(points_per_game, assists_per_game, rebounds_per_game, blocks_per_game, field_goal_percentage) VALUES('{points_per_game}', '{assists_per_game}', '{rebounds_per_game}', '{blocks_per_game}', '{field_goal_percentage}');"   
  
  return nba_stats_insert_query





def pull_data_from_api():
  
  headers = {
	"X-RapidAPI-Key": "b82a4c582fmshe3e828826086ba4p107028jsn4248d3335c3d",
	"X-RapidAPI-Host": "free-nba.p.rapidapi.com"
}

  nba_players = ["Giannis+Antetokounmpo", "Kevin+Durant", "Stephen+Curry", "Nikola+Jokic",
                "Joel+Embiid", "Jayson+Tatum", "Luka+Doncic", "Lebron+James", "Kawhi+Leonard", "Ja+Morant", 
                "Devin+Booker", "Jimmy+Butler", "James+Harden", "Karl-Anthony+Towns", "Trae+Young", 
                "Anthony+Davis", "Donovan+Mitchell", "Damian+Lillard", "Bradley+Beal", "Paul+George"]

  insert_queries_dict = dict()
  n = len(nba_players)

  for idx, player_name in enumerate(nba_players):
    insert_queries_dict[player_name] = dict()
    url = f"https://free-nba.p.rapidapi.com/players?search={player_name}"
    response = request(url, headers)
    data = parse_data(response=response, player_name=player_name)
    if data:
     
      nba_player_insert_query = insert_query_for_nba_players_table(data)
      nba_teams_insert_query = insert_query_for_nba_teams_table(data)
      insert_queries_dict[player_name]['nba_player_insert_query'] = nba_player_insert_query
      insert_queries_dict[player_name]['nba_teams_insert_query'] = nba_teams_insert_query
      print(f'({idx+1}/{n}) Processed insert query for {player_name}...')
  
  return insert_queries_dict



def pull_stats_data_from_api():

  insert_queries_dict = dict()
  n = len(player_ids)


  for idx, player_individual_id in enumerate(player_individual_ids):
    insert_queries_dict[player_individual_id] = dict()
    url = f"https://www.balldontlie.io/api/v1/season_averages?player_ids[]={player_individual_id}"
    response = request_stats(url)
    
    data = parse_stats_data(response=response, player_individual_id=player_individual_id)
    if data:

      nba_stats_insert_query = insert_query_for_nba_player_stats_table(data)
      insert_queries_dict[player_individual_id]['nba_stats_insert_query'] = nba_stats_insert_query
      print(f'({idx+1}/{n}) Processed insert query for {player_individual_id}...')
  
  return insert_queries_dict





def push_data_into_heroku_db(insert_queries):

  for query in insert_queries.keys():
    cursor.execute(insert_queries.get(query)['nba_player_insert_query'],())

  for query in insert_queries.keys():
    cursor.execute(insert_queries.get(query)['nba_teams_insert_query'],())

    
 
    pass

def push_stat_data_into_heroku_db(insert_stat_queries):
  
  keyToFind = 'nba_stats_insert_query'
  
  for query in insert_stat_queries.keys():
    if keyToFind in insert_stat_queries.get(query):
      cursor.execute(insert_stat_queries.get(query)['nba_stats_insert_query'])

    


    pass





if __name__ == '__main__':
  insert_queries = pull_data_from_api()
  insert_stat_queries = pull_stats_data_from_api()
  push_stat_data_into_heroku_db(insert_stat_queries)
  push_data_into_heroku_db(insert_queries)
  conn.commit()