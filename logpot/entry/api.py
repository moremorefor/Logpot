
from flask import current_app
from flask_restful import Resource
from logpot.entry.models import Entry
from logpot.ext import db
from datetime import datetime, timedelta

class Heatmap(Resource):
    def get(self):
        entries = db.session.query(Entry).filter_by(is_published=True).order_by(Entry.id.desc()).all()
        timestamps = self.getYearData()
        if len(entries) != 0:
            for e in entries:
                rate = self.rateHeatmap(len(e.body))
                key = str(e.created_at.timestamp())
                timestamps[key] = rate
        return timestamps

    def rateHeatmap(self, num):
        base = 800
        rate = max(1, int(num / base))
        return rate

    def getYearData(self):
        now = datetime.now()
        year = now.year
        isLeap = self.isLeap(year)

        initial_date = str(now.year) + '-1-1'
        d = datetime.strptime(initial_date, '%Y-%m-%d')

        count = 366 if isLeap else 365
        year_data = {}
        for i in range(count):
            key = str(d.timestamp())
            year_data[key] = 0
            d += timedelta(days = 1)

        return year_data

    def isLeap(self, year):
        if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
            return True
        else:
            return False
