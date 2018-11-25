from csv import DictReader
from .settings import BUS_STATION_CSV, STATIONS_ON_PAGE
from urllib.parse import urlencode, quote_plus

from django.shortcuts import render_to_response, redirect
from django.urls import reverse

import datetime


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    get_param_page = request.GET.get('page')

    current_page_pagination = 1 if get_param_page is None else int(get_param_page)

    stations = []
    with open(BUS_STATION_CSV, encoding='cp1251') as csv_file:
        reader = DictReader(csv_file)
        cur_csv_page = current_page_pagination * STATIONS_ON_PAGE

        for counter, row in enumerate(reader):
            if cur_csv_page - counter < STATIONS_ON_PAGE:
                stations.append({'Name': row['Name'], 'Street': row['Street'], 'District': row['District']})
            if counter > cur_csv_page:
                break

    prev_url = f"{reverse('bus_stations')}?page={current_page_pagination-1}"
    next_url = f"{reverse('bus_stations')}?page={current_page_pagination+1}"

    return render_to_response('index.html', context={
        'bus_stations': stations,
        'current_page': current_page_pagination,
        'prev_page_url': prev_url if current_page_pagination != 1 else None,
        'next_page_url': next_url,
    })
