# Eric Kha
# Info 340D
# Lab 5 Python code
import csv

# import the postgres module
import psycopg2

# import goodies to make SELECT statments eai ser
# Returns values from a SELECT as a dictionary. Yay!
from psycopg2.extras import DictCursor

#import codecs to fix UTF-8 problem
import codecs
# Connect to the database using the dictionary cursor
conn = psycopg2.connect("dbname=tbarn2 user=tbarn2")

# Autocommit -- If your inserts are not saving then you forgot this line!
# Otherside you need to issue a conn.commit() before ending the script
# conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

# Create a cursor
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# open our data file
csvfile = codecs.open('nhl.csv', encoding='utf-8', mode='r')
csvfile2 = codecs.open('teams.csv', encoding='utf8', errors='ignore', mode='r')
csvfile3 = codecs.open('positions.csv', encoding='utf8', errors='ignore', mode='r')

datareader = csv.DictReader(csvfile, delimiter=',')
datareader2 = csv.DictReader(csvfile2, delimiter=',')
datareader3 = csv.DictReader(csvfile3, delimiter=',')

try:
    # Loop through each line of the data for Position csv file
    for row in datareader3:
        # Checks to see if the position_id is in db alredady
        pos = row['ID']
        cur.execute('SELECT pos_id FROM position WHERE pos_id = %s', (pos,))
        pos = cur.fetchone()
        if pos is None:
            # Populate position table
            cur.execute("INSERT INTO position (pos_id, pos_name, role) VALUES (%s, %s, %s) RETURNING pos_id", (row['ID'], row['Name'], row['Role']))

    # loop through each line of the data for Teams csv file
    for row in datareader2:
        # Checks to see if team_city is in db already
        location = row['City']
        cur.execute('SELECT city_id FROM team_loc where city = %s', (location,))
        location = cur.fetchone()
        if location is None:
            # Populate tean_loc table
            cur.execute("INSERT INTO team_loc (city, state_prov, country) VALUES (%s, %s, %s) RETURNING city_id", (row['City'], row['S/P'], row['Country']))
            location = cur.fetchone()

        # Checks to see if team is in db already
        team_id = row['ID']
        cur.execute('SELECT team_id FROM team where team_id = %s', (team_id, ))
        team_id = cur.fetchone()
        if team_id is None:
            #populate teams table
            cur.execute("INSERT INTO team(team_id, team_name, team_city_id, founded, joined, arena, arena_cap) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING team_id", (row['ID'], row['Name'], location[0], row['Founded'], row['Joined'], row['Arena'], row['Arena Capacity']))

    # loop through each line of the data for Main csv file
    for row in datareader:
        row['team/location/sp'] = row['team/location/sp'] if 'team/location/sp' in row else None
        row['player/sp'] = row['player/sp'] if 'player/sp' in row else None
        ShootOutShotsTaken = row['ShootOutShotsTaken'] if 'ShootOutShotsTaken' in row else 0
        ShootoutGoals = row['ShootoutGoals'] if 'ShootoutGoals' in row else 0
        SO = row['SO%'] if 'SO%' in row else 0
        HitsReceived = row['HitsReceived'] if 'HitsReceived' in row else None

        # Birth_loc
        #Checks to see if the city/country combination is in the db already
        birth_city = row['player/birth_city']
        birth_state = row['player/sp']
        birth_country = row['player/country']
        cur.execute('SELECT birth_loc_id FROM birth_loc WHERE city = %s AND state_prov = %s AND country = %s', (birth_city, birth_state, birth_country))
        birth_id = cur.fetchone()
        if birth_id is None:
            # populate birth_loc table
            cur.execute('INSERT INTO birth_loc(city, state_prov, country) VALUES (%s, %s, %s) RETURNING birth_loc_id', (row['player/birth_city'], row['player/sp'], row['player/country']))
            birth_id = cur.fetchone()

        # PLAYER
        #Checks to see if the player is the in the db already
        player = row['ID']
        cur.execute('SELECT player_id FROM player WHERE player_id = %s', (player,))
        player = cur.fetchone()
        if player is None:
            draft_year = row['Draft'] if 'Draft' in row else None
            draft_round = row['Round'] if 'Round' in row else None
            overall = row['Overall'] if 'Overall' in row else None
            blocked = row['Blocked'] if 'Blocked' in row else None

            # Populate player table

            cur.execute('INSERT INTO player (team_id, fname, lname, jersey_num, dob, age, birth_loc_id, height, weight, hand, draft, draft_round, draft_rank, rookie, pos_id, games_played, goals_made, assists_made, first_assists_made, total_points_scored, plus_minus, total_shots_made, total_shots_missed, shots_taken_blocked, goals_per_shots, minutes_on_ice, minuites_on_ice_per_game, minutes_on_ice_per_shift, shifts, shifts_per_game, passes, passes_per_60, faceoffs_won, faceoffs_lost, faceoffs_winning_percentage, hits_recieved, hits_recieved_per_60, hits_given, hits_given_per_60, blocked_shots, blocked_shots_per_60, giveaways, giveaways_per_60, takeaways, takeaways_per_60, penalties_in_minutes, minor_penalties_taken, major_penalties_taken, misconducts, game_misconducts, match_penalties, grit, shootout_shots_taken, shootout_shots_made, shootout_shots_ratio, first_goal_of_game, overtime_goals, game_winning_goals, empty_net_goals, backhand_goals, deflected_goals, slapshot_goals, snapshot_goals, tipped_goals, wraparound_goals, wristshot_goals, penaltyshot_goals, penaltyshot_taken, pentalshot_ratio, avg_distance_shot, hit_crossbar, hit_post, over_net, wide_net, backhand_shot, deflected_shot, slapshots, snapshots, tipped_shots, wraparound_shots, wrist_shots, first_star, second_star, third_star, salary_days, salary, cap_hit, cap_cost, bonuses) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING player_id',
            (row['Team/team_id'], row['First Name'], row['Last Name'], row['Num'], row['DOB'], row['Age'], birth_id[0], row['HT'], row['Wt'], row['S'], draft_year, draft_round,
            overall, row['Rk'], row['player/pos_id'], row['GP'], row['G'], row['A'], row['A1'], row['PTS'], row['+/-'], row['Sh'], row['Misses'], blocked, row['Sh%'], row['TOI'],
            row['TOI/G'], row['TOI/Sh'], row['Shifts'], row['Sh/G'], row['Passes'], row['Pa/60'], row['FOW'], row['FOL'], row['FO%'], HitsReceived, row['HitsRecieved/60'], row['HitsGiven'], row['HitsGiven/60'], row['BlockedShots'], row['Blocks/60'],
            row['GiveAways'], row['Giveaways/60'], row['TakeAways'], row['Takeaways/60'], row['PIM'], row['Minor'], row['Major'], row['Misconducts'], row['Game Misconducts'], row['Match'], row['Grit'], ShootOutShotsTaken, ShootoutGoals, SO, row['1G'], row['OTG'],
            row['GWG'], row['ENG'], row['BHG'], row['DeflG'], row['SlapG'], row['SnapG'], row['TipG'], row['WrapG'], row['WristG'], row['PenaltyShotGoals'], row['PenaltyShotsTaken'], row['PenaltyShot%'], row['ShotDist'], row['Crossbar'],
            row['Post'], row['OverNet'], row['WideOfNet'], row['Backhand'], row['Deflected'], row['Slap'], row['Snap'], row['Tipped'], row['Wraparound'], row['Wrist'], row['1st Star'], row['2nd Star'], row['3rd Star'], row['salary_Days'],
            row['Salary'], row['Cap Hit'], row['Cap Cost'], row['Bonuses']))
            player = cur.fetchone()

        #INJURIES
        injuries = [row['injury/Injury1'], row['injury/Injury2'], row['injury/Injury3'], row['injury/Injury4']]
        # For each injuries in the table
        for injury in injuries:
            #Checks if not null
            if injury != '':
                # Check if its in the injury table
                cur.execute('SELECT injury_id FROM injury WHERE injury_name = %s', (injury, ))
                isInjured = cur.fetchone()
                # IF injury is NOT in table already
                if isInjured is None:
                    # Populate Injury table
                    cur.execute('INSERT INTO injury (injury_name) VALUES (%s) RETURNING injury_id', (injury,))
                    isInjured = cur.fetchone()
                #Populate associative entity
                cur.execute('INSERT INTO player_injury (player_id, injury_id) VALUES (%s, %s)', (player[0], isInjured[0]))

except psycopg2.DatabaseError, e:
    #a transaction failed, so rollback all transactions and print error(s)
    conn.rollback()
    print 'Error %s' % e

finally:
    if conn:
        #close the database connection (for security)
        conn.commit()
        conn.close()
