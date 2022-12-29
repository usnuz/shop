from django.contrib.auth import login, authenticate, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *


@api_view(['POST'])
def sign_up(request):
    first_name = request.POST.get('first-name')
    last_name = request.POST.get('last-name')
    username = request.POST.get('username')
    password = request.POST.get('password')
    try:
        new_user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
        )
        return Response('Success')
    except:
        return Response(f'{username} username is busy')


@api_view(['POST'])
def log_in(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    usr = authenticate(username=username, password=password)
    print(usr, username, password)
    if usr is not None:
        login(request, usr)
        return Response(f'{username} login')
    else:
        return Response('Error username or password')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def log_out(request):
    logout(request)
    return Response('logout')
