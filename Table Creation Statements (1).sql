CREATE TABLE team_loc (
  city_id SERIAL PRIMARY KEY,
  city varchar(250) NOT NULL,
  state_prov varchar(250) NOT NULL,
  country varchar(250) NOT NULL
  );

CREATE TABLE team (
  team_id varchar (250) PRIMARY KEY,
  team_name varchar(250) NOT NULL,
  team_city_id INT references team_loc(city_id) NOT NULL,
  founded INT NOT NULL,
  joined INT NOT NULL,
  arena varchar(250) NOT NULL,
  arena_cap INT NOT NULL
);

/*CREATE TABLE player_stats (
  player_stats_id varchar(250) PRIMARY KEY,
  player_id varchar(250) references
  games INT,
  goals INT,
  assists INT,
  points INT,
  points_per_60 INT
);*/

CREATE TABLE birth_loc (
  birth_loc_id SERIAL PRIMARY KEY,
  city varchar(250) NOT NULL,
  state_prov varchar(250),
  country varchar(250) NOT NULL
);

CREATE TABLE position (
  pos_id varchar(2) PRIMARY KEY,
  pos_name varchar(250) NOT NULL,
  role varchar(250) NOT NULL
);

CREATE TABLE injury (
  injury_id SERIAL PRIMARY KEY,
  injury_name varchar(250) NOT NULL
);

CREATE TABLE player (
  player_id SERIAL PRIMARY KEY,
  team_id varchar(250) references team(team_id) NOT NULL,
  fname varchar(250) NOT NULL,
  lname varchar(250) NOT NULL,
  jersey_num INT NOT NULL,
  dob timestamp NOT NULL,
  age INT NOT NULL,
  birth_loc_id INT references birth_loc(birth_loc_id) NOT NULL,
  height INT NOT NULL,
  weight INT NOT NULL,
  hand varchar(1),
  draft varchar(250),
  draft_round varchar(250),
  draft_rank varchar(250),
  rookie varchar(1),
  pos_id varchar(2) references position(pos_id) NOT NULL,
  games_played INT NOT NULL,
  goals_made INT NOT NULL,
  assists_made INT NOT NULL,
  first_assists_made INT NOT NULL,
  total_points_scored INT NOT NULL,
  plus_minus INT NOT NULL,
  total_shots_made INT NOT NULL,
  total_shots_missed INT NOT NULL,
  shots_taken_blocked INT NOT NULL,
  goals_per_shots varchar(250) NOT NULL,
  minutes_on_ice INT NOT NULL,
  minuites_on_ice_per_game varchar(250) NOT NULL, --TYPE ON MINUTES
  minutes_on_ice_per_shift varchar(250) NOT NULL,
  shifts INT NOT NULL,
  shifts_per_game varchar(250) NOT NULL,
  passes INT NOT NULL,
  passes_per_60 varchar(250) NOT NULL,
  faceoffs_won INT NOT NULL,
  faceoffs_lost INT NOT NULL,
  faceoffs_winning_percentage varchar(250)NOT NULL,
  hits_recieved INT NOT NULL,
  hits_recieved_per_60 varchar(250) NOT NULL,
  hits_given INT NOT NULL,
  hits_given_per_60 varchar(250) NOT NULL,
  blocked_shots INT NOT NULL,
  blocked_shots_per_60 varchar(250) NOT NULL,
  giveaways INT NOT NULL,
  giveaways_per_60 varchar(250) NOT NULL,
  takeaways INT NOT NULL,
  takeaways_per_60 varchar(250) NOT NULL,
  penalties_in_minutes INT NOT NULL,
  minor_penalties_taken INT NOT NULL,
  major_penalties_taken INT NOT NULL,
  misconducts INT NOT NULL,
  game_misconducts INT NOT NULL,
  match_penalties INT NOT NULL,
  grit INT NOT NULL,
  shootout_shots_taken varchar(250),
  shootout_shots_made varchar(250),
  shootout_shots_ratio varchar(250),
  first_goal_of_game INT NOT NULL,
  overtime_goals INT NOT NULL,
  game_winning_goals INT NOT NULL,
  empty_net_goals INT NOT NULL,
  backhand_goals INT NOT NULL,
  deflected_goals INT NOT NULL,
  slapshot_goals INT NOT NULL,
  snapshot_goals INT NOT NULL,
  tipped_goals INT NOT NULL,
  wraparound_goals INT NOT NULL,
  wristshot_goals INT NOT NULL,
  penaltyshot_goals INT NOT NULL,
  penaltyshot_taken INT NOT NULL,
  pentalshot_ratio varchar(250) NOT NULL, -- TYPE in PENALTY
  avg_distance_shot varchar(250) NOT NULL,
  hit_crossbar INT NOT NULL,
  hit_post INT NOT NULL,
  over_net INT NOT NULL,
  wide_net INT NOT NULL,
  backhand_shot INT NOT NULL,
  deflected_shot INT NOT NULL,
  slapshots INT NOT NULL,
  snapshots INT NOT NULL,
  tipped_shots INT NOT NULL,
  wraparound_shots INT NOT NULL,
  wrist_shots INT NOT NULL,
  first_star INT NOT NULL,
  second_star INT NOT NULL,
  third_star INT NOT NULL,
  salary_days INT NOT NULL,
  salary varchar(250) NOT NULL,
  cap_hit varchar(250) NOT NULL,
  cap_cost varchar(250) NOT NULL,
  bonuses varchar(250) NOT NULL
);

CREATE TABLE player_injury (
  player_id INT references player(player_id) NOT NULL,
  injury_id INT references injury(injury_id) NOT NUll
);
