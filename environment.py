from datetime import date
import datetime

class Environment:
    def __init__(self, id):
        self.id = id
        self.date = date.today()
        self.bank_amount = 1000000
    
    def incrementDate(self):
        self.date = self.date + datetime.timedelta(days=1)
    
    def getDate(self):
        return self.date