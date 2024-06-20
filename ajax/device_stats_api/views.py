import json
from itertools import groupby

import django.db.models
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseNotFound

from .models import TestResult
from django.forms.models import model_to_dict


def stats(request: HttpRequest):
    if not request.method == "GET":
        return HttpResponseNotFound()

    query = request.GET
    results = TestResult.objects.filter(
        **dict(query.items())
    )
    grouped_by_device_type = groupby(sorted(
        map(model_to_dict, results),
        key=lambda r: r["device_type"]), lambda r: r["device_type"])

    _result = [
        {
            "device_type": key,
            "total": len(g_list := list(group)),
            "success_total": sum((record["success"] for record in g_list)),
            "failed_total": len(g_list) - sum((record["success"] for record in g_list))
         }
        for key, group in grouped_by_device_type
    ]
    return JsonResponse(_result, safe=False)


def test_result_list(request: HttpRequest):
    if not request.method == "GET":
        return HttpResponseNotFound()

    return JsonResponse(list(map(model_to_dict, TestResult.objects.all())), safe=False)


def test_result_post(request: HttpRequest):
    if not request.method == "POST":
        return HttpResponseNotFound()

    new_record = TestResult(**json.loads(request.body))
    new_record.validate_constraints()
    new_record.save()
    return HttpResponse(status=200)


def test_result_delete(request: HttpRequest, pk: str):
    if not request.method == "DELETE":
        return HttpResponseNotFound()
    try:
        record = TestResult.objects.get(pk=pk)
        record.delete()
        return HttpResponse(request.body)
    except django.core.exceptions.ObjectDoesNotExist:
        return HttpResponseNotFound()
