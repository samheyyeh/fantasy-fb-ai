#!/usr/bin/env python3

import pandas as pd
import numpy as np
from collections import Counter

df = pd.read_csv('player_data_ordered.csv')

NUM_TEAMS = int(input("Enter the number of teams in the draft: "))
ROUNDS = int(input("Enter the number of rounds in the draft: "))
USER_PICK = int(input("Enter your pick position (1-{}): ".format(NUM_TEAMS)))
NUM_SIMULATIONS = 500
MARGIN = 0.015 # 1.5% randomness

POSITION_PRIORITIES = {
    'R1': ['WR', 'RB'],
    'R2': ['WR', 'RB'],
    'R3': ['WR', 'RB'],
    'R4': ['WR', 'RB'],
    'R5': ['TE'],
    'R6': ['QB'],
    'R7': ['TE'],
    'R8': ['QB'],
    'R9': ['WR', 'RB'],
    'R10': ['WR', 'RB'],
    'R11': ['WR', 'RB'],
    'R12': ['WR', 'RB'],
    'R13': ['WR', 'RB'],
    'R14': ['WR', 'RB'],
    'R15': ['WR', 'RB'],
    'R16': ['WR', 'RB'],
    'R17': ['K'],
    'R18': ['DST'],
}

def prioritize_players(players, position):
    if position in ['WR', 'TE']:
        players = players.sort_values(by=['receiving_yards', 'receiving_data'], ascending=False)
    elif position == 'RB':
        players = players.sort_values(by=['rushing_yards', 'rushing_data', 'receiving_data'], ascending=False)
    elif position == 'QB':
        players = players.sort_values(by=['passing_data', 'rushing_yards'], ascending=False)
    elif position == 'K':
        players = players.sort_values(by='projected_points', ascending=False)
    elif position == 'DST':
        players = players.sort_values(by='projected_points', ascending=False)
    else:
        players = players.sort_values(by='projected_draft_position')
    return players

def simulate_draft():
    available_players = df.copy()
    team_drafts = [[] for _ in range(NUM_TEAMS)]
    team_limits = [{'QB': 0, 'DST': 0, 'K': 0} for _ in range(NUM_TEAMS)]
    
    for round_num in range(1, ROUNDS + 1):
        if round_num == 10:
            current_positions = POSITION_PRIORITIES['R10']
        elif round_num == 12:
            current_positions = POSITION_PRIORITIES['R12']
        else:
            round_key = f'R{round_num if round_num <= 4 else 8}'
            current_positions = POSITION_PRIORITIES[round_key]

        available_players = available_players.sample(frac=1).reset_index(drop=True)
        
        for team in range(NUM_TEAMS):
            if available_players.empty:
                break
            
            filtered_players = available_players[available_players['position'].str.contains('|'.join(current_positions))]
            if filtered_players.empty:
                filtered_players = available_players
            
            if filtered_players.empty:
                continue
            
            draft_margin = int(len(filtered_players) * MARGIN)
            draft_margin = max(draft_margin, 1)
            
            filtered_players['draft_order'] = filtered_players['projected_draft_position']
            filtered_players = filtered_players.sort_values(by='draft_order')
            
            if len(filtered_players) > 0:
                pick_index = np.random.randint(0, min(draft_margin, len(filtered_players)))
                pick = filtered_players.iloc[pick_index]
                available_players = available_players.drop(available_players.index[available_players.index.get_loc(pick.name)])
                
                team_drafts[team].append(pick['player_name'])
                if pick['position'] in team_limits[team]:
                    team_limits[team][pick['position']] += 1
    
    return team_drafts

draft_results = [simulate_draft() for _ in range(NUM_SIMULATIONS)]

results_df = pd.DataFrame(draft_results, columns=[f'Team_{i+1}' for i in range(NUM_TEAMS)])

user_team_picks = [result[USER_PICK - 1] for result in draft_results]
user_team_picks_per_round = list(zip(*user_team_picks))

def get_most_common_players(picks_per_round):
    common_players = []
    for picks in picks_per_round:
        counter = Counter(picks)
        common = counter.most_common(3) 
        common_players.append([player[0] for player in common])
    return common_players

most_common_players = get_most_common_players(user_team_picks_per_round)

print("Your simulated team based on 500 simulations is:")
for round_num, players in enumerate(most_common_players, start=1):
    print(f"Round {round_num}:")
    for i, player in enumerate(players, start=1):
        print(f"  {i}. {player}")

