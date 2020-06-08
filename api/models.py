
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from math import cos, asin, sqrt
import csv
import re



models.DecimalField(max_digits=7, decimal_places=3)
models.CharField(max_length=200)
ArrayField(models.IntegerField(), default=list, size=40)
ArrayField(models.DecimalField(max_digits=4, decimal_places=3), default=list, size=40)
models.DateTimeField('reference time', null=True)
models.ForeignKey(Spot, on_delete=models.CASCADE)



class Radiosonde(models.Model):

    sonde_validtime = models.DateTimeField('sonde validtime', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    wmo_id = models.CharField(max_length=50)
    station_name = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=9, decimal_places=4)
    lon = models.DecimalField(max_digits=9, decimal_places=4)
    temperatureK = ArrayField(models.DecimalField(max_digits=4, decimal_places=3), default=list)
    dewpointK = ArrayField(models.DecimalField(max_digits=4, decimal_places=3), default=list)
    pressurehPA = ArrayField(models.IntegerField(), default=list)
    u_windMS = ArrayField(models.DecimalField(max_digits=4, decimal_places=3), default=list)
    v_windMS =ArrayField(models.DecimalField(max_digits=4, decimal_places=3), default=list)

    def __str__(self):
        return f"{station_name} ({wmo_id}): {sonde_validtime}\ntemperature: {temperatureK}"



class UpdateRecord(models.Model):

    filename =  models.CharField(max_length=50)
    updatetime = models.DateTimeField(auto_now_add=True)

    @classmethod
    def delete_expired(cls, expiration_days):
        limit = timezone.now() - timezone.timedelta(days=expiration_days)
        cls.objects.filter(cls.updatetime <= limit).delete()
        cls.save()



class Station(models.Model):

    stn_wmoid = models.CharField(max_length=50)
    stn_name = models.CharField(max_length=50)
    stn_lat = models.DecimalField(max_digits=9, decimal_places=4)
    stn_lon = models.DecimalField(max_digits=9, decimal_places=4)
    stn_altitude = models.DecimalField(max_digits=9, decimal_places=4)

    def __str__(self):
        return f"{stn_name} ({stn_wmoid})"

    @classmethod
    def initialize_stations(cls):
        US_STATES = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "IA", "ID",
                     "IL", "IN", "KS","LA", "MA", "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC",
                     "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI", "SC", "SD",
                     "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY"]

        with open('station_list.txt', 'r') as csvfile:
            print("Running station initializer...")
            stndata = csv.reader(csvfile, delimiter='\t')
            for row in stndata:
                m = re.match(r"(?P<stn_wmoid>^\w+)\s+(?P<stn_lat>\S+)\s+(?P<stn_lon>\S+)\s+(?P<stn_altitude>\S+)(?P<stn_name>\D+)" , row[0])
                fields = m.groupdict()
                stn_wmoid = fields['stn_wmoid'][6:]
                stn_name = fields['stn_name'].strip()

                if re.match(r"^[a-zA-Z]{2}\s", stn_name) and  stn_name[:2] in US_STATES:
                    stn_name = stn_name[2:].strip().title() + ", " + stn_name[:2]
                else:
                    stn_name = stn_name.title()
                stn_name = fields['stn_name'].strip().title()
                stn_lat = float(fields['stn_lat'])
                stn_lon = float(fields['stn_lon'])
                stn_altitude = float(fields['stn_altitude'])

                if stn_altitude != -998.8:
                    station = Station(stn_wmoid=stn_wmoid, stn_lat=stn_lat, stn_lon=stn_lon, stn_name=stn_name, stn_altitude=stn_altitude)
                    station.save()


class Haversine:
    @classmethod
    def distance(cls, lat1, lon1, lat2, lon2):
        p = 0.017453292519943295
        a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
        return 12742 * asin(sqrt(a))

    @classmethod
    def closest(cls, data, v):
        return min(data, key=lambda p: cls.distance(float(v['lat']), float(v['lon']), p.lat, p.lon))
