import os
import pandas as pd
import numpy as np

from datetime import datetime
from configparser import ConfigParser


###Parse Configuration file
parser=ConfigParser()
parser.read('dev.ini')
print(parser.sections())

Work_Location=parser['DB']['Work Location']
print(Work_Location)
Start_date=parser['DB']['Start_date']
print(Start_date)
End_date=parser['DB']['End_date']
print(End_date)
LastWorkingDate=parser['DB']['lst_Date']
print(LastWorkingDate)


###Take emp names in to list
Emp_Names=[]
for name in parser['DB']['Emp_names'].split(','):
    Emp_Names.append(name)

print(Emp_Names)  
