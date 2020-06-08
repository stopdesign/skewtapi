from rest_framework import serializers
from .models import Radiosonde



class RadiosondeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    wmo_id = serializers.CharField()
    sonde_validtime =serializers.DateTimeField()
    station_name =serializers.CharField()
    lat = serializers.DecimalField(max_digits=9, decimal_places=4)
    lon = serializers.DecimalField(max_digits=9, decimal_places=4)
    temperatureK = serializers.ListField(child=serializers.DecimalField(max_digits=6, decimal_places=2))
    dewpointK = serializers.ListField(child=serializers.DecimalField(max_digits=6, decimal_places=2))
    pressurehPA = serializers.ListField(child=serializers.IntegerField())
    u_windMS = serializers.ListField(child=serializers.DecimalField(max_digits=6, decimal_places=2))
    v_windMS = serializers.ListField(child=serializers.DecimalField(max_digits=6, decimal_places=2))
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()



class AvailableSerializer(serializers.Serializer):
    wmo_id = serializers.CharField()
    lat = serializers.DecimalField(max_digits=9, decimal_places=4)
    lon = serializers.DecimalField(max_digits=9, decimal_places=4)



class NearestSerializer(serializers.Serializer):
    wmo_id = serializers.CharField()