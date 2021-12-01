'''
Anoop Nath (nathar90@gmail.com)
11/30/2021
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


shots= pd.read_csv('shots_data.csv')

#calculating distance of shots
shots['distance'] = ((0-shots['x'])**2 + (shots['y'])**2)**.5


#creating new rows for corner threes, non_corner threes, and two point shots
shots['corner_three'] = np.where( (shots.distance >22) & (shots.y <= 7.8) , 1, 0)
shots['non_corner_three']= np.where( (shots.corner_three == 0) & (shots.distance >= 23.75) , 1, 0)
shots['two_pointer'] = np.where( (shots.corner_three == 0) & (shots.non_corner_three == 0) , 1, 0)
shots['shot_type'] =  np.where( (shots.corner_three == 1), 'corner three',   np.where( (shots.non_corner_three == 1), 'non corner three', 'two pointer' )) 

col = shots.shot_type.map({'corner three':'b', 'non corner three':'r' , 'two pointer': 'g'})

#plot the shots
plt.scatter(shots['x'], shots['y'], s=5, c=col, marker='.')
plt.show()

teamA= shots[shots.team =='Team A'] #df for Team A
teamB= shots[shots.team =='Team B'] #df for Team B

teamA_madeShots= teamA[teamA.fgmade ==1] #df for Team A w/ made shots only
teamB_madeShots= teamB[teamB.fgmade ==1] #df for Team B w/ made shots only

#calculating shot selection %, fg% and efg% for team A 
teamA_shot_distribution =  pd.DataFrame(teamA.shot_type.value_counts() )
teamA_shot_distribution = teamA_shot_distribution.rename(columns={'shot_type': 'attempts'})
teamA_shot_distribution['shot_type'] = teamA_shot_distribution.index
teamA_shot_distribution['shot_selection_percentage'] = teamA_shot_distribution['attempts']/teamA_shot_distribution['attempts'].sum()
teamA_shot_distribution['made']  = pd.DataFrame(teamA_madeShots.shot_type.value_counts() )
teamA_shot_distribution['fg%'] =  teamA_shot_distribution['made']/teamA_shot_distribution['attempts']
teamA_shot_distribution['efg%']= np.where( (teamA_shot_distribution.shot_type =='two pointer') , teamA_shot_distribution['fg%'], teamA_shot_distribution['made']*1.5/teamA_shot_distribution.attempts )
teamA_shot_distribution.reset_index(drop=True,  inplace=True)
teamA_shot_distribution = teamA_shot_distribution [['shot_type','shot_selection_percentage', 'attempts' , 'made', 'fg%' , 'efg%']] #reordering columns

#calculating shot selection %, fg% and efg% for team B 
teamB_shot_distribution =  pd.DataFrame(teamB.shot_type.value_counts() )
teamB_shot_distribution = teamB_shot_distribution.rename(columns={'shot_type': 'attempts'})
teamB_shot_distribution['shot_selection_percentage'] = teamB_shot_distribution['attempts']/teamB_shot_distribution['attempts'].sum()
teamB_shot_distribution['made']  = pd.DataFrame(teamB_madeShots.shot_type.value_counts() )
teamB_shot_distribution['fg%'] =  teamB_shot_distribution['made']/teamB_shot_distribution['attempts']
teamB_shot_distribution['shot_type'] = teamB_shot_distribution.index
teamB_shot_distribution.reset_index(drop=True,  inplace=True)
teamB_shot_distribution['efg%']= np.where( (teamB_shot_distribution.shot_type =='two pointer') , teamB_shot_distribution['fg%'], teamB_shot_distribution['made']*1.5/teamB_shot_distribution.attempts )
teamB_shot_distribution = teamB_shot_distribution [['shot_type','shot_selection_percentage', 'attempts' , 'made', 'fg%' , 'efg%']] #reordering columns





