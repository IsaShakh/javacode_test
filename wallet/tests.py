
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Wallet
from django.urls import reverse
from uuid import uuid4

class WalletAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.wallet = Wallet.objects.create(uuid=uuid4(), balance=1000)

    def test_wallet_balance_not_found(self):
        url = reverse('wallet-detail', args=[uuid4()])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertIn('detail', response.data)

    def test_wallet_operation_invalid_data(self):
        url = reverse('wallet-create-operation', args=[self.wallet.uuid])
        response = self.client.post(url, {'invalid_field': 'invalid_value'}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('detail', response.data)

    def test_wallet_operation_insufficient_funds(self):
        url = reverse('wallet-create-operation', args=[self.wallet.uuid])
        response = self.client.post(url, {'operation_type': 'WITHDRAW', 'amount': 5000}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], 'Недостаточно средств')
