import json
from math import ceil
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ForecastSerializer, UserDetailsSerializer, ForecastScenarioSerializer
# Create your views here.
from .models import Forecast, UserDetails, ForecastScenario
from .utils import *
class Login(APIView):
    def post(self,request):
        data=request.data
        username=data['username']
        password=data['password']
        user=authenticate(username=username,password=password)
        jwt = RefreshToken.for_user(user)
        isAdmin=user.is_staff
        return Response({"access_token": str(jwt.access_token),"refresh_token":str(jwt),"isAdmin":isAdmin})
class GetHistory(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        forecastList=Forecast.objects.filter(userID=user)
        forecastSerializer=ForecastSerializer(forecastList,many=True)
        forecastData=forecastSerializer.data
        for forecast in forecastData:
            date_format = "%Y-%m-%d"
            scenario=ForecastScenario.objects.get(id=int(forecast['scenario']))
            forecast['scenario']=ForecastScenarioSerializer(scenario).data['title']
            date_object = datetime.datetime.strptime(forecast['period'], date_format).date().replace(day=1)
            createdAtDate=datetime.datetime.strptime(forecast['createdAt'], date_format).date()
            if(date_object>=datetime.date.today().replace(day=1).replace(day=1) and latestCreated(forecast['period'],createdAtDate,forecastData)):
                forecast['editable']=True
            else:
                forecast['editable'] = False
        return Response(forecastData)
class UpdateForecastList(APIView): #{ "list":[{"period":"2023-08-01","values":{"tailWind":1,"firmWind":2,"worst":3}},{"period":"2023-09-01","values":{"tailWind":4,"firmWind":5,"worst":6}}] }
    def post(self,request):
        data=request.data
        list=data['list']
        user = User.objects.get(id=1)
        for forecast in list:
            period = forecast['period']
            values = forecast['values']
            forecastTail = Forecast.objects.get(period=period, forecast_type='Tail Wind',userID=user)
            forecastTail.amount = values['tailWind']
            forecastTail.save()
            forecastFirm = Forecast.objects.get(period=period, forecast_type='Firm Wind',userID=user)
            forecastFirm.amount = values['firmWind']
            forecastFirm.save()
            forecastWorst = Forecast.objects.get(period=period, forecast_type='Worst',userID=user)
            forecastWorst.amount = values['worst']
            forecastWorst.save()
        return Response({"message":"updated successfully"})

class CreateUpdateForecast(APIView):  #{"year":"Y","values":{"month":{"tailWind":1,"firmWind":2,"worst":3},"month2":{"tailWind":1,"firmWind":2,"worst":3}}}
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        data=request.data
        year=data['year']
        values=data['values']
        user=request.user
        firmWind = ForecastScenario.objects.get(id=1)
        tailWind = ForecastScenario.objects.get(id=2)
        worst = ForecastScenario.objects.get(id=3)
        for month in values.keys():
            Forecast.objects.create(userID=user,period=datetime.date(int(year),int(month),28),insertedBy=user,
                                    scenario=tailWind,amount=values[month]['tailWind'],
                                    createdAt=datetime.date.today(),updatedAt=datetime.date.today())
            Forecast.objects.create(userID=user, period=datetime.date(int(year), int(month), 28),insertedBy=user,
                                    scenario=firmWind, amount=values[month]['firmWind'], createdAt=datetime.date.today(),updatedAt=datetime.date.today())
            Forecast.objects.create(userID=user, period=datetime.date(int(year), int(month), 28),insertedBy=user,
                                    scenario=worst, amount=values[month]['worst'], createdAt=datetime.date.today(),updatedAt=datetime.date.today())
        return Response({"message":"created successfully"})
    def put(self,request):
        data=request.data
        period=data['period']
        values=data['values']
        user = request.user
        firmWind = ForecastScenario.objects.get(id=1)
        tailWind = ForecastScenario.objects.get(id=2)
        worst = ForecastScenario.objects.get(id=3)
        forecastTail=Forecast()
        forecastTail.userID=user
        forecastTail.period=period
        forecastTail.scenario=tailWind
        forecastTail.amount=values['tailWind']
        forecastTail.insertedBy=user
        forecastTail.createdAt = datetime.date.today()
        forecastTail.updatedAt = datetime.date.today()
        forecastTail.save()
        forecastFirm = Forecast()
        forecastFirm.userID = user
        forecastFirm.period = period
        forecastFirm.scenario = firmWind
        forecastFirm.amount = values['firmWind']
        forecastFirm.insertedBy=user
        forecastFirm.createdAt = datetime.date.today()
        forecastFirm.updatedAt = datetime.date.today()
        forecastFirm.save()
        forecastWorst = Forecast()
        forecastWorst.userID = user
        forecastWorst.period = period
        forecastWorst.scenario = worst
        forecastWorst.amount = values['worst']
        forecastWorst.insertedBy=user
        forecastWorst.createdAt=datetime.date.today()
        forecastWorst.updatedAt = datetime.date.today()
        forecastWorst.save()
        return Response({"message":"updated successfully"})

class AvailableQuarters(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        today=datetime.date.today()
        today=str(today).split("-")[0]+"-"+str(today).split("-")[1]
        today=datetime.datetime.strptime(str(today),"%Y-%m").date()
        latestForecast=Forecast.objects.filter(period__gte=today,userID=user)
        serializer=ForecastSerializer(latestForecast,many=True)
        current_date = datetime.datetime.now()
        current_month = current_date.month
        current_year=current_date.year
        current_quarter=ceil(current_month/3)
        availableQuarters=[]
        c=current_quarter
        for i in range(4):
            if(c<=4):
                availableQuarters.append({"quarter":c,"year":current_year})
            else:
                availableQuarters.append({"quarter": c%4, "year": current_year+1})
            c+=1
        for cast in serializer.data:
            month=int(cast['period'].split("-")[1])
            year=int(cast['period'].split("-")[0])
            createdAtDateString=str(cast['createdAt']).split("-")[0]+"-"+str(cast['createdAt']).split("-")[1]
            createdAtDate=datetime.datetime.strptime(createdAtDateString,"%Y-%m").date()
            if(createdAtDate>=today):
                availableQuarters=list(filter(lambda x: x['quarter']!=ceil(month/3) or x['year']!=year, availableQuarters))
        return Response(availableQuarters)









