from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from profiles_api import serializers

class HelloAPIView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a dictionary"""

        an_apiview = ['1','2','3','4']

        return Response({'message': 'Hello', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = 'Hello {}'.format(name)

            return Response({'message': message})
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)