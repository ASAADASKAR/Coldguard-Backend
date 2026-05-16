from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Device
from .serializers import CustomerSerializer, DeviceSerializer


class CustomerAPIView(APIView):
    """
    Manages ColdGuard customers.
    GET  /api/customers/ — list all customers
    POST /api/customers/ — create new customer
    """

    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class DeviceAPIView(APIView):
    """
    Manages ColdGuard devices.
    GET  /api/devices/ — list all devices
    POST /api/devices/ — register new device
    """

    def get(self, request):
        devices = Device.objects.all()
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )