import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
import plotly 
import ast 
from matplotlib.patches import Arc
import seaborn as sns  
import requests
import json
import gzip  
from mplsoccer.pitch import Pitch


class Team_Tracking_Record: 
    # to store a big dataset into individual dictionary 
    def __init__(self, indata, homeboys, visitors): 
        # to divide the big dataset into 17 smaller nested dictionary 
        self.indata = indata 
        # to store home team data 
        self.hometeam_pos = {} 
        # to track each player's running distance 
        self.hometeam_distance = {} 
        # to store away team data 
        self.awayteam_pos = {}  
        # to track each player's running distance  
        self.awayteam_distance = {}  
        # to store time 
        self.timelist = []  
        # to link a connection between the jersey number and the names of the lads 
        self.homelads = homeboys
        self.awaylads = visitors
        
        # to create two empty dictionary to store dataframe 
        self.homeplayerdf = {}  
        self.awayplayerdf = {}  
        
        
    def storedata_firsthalf(self):  
        # to estimate the number of dictionary 
        L_track = len(self.indata) 
        
        def new_data_in_dict(inputdict, posdict, distancedict):
            # to store data into the nested dictionary 
            for player in inputdict: 
                player_id = player['jersey_number'] 
                if player_id in  posdict: 
                    posdict[player_id].append(player['position'])
                else: 
                    posdict[player_id] = [player['position']]
                if player_id in distancedict: 
                    distancedict[player_id].append(player['distance']) 
                else: 
                    distancedict[player_id] = [player['distance']] 
            return  posdict, distancedict               
                    
        
        for i in range(int(L_track/2)): 
            current_dict = self.indata[i] 
            # home team information
            hometeam = current_dict['home_team'] 
            # away team information 
            awayteam = current_dict['away_team'] 
            # to append new time stamp 
            self.timelist.append(current_dict['match_time']) 
            # to update both the distance dictionary and the position dictionary 
            self.hometeam_pos, self.hometeam_distance = new_data_in_dict(hometeam, self.hometeam_pos, self.hometeam_distance)
            self.awayteam_pos, self.awayteam_distance = new_data_in_dict(awayteam, self.awayteam_pos, self.awayteam_distance)

    def storedata_secondhalf(self):  
        # to estimate the number of dictionary 
        L_track = len(self.indata) 
        
        def new_data_in_dict(inputdict, posdict, distancedict):

            # to store data into the nested dictionary 
            for player in inputdict: 
                player_id = player['jersey_number'] 
                if player_id in  posdict: 
                    posdict[player_id].append(player['position'])
                else: 
                    posdict[player_id] = [player['position']]
                if player_id in distancedict: 
                    distancedict[player_id].append(player['distance']) 
                else: 
                    distancedict[player_id] = [player['distance']] 
            return  posdict, distancedict               
                    
        
        for i in range(int(L_track/2), L_track):   
            current_dict = self.indata[i] 
            # home team information
            hometeam = current_dict['home_team'] 
            # away team information 
            awayteam = current_dict['away_team'] 
            # to append new time stamp 
            self.timelist.append(current_dict['match_time']) 
            # to update both the distance dictionary and the position dictionary 
            self.hometeam_pos, self.hometeam_distance = new_data_in_dict(hometeam, self.hometeam_pos, self.hometeam_distance)
            self.awayteam_pos, self.awayteam_distance = new_data_in_dict(awayteam, self.awayteam_pos, self.awayteam_distance)
            
    def player_dataframe(self): 
        # to create a new instance variable which stores the dataframes 
        def namedict(playerdict): 
            player_dict = { }
            for i in range(len(playerdict)): 
                tempdict = playerdict[i]
                number = tempdict['jersey_number']
                player_dict[number] = tempdict['name'] 
            return player_dict
                
        def pos_coord(inputlist):
            # to create two separate lists of coordinates 
            matris = np.array(inputlist)
            tempx = list(matris[:, 0])
            xcoord = [tempx[i]+60 for i in range(len(tempx))]
            tempy = list(matris[:, 1]) 
            ycoord  = [tempy[i]+40 for i in range(len(tempy)) ]
            return xcoord,  ycoord  
        
        def create_dataframe(listpos, posdict, distdict): 
            poslist = posdict[listpos]
            
            # to separate the position list 
            xcoord,  ycoord = pos_coord(poslist)
            
            # to take out the distance list 
            distlist = distdict[listpos] 
            
            playerdata = {'x-coordinate': xcoord, 'y-coordinate': ycoord, 'distance': distlist}
            
            # to create a dataframe 
            playerdf = pd.DataFrame(playerdata) 
            
            return playerdf
        # to store which players have played in the game 
        home_number = [ ]
        away_number = [ ]
        
        homedict = namedict(self.homelads)
        awaydict = namedict(self.awaylads)
        
        for k,v in self.hometeam_pos.items(): 
            home_number.append(k) 
            
        for number in home_number: 
            # to fetch the number of the player's jewsey 
            n = int(number)  
            playerdf = create_dataframe(n, self.hometeam_pos, self.hometeam_distance)
            name = homedict[n]
            self.homeplayerdf[name] = playerdf
            
        for k,v in self.awayteam_pos.items(): 
            away_number.append(k)  
            
         
        for number in away_number: 
            # to fetch the number of the player's jewsey 
            n = int(number)  
            playerdf = create_dataframe(n, self.awayteam_pos, self.awayteam_distance)
            name = awaydict[n] 
            self.awayplayerdf[name] = playerdf 
            
            
class Creating_player_heatmap:  
    # to store all necessary information in a dataframe 
    def __init__(self, inputdict):
        self.inputdict = inputdict 

    def plotheatmap(self, player):
      # to extract player tracking data from the dictionary 
      playerdf = self.inputdict[player] 
      fig, ax = plt.subplots(figsize=(21, 12))
      # to create a football pitch with mplsoccer 
      pitch = Pitch(pitch_type='statsbomb', orientation='horizontal', pitch_color='grass', 
              line_color='white', stripe=True, figsize=(20, 12), constrained_layout=False, tight_layout=True) 
      pitch.draw(ax=ax)
      plt.gca().invert_yaxis()
      #Create the heatmap with seaborn
      kde = sns.kdeplot(playerdf['x-coordinate'], playerdf['y-coordinate'], shade = True, shade_lowest=False,
        alpha=0.95, n_levels=30, cmap="rocket_r") 
      plt.title( player )             
