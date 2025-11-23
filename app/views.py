import json

from django.core.serializers import serialize
from django.http import HttpRequest, JsonResponse

from app.models import Driver, Nationality


def nationality(request: HttpRequest):
    if request.method == "GET":
        json_data = json.loads(serialize(format="json",
                                                          queryset=Nationality.objects.all(),
                                                          fields=["demonym", "country"]))
        return JsonResponse({"status": 200,
                                           "count": Nationality.objects.count(),
                                           "data": json_data})
    return JsonResponse({"status": 404})


def driver(request: HttpRequest):
    if request.method == "GET":
        json_data = json.loads(serialize(format="json",
                                                          queryset=Driver.objects.all()))
        return JsonResponse({"status": 200,
                                            "count": Driver.objects.count(),
                                            "data": json_data})

    elif request.method == "POST":
        driver_obj = Driver.objects.create(**request.POST.dict())
        driver_data = Driver.objects.filter(id=driver_obj.pk).values().first()
        return JsonResponse({"status": 201, "data": driver_data})

    return JsonResponse({"status": 404})

