# to import packages 
from statsmodels.multivariate.manova import MANOVA
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.multivariate.manova import MANOVA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as lda


class sortdataframe: 
  def __init__(self, input_dataframe): 
    # to read the input file 
    self.df = pd.read_csv(input_dataframe) 

    # to sort the dataframe 
    self.df.sort_values('WinLoss', axis=0, ascending = True, inplace = True) 

  def newframe(self): 
    col3 = self.df['3P'].tolist()
    col3attempt = self.df['3PA'].tolist()
    colFG = self.df['FG'].tolist() 
    colFGattempt = self.df['FGA'].tolist()  
    colFT = self.df['FT'].tolist()
    FTattempt = self.df['FTA'].tolist()
    result=self.df['WinLoss'].tolist()

    # to calculate 2P field goals  
    LG = len(col3) # to calculate the number of element in the list 
    col2 = [colFG[i]-col3[i] for i in range(LG)] 

    # the failed 3P attempt 
    col3_fail = [col3attempt[i]-col3[i] for i in range(LG)] 

    # the failed field goals
    FGfail = [colFGattempt[i]-colFG[i] for i in range(LG)] 

    # the failed 2P attempt
    col2_fail = [FGfail[i]-col3_fail[i] for i in range(LG)]  

    # to calculate failed free throws 
    colFT_fail = [FTattempt[i]-colFT[i] for i in range(LG)] 

    Offensive_RB = self.df['ORB'].tolist()
    Total_RB = self.df['TRB'].tolist()

    # the defensive rebound 
    Defensive_RB = [Total_RB[i] - Offensive_RB[i] for i in range(LG)]  

    self.newframe = pd.DataFrame(list(zip( result, col3, col3_fail, col2, col2_fail, colFT, colFT_fail, Offensive_RB, Defensive_RB)),
               columns =['result','goal3', 'goal3fail', 'goal2', 'goal2fail', 'FT', 'FTfail', 'ORB', 'DRB']) 
    
  def chunking_frame(self): 
    self.newframe()
    frame_rest = self.df.iloc[:, 9:]
    result = pd.concat([self.newframe, frame_rest], axis=1)

    resultlist = result['result'].tolist()

    # to create two empty lists 
    winlist =[]
    defeatedlist=[]

    LR = len(resultlist)
    for i in range(LR): 
      if resultlist[i] == 'L':
        defeatedlist.append(i)
      else: 
        winlist.append(i) 

    LD = len(defeatedlist)-1
    LW = len(defeatedlist)

    self.defeateddf = result.iloc[0:LD, :] 
    self.windf = result.iloc[LW:, :]

    self.fullframe = result 

  def statscalc(self): 
    result = ['L', 'W']
    deflist = self.defeateddf.iloc[:, 1:].to_numpy() 
    winlist = self.windf.iloc[:, 1:].to_numpy()  
    self.defmean = np.mean(deflist, axis=0)
    self.defsd = np.std(deflist, axis=0)

    self.winmean = np.mean(winlist, axis=0)
    self.winsd = np.std(winlist, axis=0)
