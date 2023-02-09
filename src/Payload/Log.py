"""
    Teddy Oweh: ifechukwudeni.oweh@go.tarleton.edu
"""
from datetime import datetime
import os
class Log:
    def __init__(self):
       
        pass
    
    def get(self,type):
        pass
 
    def set(self, value):
        pass
 
    def log_pressure(self,pressure):
        pass
    def log_data(self,data):
        date = str(datetime.now())
        dashs = '-'*200
        data = f'\n {dashs}\n {date} : {data}\n'
        filename = f'/home/trc/Downloads/TARPayload/src/logs/logs.txt'
        open (filename,'a').write(data)