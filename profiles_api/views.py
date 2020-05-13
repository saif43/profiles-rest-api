from rest_framework.views import APIView
from rest_framework.response import Response

class HelloAPIView(APIView):
    """Test API View"""

    def get(self, request, format=None):
        """Returns a dictionary"""

        an_apiview = ['1','2','3','4']

        return Response({'message': 'Hello', 'an_apiview': an_apiview})