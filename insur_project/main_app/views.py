from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer, LicenseSerializer, VehicleSerializer
from .models import Users, Licenses, Vehicles


class ViewAll(APIView):

    def get(self, request):
        users = Users.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)


class UserDetail(APIView):

    def get(self, request, pk):

        e = Users.objects.prefetch_related('vehicles_set').select_related('licenses').get(id=pk)
        users = e
        vehicles = e.vehicles_set
        licenses = e.licenses
        serializer_user = UserSerializer(users)
        serializer_license = LicenseSerializer(licenses)
        serializer_vehicle = VehicleSerializer(vehicles, many=True)
        data = {'user': serializer_user.data, 'license': serializer_license.data, 'vehicle': serializer_vehicle.data}
        return Response(data)
