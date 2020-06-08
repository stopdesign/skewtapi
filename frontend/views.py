from api.models import Radiosonde
from django.shortcuts import render




def index(request):
    if request.method == 'GET':
        sample_sonde = Radiosonde.objects.first()
    return render(request,'frontend/index.html',{'sample_sonde': sample_sonde})
