from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
import requests
from django.conf import settings
# Create your views here.

from rest_framework.decorators import api_view
import math
import statistics

@api_view(['GET'])
def get_weather_data(request, location):
    days = request.GET.get('days')

    url = '{}?key={}&q={}&days={}' \
        .format(settings.WEATHER_API_URL,
            settings.WEATHER_API_KEY,
            location,
            days)

    response = requests.get(url)
    try:
        response.raise_for_status()
        data = response.json()

        minimum = min([x['day']['mintemp_c'] for x in  data['forecast']['forecastday']])
        maximum = max([x['day']['mintemp_c'] for x in  data['forecast']['forecastday']])
        average = statistics.mean([x['day']['mintemp_c'] for x in  data['forecast']['forecastday']])
        median = statistics.median([x['day']['mintemp_c'] for x in  data['forecast']['forecastday']])

    except requests.HTTPError as e:
        return Response(str(e))


    return Response({'maximum': maximum,
        'minimum': minimum,
        'average': average,
        'median': median})
