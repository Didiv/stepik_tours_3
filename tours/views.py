from random import randint

from django.http import HttpResponseNotFound

from django.shortcuts import render

from django.views.generic import View

import tours.data as data


class MainView(View):

    def genRandTourList(self, n: int, tours: dict) -> dict:
        '''
        Return n random tours
        '''
        result_tours = {}
        keys = tours.keys()
        for _ in range(n):
            n = randint(1, len(keys))
            while n in result_tours:
                n = randint(1, len(keys))
            result_tours[n] = tours[n]
        return result_tours

    def get(self, request) -> render:

        return render(
            request, 'index.html', context={
                "tours": self.genRandTourList(6, data.tours),
            }
        )


class DepartureView(View):
    def get(self, request, departure: str) -> render:

        if departure not in data.departures:
            return HttpResponseNotFound(
                f'Вылет из {departure} не поддерживается')

        tours_filtered = {k: v for k, v in data.tours.items()
                          if v['departure'] == departure}
        prices = sorted(tour['price'] for tour in tours_filtered.values())
        nights = sorted(tour['nights'] for tour in tours_filtered.values())

        return render(
            request, 'departure.html', context={
                "departure": departure,
                "departure_name": data.departures[departure],
                "tours": tours_filtered,
                "min_price": prices[0],
                "max_price": prices[-1],
                "min_nights": nights[0],
                "max_nights": nights[-1],
            }
        )


class TourView(View):
    def get(self, request, id: int) -> render:

        if id not in data.tours:
            return HttpResponseNotFound(
                f'Тур с id {id} нам не известен')

        return render(
            request, 'tour.html', context={
                "tour": data.tours[id],
                "departure_name": data.departures[data.tours[id]['departure']]
            }
        )
