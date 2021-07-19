from django.http.request import HttpRequest
from django.shortcuts import render


def category(request):
    return render(request, 'Products/category.html')
