from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_auth.registration.views import VerifyEmailView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.decorators import (api_view,
                                       authentication_classes,
                                       permission_classes,)
from rest_framework_expiring_authtoken.authentication import (ExpiringTokenAuthentication,)

import requests


class ConfirmEmailView(APIView):
    """
    APIView for confirming email after registration
    """
    permission_classes = (AllowAny,)
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')

    def get(self, request, *args, **kwargs):
        post_data = {
            'key': kwargs['key'],
        }

        requests.post(request.build_absolute_uri(
            reverse("rest_verify_email")), data=post_data)
        return Response({'message': "Email verified successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
@authentication_classes((ExpiringTokenAuthentication,))
def disable_user(request):

    user = request.user
    user.is_active = False
    user.save()
    logout(request)
    return Response(status=status.HTTP_200_OK)
