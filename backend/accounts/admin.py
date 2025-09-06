"""
Admin interface for Account models.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, UserProfile, Wallet, Transaction, Subscription


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin interface for custom User model.
    """
    list_display = (
        'email', 'username', 'first_name', 'last_name', 
        'is_verified', 'is_premium', 'wallet_balance', 'created_at'
    )
    list_filter = (
        'is_verified', 'is_premium', 'is_active', 'is_staff', 'created_at'
    )
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('phone', 'is_verified', 'is_premium', 'premium_until', 'free_tier_expires')
        }),
    )
    
    def wallet_balance(self, obj):
        """Display user's wallet balance."""
        try:
            return f"${obj.wallet.balance}"
        except:
            return "No wallet"
    wallet_balance.short_description = 'Wallet Balance'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for UserProfile model.
    """
    list_display = ('user', 'company', 'location', 'language', 'created_at')
    list_filter = ('language', 'email_notifications', 'sms_notifications')
    search_fields = ('user__email', 'company', 'location')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    """
    Admin interface for Wallet model.
    """
    list_display = (
        'user', 'balance_display', 'currency', 'low_balance_status', 
        'auto_recharge_enabled', 'updated_at'
    )
    list_filter = ('currency', 'auto_recharge_enabled')
    search_fields = ('user__email',)
    readonly_fields = ('created_at', 'updated_at')
    
    def balance_display(self, obj):
        """Display formatted balance."""
        color = 'red' if obj.is_low_balance else 'green'
        return format_html(
            '<span style="color: {};">{} {}</span>',
            color, obj.balance, obj.currency
        )
    balance_display.short_description = 'Balance'
    
    def low_balance_status(self, obj):
        """Display low balance warning."""
        if obj.is_low_balance:
            return format_html('<span style="color: red;">⚠️ Low Balance</span>')
        return '✅ OK'
    low_balance_status.short_description = 'Status'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Admin interface for Transaction model.
    """
    list_display = (
        'wallet', 'transaction_type', 'amount_display', 'status', 
        'payment_gateway', 'created_at'
    )
    list_filter = ('transaction_type', 'status', 'payment_gateway', 'created_at')
    search_fields = ('wallet__user__email', 'description', 'gateway_transaction_id')
    readonly_fields = ('created_at', 'updated_at')
    
    def amount_display(self, obj):
        """Display formatted amount with color coding."""
        color = 'green' if obj.transaction_type == 'CREDIT' else 'red'
        symbol = '+' if obj.transaction_type == 'CREDIT' else '-'
        return format_html(
            '<span style="color: {};">{}{}</span>',
            color, symbol, obj.amount
        )
    amount_display.short_description = 'Amount'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Admin interface for Subscription model.
    """
    list_display = (
        'user', 'plan_type', 'status_display', 'monthly_cost', 
        'start_date', 'end_date', 'auto_renewal'
    )
    list_filter = ('plan_type', 'status', 'auto_renewal', 'created_at')
    search_fields = ('user__email',)
    readonly_fields = ('created_at', 'updated_at')
    
    def status_display(self, obj):
        """Display status with color coding."""
        colors = {
            'ACTIVE': 'green',
            'EXPIRED': 'orange',
            'CANCELLED': 'red',
            'SUSPENDED': 'purple'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {};">{}</span>',
            color, obj.get_status_display()
        )
    status_display.short_description = 'Status'
