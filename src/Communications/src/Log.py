from datetime import datetime
import os
class Log:
    def __init__(self):
        self.path = '../path/log'
        try:
            os.makedirs(self.path)
        except:
            pass
    
    
    def get(self,type):
        pass
    @staticmethod
    def set(self, value):
        pass
    @staticmethod
    def log_pressure(self,pressure):
        pass