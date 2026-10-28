from modeltranslation.translator import register, TranslationOptions
from .models import Wallet, Category, Transaction

# Hamyon (Wallet) modelini 3 ta tilda (uz, ru, en) tarjima qilish sozlamasi
@register(Wallet)
class WalletTranslationOptions(TranslationOptions):
    # 'name' maydoni 3 tilda saqlanadi: name_uz, name_ru, name_en
    fields = ('name',)

# Kategoriya (Category) modelini 3 ta tilda (uz, ru, en) tarjima qilish sozlamasi
@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    # 'name' maydoni 3 tilda saqlanadi: name_uz, name_ru, name_en
    fields = ('name',)

# Tranzaksiya (Transaction) modelining izohini ham ixtiyoriy 3 tilda qo'llab-quvvatlash
@register(Transaction)
class TransactionTranslationOptions(TranslationOptions):
    # 'description' maydoni 3 tilda saqlanadi: description_uz, description_ru, description_en
    fields = ('description',)
