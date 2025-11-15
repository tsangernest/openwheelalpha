import json
from http import HTTPStatus

from django.core.serializers import serialize
from django.http import JsonResponse

from app.models import Driver, Nationality


def nationality(request):
    if request.method == "GET":
        json_data = json.loads(serialize(format="json",
                                                          queryset=Nationality.objects.all(),
                                                          fields=["demonym", "country"]))
        return JsonResponse({"status": HTTPStatus.OK,
                                           "count": Nationality.objects.count(),
                                           "data": json_data})
    return JsonResponse({"status": HTTPStatus.NOT_FOUND})


def driver(request):
    if request.method == "GET":
        json_data = json.loads(serialize(format="json",
                                                          queryset=Driver.objects.all()))
        return JsonResponse({"status": HTTPStatus.OK,
                                            "count": Driver.objects.count(),
                                            "data": json_data})
    return JsonResponse({"status": HTTPStatus.NOT_FOUND})

