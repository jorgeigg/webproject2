# URLS from Home
from django.urls import path
from . import views

app_name = "mediciones_app"

urlpatterns = [
     # ****************************************************** 
     # ******************************************************
     # MEDICIONES 
     # HTML - Lista los datos de la mediciones en general
     #path('',views.MeasurementDataFloat.as_view(), name='mediciones_agua_lista'),  
]