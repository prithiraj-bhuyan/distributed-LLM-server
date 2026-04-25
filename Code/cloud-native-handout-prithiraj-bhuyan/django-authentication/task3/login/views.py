from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from task3.login.serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError
import jwt
from django.conf import settings

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class MyTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        # re-write the access token to make KrakenD happy.
        def add_kid_header(mat):
            payload = jwt.decode(mat, options={"verify_signature": False})
            new_token = jwt.encode(
                payload, 
                settings.SIMPLE_JWT['SIGNING_KEY'],
                algorithm='RS256', 
                headers={'kid': 'mycoolkid'}
            )
            return new_token

        serializer.validated_data['access']  = add_kid_header(serializer.validated_data['access'])
        serializer.validated_data['refresh'] = add_kid_header(serializer.validated_data['refresh'])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)