from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from rest_framework import serializers
from .models import Wallet, Category, Transaction


class UserSerializer(serializers.ModelSerializer):
    """
    Foydalanuvchini ro'yxatdan o'tkazish uchun serializer.
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class WalletSerializer(serializers.ModelSerializer):
    """
    Hamyonlar (Wallet) uchun serializer.
    3 ta tilda (uz, ru, en) nomlarni qabul qilish va qaytarishni to'liq qo'llab-quvvatlaydi.
    - 'name': joriy faol tildagi nom (Accept-Language yoki ?lang parametriga qarab avtomatik o'zgaradi)
    - 'name_uz', 'name_ru', 'name_en': aniq tildagi nomlar
    """
    name_uz = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    name_ru = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    name_en = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Wallet
        fields = ('id', 'name', 'name_uz', 'name_ru', 'name_en', 'wallet_type', 'balance', 'currency')
        read_only_fields = ('user', 'balance')


class CategorySerializer(serializers.ModelSerializer):
    """
    Kategoriyalar (Category) uchun serializer.
    3 ta tilda (uz, ru, en) nomlarni qabul qilish va qaytarishni to'liq qo'llab-quvvatlaydi.
    - 'name': joriy faol tildagi kategoriya nomi
    - 'name_uz', 'name_ru', 'name_en': har bir til uchun alohida nomlar
    """
    name_uz = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    name_ru = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    name_en = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'name_uz', 'name_ru', 'name_en', 'category_type')
        read_only_fields = ('user',)


class TransactionSerializer(serializers.ModelSerializer):
    """
    Tranzaksiyalar (Transaction) uchun serializer.
    Izohni 3 ta tilda (description_uz, description_ru, description_en) saqlay oladi.
    Xatolik xabarlari (validation errors) tanlangan tilga mos holda 3 tilda qaytariladi.
    """
    description_uz = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    description_ru = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    description_en = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Transaction
        fields = (
            'id', 'wallet', 'category', 'amount', 'transaction_type',
            'description', 'description_uz', 'description_ru', 'description_en',
            'transaction_date', 'created_at'
        )
        read_only_fields = ('user', 'created_at')

    def validate(self, data):
        # Foydalanuvchi ma'lumotlarini tekshirish
        request = self.context.get('request')
        user = request.user if request else None

        wallet = data.get('wallet')
        category = data.get('category')

        # 3 ta tilda tarjima qilinadigan xatolik xabarlari (Django gettext orqali):
        if wallet and user and wallet.user != user:
            raise serializers.ValidationError({"wallet": _("Bu hamyon sizga tegishli emas.")})

        if category and user and category.user != user:
            raise serializers.ValidationError({"category": _("Bu kategoriya sizga tegishli emas.")})

        # Tranzaksiya turi va kategoriya turi mos kelishini tekshirish
        if data.get('transaction_type') and category and data.get('transaction_type') != category.category_type:
            raise serializers.ValidationError({"category": _("Kategoriya turi tranzaksiya turiga mos kelmaydi.")})

        return data