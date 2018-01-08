from django.shortcuts import render
from service import Sorter
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dataFilePath = os.path.join(BASE_DIR,'Sorter' + os.path.sep + 'saved_report.txt')
 
def list(request):
    context = {}
    context['athleteNames'] = Sorter.getAthleteNames(dataFilePath)
    return render(request, 'list.html', context)

def detail(request):
    name = request.GET['name']
    context = {}
    context['detail'] = Sorter.getDetail(dataFilePath, name)
    return render(request, 'detail.html', context)
    
