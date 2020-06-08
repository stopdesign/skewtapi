from django.urls import path
from api.views import RadiosondeAPIView


urlpatterns = [
    path("sondes/<int:pk>/", RadiosondeAPIView.as_view(), name="get-sonde"),
] 