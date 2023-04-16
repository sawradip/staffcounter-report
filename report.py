import requests
import datetime
from bs4 import BeautifulSoup

# 0 for current week, -1 for previous week, -2 forweek brfore that etc.
n_week = 0

full_time = 160  #in hours
full_time_pay = 50000 
BDT_to_USD = 106

# Put your staffcounter email id here. 
EMAIL_ID = "sawradipsaha5@gmail.com"    
# URL_format = "https://data.staffcounter.net/report/sawradipsaha5@gmail.com?date=2022-12-17"
# https://data.staffcounter.net/report/sawradipsaha5@gmail.com?reloaded=1&date=2023-04-10
def getDuration(emailId = EMAIL_ID, dateString = "2022-12-17"):

    URL = f"https://data.staffcounter.net/report/{emailId}"
    PARAMS = {"reloaded":1, "date": dateString}
    r = requests.get(URL, params=PARAMS)

    soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install ' or install html5lib
    s = soup.find("div", {"id": "productivity_chart_271040"})
    timeString = s.parent.findNext('td').text.strip()

    try:
        t = datetime.datetime.strptime(timeString, "%Hh %Mm")
        workDuration = datetime.timedelta(hours=t.hour, minutes=t.minute)
    except  ValueError:
        try:
            t = datetime.datetime.strptime(timeString, "%Mm")
            workDuration = datetime.timedelta(minutes=t.minute)
        except ValueError:
            try:
                t = datetime.datetime.strptime(timeString, "%Hh")
                workDuration = datetime.timedelta(hours=t.hour)
            except ValueError:
                workDuration = datetime.timedelta(0)
    return workDuration

    

# Last  Monday
todayDate = datetime.date.today()

startDate = todayDate + datetime.timedelta(days=-todayDate.weekday(), weeks=n_week)
if n_week == 0:
    endDate = todayDate
else:
    endDate = startDate + datetime.timedelta(days= 6)

def getTotalTime(startDate, endDate):
    totalTime = datetime.timedelta(0)
    day_count = (endDate - startDate).days + 1
    for singleDate in [d for d in (startDate + datetime.timedelta(n) for n in range(day_count)) if d <= endDate]:
        workDuration = getDuration(dateString = singleDate.__str__())
        totalTime = totalTime + workDuration
        print(f"{singleDate.__str__()} --> {int(workDuration.total_seconds()//3600)}h {int((workDuration.total_seconds()%3600)//60)}m = TotalTime: {totalTime}")

    return totalTime


print( f""" 

Time Report:
-----------------------""")
totalTime =  getTotalTime(startDate, endDate)
total_active_time_str = f"{int(totalTime.total_seconds()//3600)}h {int((totalTime.total_seconds()%3600)//60)}m"
total_active_time_decimal = int(totalTime.total_seconds()//3600) +  ((totalTime.total_seconds()%3600)//60)/60

print( f"""--------------------------

Start_date: {startDate}
End_date: {endDate}
Total Active Time: {total_active_time_str}
BDT : {total_active_time_decimal * full_time_pay / full_time}
USD: { total_active_time_decimal * full_time_pay / full_time / BDT_to_USD}



 """)