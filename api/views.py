from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render

from api.models import Radiosonde
from api.serializers import RadiosondeSerializer
from rest_framework.generics import get_object_or_404



class RadiosondeAPIView(APIView):
    def get(self, request, pk):
        sonde = get_object_or_404(Radiosonde, pk=pk)
        serializer = RadiosondeSerializer(sonde)
        return Response(serializer.data) 



