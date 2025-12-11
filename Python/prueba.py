from datetime import date, timedelta


todays_date = date.today() # current time 'yy-mm-dd' UTC
print("Current date: ", todays_date)

var_dia = timedelta(days=365)
deltatime = todays_date - var_dia
print("Ayer: ", deltatime)

