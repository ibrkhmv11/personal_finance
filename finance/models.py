from django.db import models
from django.contrib.auth.models import User


class Wallet(models.Model):
    WALLET_TYPES = (
        ('cash', 'Naqd pul'),
        ('card', 'Karta (Uzcard/Humo)'),
        ('visa', 'Visa Karta'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets', verbose_name="Foydalanuvchi")
    name = models.CharField(max_length=100, verbose_name="Hamyon nomi")
    wallet_type = models.CharField(max_length=20, choices=WALLET_TYPES, default='cash', verbose_name="Hamyon turi")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Balans")
    currency = models.CharField(max_length=10, default='UZS', verbose_name="Valyuta")

    def __str__(self):
        return f"{self.name} ({self.get_wallet_type_display()}) - {self.balance} {self.currency}"


class Category(models.Model):
    CATEGORY_TYPES = (
        ('income', 'Kirim'),
        ('expense', 'Chiqim'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories', verbose_name="Foydalanuvchi")
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPES, verbose_name="Turi")

    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Kirim'),
        ('expense', 'Chiqim'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions', verbose_name="Foydalanuvchi")
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions', verbose_name="Hamyon")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='transactions',
                                 verbose_name="Kategoriya")

    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Summa")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, verbose_name="Tranzaksiya turi")
    description = models.TextField(blank=True, null=True, verbose_name="Izoh")

    transaction_date = models.DateTimeField(verbose_name="Tranzaksiya vaqti")  # Foydalanuvchi ko'rsatadigan sana/vaqt
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Tizimga kiritilgan vaqt")  # Avtomatik yoziladigan vaqt

    def __str__(self):
        return f"{self.transaction_type}: {self.amount} - {self.wallet.name}"
