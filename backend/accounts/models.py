"""
User Account Models

This module contains models for user management, profiles, wallets, 
transactions, and subscription management for the AI ChatBot application.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from decimal import Decimal


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Adds fields specific to the AI ChatBot application.
    """
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Subscription fields
    is_premium = models.BooleanField(default=False)
    premium_until = models.DateTimeField(null=True, blank=True)
    free_tier_expires = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'auth_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.email
    
    @property
    def is_in_free_tier(self):
        """Check if user is still in free tier period."""
        if not self.free_tier_expires:
            return False
        return timezone.now() < self.free_tier_expires
    
    @property
    def has_active_premium(self):
        """Check if user has active premium subscription."""
        if not self.is_premium or not self.premium_until:
            return False
        return timezone.now() < self.premium_until


class UserProfile(models.Model):
    """
    Extended user profile information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    company = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    
    # Preferences
    language = models.CharField(max_length=10, default='en')
    timezone = models.CharField(max_length=50, default='UTC')
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email}'s Profile"


class Wallet(models.Model):
    """
    User wallet for prepaid balance management.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    currency = models.CharField(max_length=3, default='USD')
    
    # Alert thresholds
    low_balance_threshold = models.DecimalField(
        max_digits=10, decimal_places=2, 
        default=Decimal('10.00'),
        help_text="Alert when balance drops below this amount"
    )
    auto_recharge_enabled = models.BooleanField(default=False)
    auto_recharge_amount = models.DecimalField(
        max_digits=10, decimal_places=2, 
        default=Decimal('50.00')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'wallets'
    
    def __str__(self):
        return f"{self.user.email}'s Wallet - {self.balance} {self.currency}"
    
    @property
    def is_low_balance(self):
        """Check if wallet balance is below threshold."""
        return self.balance <= self.low_balance_threshold
    
    def add_balance(self, amount, description=""):
        """Add money to wallet."""
        self.balance += Decimal(str(amount))
        self.save()
        
        # Create transaction record
        Transaction.objects.create(
            wallet=self,
            transaction_type='CREDIT',
            amount=amount,
            description=description,
            status='COMPLETED'
        )
    
    def deduct_balance(self, amount, description=""):
        """Deduct money from wallet."""
        amount_decimal = Decimal(str(amount))
        if self.balance >= amount_decimal:
            self.balance -= amount_decimal
            self.save()
            
            # Create transaction record
            Transaction.objects.create(
                wallet=self,
                transaction_type='DEBIT',
                amount=amount,
                description=description,
                status='COMPLETED'
            )
            return True
        return False


class Transaction(models.Model):
    """
    Transaction history for wallet operations.
    """
    TRANSACTION_TYPES = [
        ('CREDIT', 'Credit'),
        ('DEBIT', 'Debit'),
        ('REFUND', 'Refund'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    
    # Payment gateway details
    payment_gateway = models.CharField(max_length=50, null=True, blank=True)
    gateway_transaction_id = models.CharField(max_length=100, null=True, blank=True)
    gateway_response = models.JSONField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'transactions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.wallet.user.email} - {self.transaction_type} - {self.amount}"


class Subscription(models.Model):
    """
    User subscription plans and history.
    """
    PLAN_TYPES = [
        ('FREE', 'Free Tier'),
        ('BASIC', 'Basic Plan'),
        ('PREMIUM', 'Premium Plan'),
        ('ENTERPRISE', 'Enterprise Plan'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
        ('CANCELLED', 'Cancelled'),
        ('SUSPENDED', 'Suspended'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    
    # Plan details
    monthly_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    query_limit = models.IntegerField(default=100)
    token_limit = models.IntegerField(default=10000)
    
    # Subscription period
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    auto_renewal = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'subscriptions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.plan_type} - {self.status}"
    
    @property
    def is_active(self):
        """Check if subscription is currently active."""
        return (
            self.status == 'ACTIVE' and 
            timezone.now() <= self.end_date
        )
