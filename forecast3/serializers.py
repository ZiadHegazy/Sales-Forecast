from rest_framework import serializers
from .models import Forecast, UserDetails, ForecastScenario


class ForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forecast
        fields = ('userID','insertedBy', 'period','scenario','amount','createdAt','updatedAt')
class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ('userID', 'position')
class ForecastScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model=ForecastScenario
        fields=('id','title')