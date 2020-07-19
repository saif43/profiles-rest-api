from rest_framework.views import APIView
from rest_framework.response import Response


class HelloApiView(APIView):
    """Test API View"""

    def get(self, request, format=None):
        result = [1, 2, 3, 4, 5]

        return Response({"message": "Hello", "result": result})

