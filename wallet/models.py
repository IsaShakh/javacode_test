from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Wallet(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, verbose_name='UUID')
    balance = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Баланс')

    def __str__(self) -> str:
        return f'Кошелек № {uuid4}'
    
    class Meta:
        verbose_name = 'Кошелек'
        verbose_name_plural = 'Кошельки'


class Operation(models.Model):
    class Type(models.TextChoices):
        DEPOSIT = 'DEPOSIT', _('Deposit')
        WITHDRAW = 'WITHDRAW', _('Withdraw')

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE,verbose_name='Кошелек')
    operation_type = models.CharField(max_length=8, choices=Type.choices, verbose_name='Тип операции')
    sum_of_operation = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Сумма операции')
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name='Выполнена в:')

    def __str__(self) -> str:
        return f'Операция {operation_type} по кошельку {wallet}'
    
    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'