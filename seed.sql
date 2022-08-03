
DROP DATABASE IF EXISTS nbapi;

CREATE DATABASE nbapi;

\c nbapi




CREATE TABLE nba_teams
(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    full_name TEXT NOT NULL,
    abbreviation TEXT NOT NULL,
    city TEXT NOT NULL,
    conference TEXT NOT NULL,
    division TEXT NOT NULL
);



CREATE TABLE nba_players
(
    id SERIAL PRIMARY KEY,
    individual_id VARCHAR,
    player_firstname TEXT NOT NULL,
    player_lastname TEXT NOT NULL,
    height_feet VARCHAR,
    height_inches VARCHAR, 
    weight VARCHAR,
    position TEXT NOT NULL,
    
   
    );


CREATE TABLE player_game_stats
(
    id SERIAL PRIMARY KEY,
    points_per_game DECIMAL(4,2) NOT NULL,
    assists_per_game DECIMAL(4,2) NOT NULL,
    rebounds_per_game DECIMAL(4,2) NOT NULL,
    blocks_per_game DECIMAL(4,2) NOT NULL,
    field_goal_percentage DECIMAL(5,2) NOT NULL
);


CREATE TABLE photo_info
(
    id SERIAL PRIMARY KEY,
    player_first_name TEXT NOT NULL,
    player_last_name TEXT NOT NULL,
    player_photo_id VARCHAR

);


   







