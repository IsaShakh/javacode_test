from django.contrib import admin
from .models import Wallet, Operation

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'balance')
    search_fields = ('uuid',)
    readonly_fields = ('uuid',)

@admin.register(Operation)
class WalletOperationAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'operation_type', 'sum_of_operation', 'completed_at')
    list_filter = ('operation_type',)
    search_fields = ('wallet__uuid',)
    readonly_fields = ('wallet', 'operation_type', 'sum_of_operation', 'completed_at')
