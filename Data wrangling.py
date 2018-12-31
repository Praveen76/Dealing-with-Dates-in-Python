import os
import pandas as pd

import numpy as np

from datetime import datetime
from configparser import ConfigParser

# Adjust dates
Start_date=pd.to_datetime(Start_date)
End_date=pd.to_datetime(End_date)
LastWorkingDate=pd.to_datetime(LastWorkingDate)


LastWorkingYear1=LastWorkingDate.year
LastWorkingMonth1=LastWorkingDate.month-1
LastWorkingDay1=LastWorkingDate.day

ThisWeekdate=LastWorkingDate-timedelta(days=4)

LastWeekdateStart=LastWorkingDate-timedelta(days=11)
LastWeekdateend=LastWorkingDate+timedelta(days=11)

PreviousMonthDate= pd.to_datetime(str(LastWorkingYear1)+'-'+str(LastWorkingMonth1)+'-'+str(LastWorkingDay1))


data2=data.copy() #Backup



data.rename(columns={'Emp Name':'Employee Name',
                          'Emp Number':'Employee Number',
                          'Eng/Internal Code Number':'Engagement/Internal Code Number'}, 
                 inplace=True)



###Take out data of last 1 month from current date.


data_LM= data[(data['Work Date']>=PreviousMonthDate) &  
            (data['Work Date']<=LastWorkingDate)&
             data['Employee Name'].isin(New_Emp)]


imp_vars=['Employee Name','Employee Number','Work Date','Engagement/Internal Code Number','Chargeable Hours'
          ]


data_LM=data_LM[imp_vars].reset_index(drop=True)

data_LM['Chargeable Hours']=round(data_LM['Chargeable Hours'],1)

data_LM.columns=['Employee_Name', 'Employee Number', 'Work_Date',
       'Engagement/Internal Code Number','Chargeable Hours']


       
Engagement_Code=[]
for index,row in data_LM.iterrows():
    Engagement_Code.append(int(row['Engagement/Internal Code Number']))


data_LM['Engagement/Internal Code Number']=Engagement_Code
    
data_LM.head()

##Important code

data_New=pd.DataFrame(data_LM.groupby(['Employee_Name','Work_Date'])['Engagement/Internal Code Number'].apply(list))

data_New['Chargeable Hours']=data_LM.groupby(['Employee_Name','Work_Date'])['Chargeable Hours'].apply(list)


Last_week_Code=[]
for i in data_New['Engagement/Internal Code Number']:
    Last_week_Code.append(i[0])

    
Last_week_Hours=[]
for i in data_New['Chargeable Hours']:
    Last_week_Hours.append(i[0])    
    
    

data_New['Last_week_Code']=Last_week_Code 
data_New['Last_week_Hours']=Last_week_Hours 




This_week_Code=[]
for i in data_New['Engagement/Internal Code Number']:
    This_week_Code.append(i[-1])

data_New['This_week_Code']=This_week_Code

This_week_Hours=[]
for i in data_New['Chargeable Hours']:
    This_week_Hours.append(i[-1])

data_New['This_week_Hours']=This_week_Hours

data_New['Changed_Code']=0

for index,row in data_New.iterrows():
    if(row['Last_week_Code']!=row['This_week_Code']):
        data_New['Changed_Code'].iloc[index]='Changed'

        



data_New.head()
data_New.to_csv('C:/Users/praveenanwla/Desktop/Python/data_New.csv',index=True)


#==============================================================================
# Another Operation
#==============================================================================

Sync_Data=data_New.reset_index().copy()

###Rename columns

Sync_Data.rename(columns={'Employee_Name':'EmployeeName',
                          'Work_Date':'Date',
                          'Engagement/Internal Code Number':'ProjectID'}, 
                 inplace=True)

cols=['EmployeeName','Date','ProjectID','Chargeable Hours']
Sync_Data=Sync_Data[cols]


##Forge Retain data for testing purpose

RetainData=pd.read_csv('C:/Users/praveenanwla/Desktop/Python/RetainData.csv',
        parse_dates=[2],    encoding='utf-8')

#Add space in Employee names in retain Data

def xyz (data):
    data=data.replace(',',', ')
    return data

RetainData['EmployeeName']=RetainData['EmployeeName'].apply(xyz)

RetainData= RetainData[(RetainData['Date']>=ThisWeekdate) &  
            (RetainData['Date']<=LastWorkingDate) &
             RetainData['EmployeeName'].isin(New_Emp)]


#Merge Sync_Data & RetainData on EmployeeName and Date

mergedStuff=pd.merge(RetainData, Sync_Data, on=['EmployeeName','Date'],how='inner')

mergedStuff.columns=['EmployeeName','Retain_ProjectID','Date','Retain_Hours','Sync_ProjectID','Sync_Hours']

mergedStuff['Defaulters']=0

for index,row in mergedStuff.iterrows():
    if row['Retain_ProjectID'] not in row['Sync_ProjectID']:
        mergedStuff['Defaulters'].iloc[index]='Yes'
    if  (len(row['Sync_ProjectID'])>1):  
        mergedStuff['Defaulters'].iloc[index]='Yes'

mergedStuff.head()


mergedStuff.to_csv('C:/Users/praveenanwla/Desktop/Python/FinalData.csv',index=False)


