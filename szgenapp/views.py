from django.shortcuts import render

from .models import Study


def index(request):
    template = 'app/index.html'
    studies = Study.objects.all()
    context = {'studies': studies}
    return render(request, template, context)