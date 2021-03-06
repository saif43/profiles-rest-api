from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from profiles_api import serializers, models
from profiles_api import permissions


class HelloApiView(APIView):
    """Test API View"""

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        result = [1, 2, 3, 4, 5]
        result.append("APIView")

        return Response({"message": "Hello", "result": result})

    def post(self, request):
        """Create a post request with our name"""

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            msg = f"Hello {name}"
            return Response({"message": msg})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({"method": "PUT"})

    def patch(self, request, pk=None):
        """Handle partial update of an object"""
        return Response({"method": "PATCH"})

    def delete(self, request, pk=None):
        """Handle updating an object"""
        return Response({"method": "DELETE"})


class HelloViewSet(viewsets.ViewSet):
    """Test API viewset"""

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """return a Hello msg"""
        result = [1, 2, 3, 4, 5]
        result.append("View set")

        return Response({"message": "Hello", "result": result})

    def create(self, request):
        """Create a Hello msg"""

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            message = f"Hello {name}"

            return Response({"message": message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle getting an object by ID"""

        return Response({"HTTP method": "GET"})

    def update(self, request, pk=None):
        """Update an object by ID"""

        return Response({"HTTP method": "PUT"})

    def partial_update(self, request, pk=None):
        """Update an object by ID"""

        return Response({"HTTP method": "PATCH"})

    def destroy(self, request, pk=None):
        """delete an object by ID"""

        return Response({"HTTP method": "DELETE"})


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UserOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        "name",
        "email",
    )


class UserLoginApiView(ObtainAuthToken):
    """Create user authentication token"""

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ProfileFeedItemView(viewsets.ModelViewSet):
    """Handling creating, reading, updating profile feed item"""

    serializer_class = serializers.ProfileFeedItemSerializer
    authentication_classes = (TokenAuthentication,)

    queryset = models.ProfileFeedItem.objects.all()

    permission_classes = (
        IsAuthenticatedOrReadOnly,
        permissions.UpdateOwnStatus
    )

    def perform_create(self, serializer):
        """Sets the user as Logged in user"""
        serializer.save(user_profile=self.request.user)
