from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Wallet, Category, Transaction

# Hamyon (Wallet) admin paneli: 3 tilda kiritish imkoniyati bilan
@admin.register(Wallet)
class WalletAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'wallet_type', 'balance', 'currency', 'user')
    search_fields = ('name_uz', 'name_ru', 'name_en', 'user__username')
    list_filter = ('wallet_type', 'currency')

# Kategoriya (Category) admin paneli: 3 tilda kiritish imkoniyati bilan
@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'category_type', 'user')
    search_fields = ('name_uz', 'name_ru', 'name_en', 'user__username')
    list_filter = ('category_type',)

# Tranzaksiya (Transaction) admin paneli: izohni 3 tilda kiritish imkoniyati bilan
@admin.register(Transaction)
class TransactionAdmin(TranslationAdmin):
    list_display = ('id', 'user', 'wallet', 'category', 'amount', 'transaction_type', 'transaction_date')
    search_fields = ('description_uz', 'description_ru', 'description_en', 'user__username', 'wallet__name')
    list_filter = ('transaction_type', 'transaction_date')