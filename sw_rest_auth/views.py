# coding: utf-8
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from . import serializers


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def check_token(request):
    serializer = serializers.CheckToken(data=request.data)
    serializer.is_valid(raise_exception=True)
    token = serializer.validated_data['token']
    return Response({'username': token.user.username})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def check_perm(request):
    serializer = serializers.CheckPerm(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    return Response({'result': 'ok'})
