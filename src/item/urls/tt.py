import datetime
date= datetime.datetime.now().date()
year, month, day= str(date).split('-')
day_name = datetime.date(int(year), int(month), int(day))
print(day_name.strftime("%A"))
