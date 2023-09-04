import datetime


def latestCreated(period,createdAt,forecasts):
    forecasts=list(filter(lambda x:x['period']==period,forecasts))
    date_format = "%Y-%m-%d"
    max = datetime.datetime.strptime(forecasts[0]['createdAt'], date_format).date()
    for forecast in forecasts:
        currentDate=datetime.datetime.strptime(forecast['createdAt'], date_format).date()
        if(currentDate>max):
            max=currentDate
    return max==createdAt