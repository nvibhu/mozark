from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import*
import pandas as pd
import os

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def financeApps(request):
    #return HttpResponse("Hello world!")
    # template = loader.get_template('myfirst.html')
    # return HttpResponse(template.render())

    template = loader.get_template('myfirst.html')
    # item = Student.objects.all().values()
    # df = pd.DataFrame(item)
    # mydict = {
    #     "df": df.to_html()
    # }
    #return render(request, 'index.html', context=mydict)
    
    
    data = {'Name':['Tom', 'nick', 'krish', 'jack'], 'Age':[20, 21, 19, 18]}
    # Create DataFrame
    df = pd.DataFrame(data)
    context = {
        "df": df.to_html()
    }

    # mymembers = {'firstname': 'Navnnet', 'lastname': 'Vibhu'}
    # context = {
    #     'mymembers': mymembers,
    # }


    path = '/Users/nvibhu/Documents/mozark/finance/Trial_Balance/'
    dir_list = os.listdir(path)
    context = {
        'dir_list': dir_list,
    }
    #print("Files and directories in '", path, "' :")

    return HttpResponse(template.render(context, request))

def files(request):
    template = loader.get_template('files.html')
    path = '/Users/nvibhu/Documents/mozark/finance/Trial_Balance/'
    dir_list = os.listdir(path)
    context = {
        'dir_list': dir_list,
    }
    return HttpResponse(template.render(context, request))


def details(request, file_name):
    print('file name is -> ',file_name)
    file_path = '/Users/nvibhu/Documents/mozark/finance/Trial_Balance/'+file_name
    df = pd.read_csv(file_path, encoding = 'latin1')
    context = {
        "df": df.to_html()
    }
    template = loader.get_template('details.html')
    return HttpResponse(template.render(context, request))


# Create your views here.
def home(request):
    item = Student.objects.all().values()
    df = pd.DataFrame(item)
    mydict = {
        "df": df.to_html()
    }
    return render(request, 'index.html', context=mydict)


# from financeSystem.financeApps.serializers import UserSerializer, GroupSerializer
# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]
