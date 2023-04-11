"""
    Teddy Oweh: ifechukwudeni.oweh@go.tarleton.edu
    Tyler Rider: tyler.rider@go.tarleton.edu
"""
from datetime import datetime


class Log:
    def __init__(self):
        pass

    def log_data(self, data):
        """Log data to the logs.txt file.

        Parameters
        ----------
        data
            A string that is sent from one of the functions in Payload.py
        """
        date = str(datetime.now())
        dashs = "-" * 200
        data = f"\n {dashs}\n {date} : {data}\n"
        filename = f"/home/tar/Desktop/TARPayload/src/logs/logs.txt"
        open(filename, "a").write(data)
