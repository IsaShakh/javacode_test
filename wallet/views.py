import uuid
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from .models import Wallet
from .serializers import WalletSerializer, OperationSerializer

# Create your views here.
class WalletViewSet(ViewSet):

    def retrieve(self, request, pk=None):
        if not self.is_valid_uuid(pk):
            return Response({"detail": "Неверный формат UUID"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            wallet = Wallet.objects.get(uuid=pk)
        except Wallet.DoesNotExist:
            return Response({"detail": "Кошелек не найден"}, status=status.HTTP_404_NOT_FOUND)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)

    def create_operation(self, request, pk=None):
        if not self.is_valid_uuid(pk):
            return Response({"detail": "Неверный формат UUID"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            wallet = Wallet.objects.get(uuid=pk)
        except Wallet.DoesNotExist:
            return Response({"detail": "Кошелек не найден"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OperationSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                operation_type = serializer.validated_data['operation_type']
                sum_of_operation = serializer.validated_data['sum_of_operation']
                if operation_type == 'DEPOSIT':
                    wallet.balance += sum_of_operation
                elif operation_type == 'WITHDRAW':
                    if wallet.balance < sum_of_operation:
                        return Response({"detail": "Недостаточно средств"}, status=status.HTTP_400_BAD_REQUEST)
                    wallet.balance -= sum_of_operation
                wallet.save()
                serializer.save(wallet=wallet)
            return Response(WalletSerializer(wallet).data)
        return Response(
            {"detail": "Неверный формат данных", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def is_valid_uuid(self, val):
        try:
            uuid.UUID(str(val))
            return True
        except ValueError:
            return False
