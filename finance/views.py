from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, inline_serializer
from rest_framework import serializers as drf_serializers

from .models import Transaction, Wallet, Category
from .serializers import (
    UserSerializer,
    WalletSerializer,
    CategorySerializer,
    TransactionSerializer
)

# Swagger va testlash uchun umumiy til parametri (uz, ru, en)
lang_query_param = OpenApiParameter(
    name='lang',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description="Tilni tanlash: uz (O'zbekcha), ru (Русский), en (English)",
    enum=['uz', 'ru', 'en'],
    default='uz'
)


class RegisterView(APIView):
    """
    Yangi foydalanuvchini ro'yxatdan o'tkazish.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Yangi foydalanuvchi ro'yxatdan o'tkazish",
        description="Foydalanuvchi nomi (username), email va parol orqali yangi hisob ochadi.",
        request=UserSerializer,
        responses={201: UserSerializer}
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    Foydalanuvchi seansini yakunlash (Tokenni o'chirish).
    Xabar 3 ta tilda (uz, ru, en) qaytariladi.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Tizimdan chiqish (Logout)",
        description="Foydalanuvchi tokenini o'chiradi va tanlangan tilda tasdiq xabarini beradi.",
        request=None,
        parameters=[lang_query_param],
        responses={200: inline_serializer('LogoutResponse', fields={'message': drf_serializers.CharField()})}
    )
    def post(self, request):
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()
        return Response(
            {"message": _("Tizimdan muvaffaqiyatli chiqildi.")},
            status=status.HTTP_200_OK
        )


class WalletListCreateAPIView(APIView):
    """
    Hamyonlar ro'yxatini olish va yangi hamyon yaratish.
    3 tildagi nomlarni (name_uz, name_ru, name_en) qo'llab-quvvatlaydi.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Hamyonlar ro'yxatini olish",
        description="Foydalanuvchining barcha hamyonlarini tanlangan tildagi nomlari bilan qaytaradi.",
        parameters=[lang_query_param],
        responses={200: WalletSerializer(many=True)}
    )
    def get(self, request):
        wallets = Wallet.objects.filter(user=request.user)
        serializer = WalletSerializer(wallets, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Yangi hamyon yaratish (3 tilda)",
        description="Yangi hamyon qo'shadi. Nomni 'name' (joriy til uchun) yoki 'name_uz', 'name_ru', 'name_en' ko'rinishida berish mumkin.",
        request=WalletSerializer,
        responses={201: WalletSerializer}
    )
    def post(self, request):
        serializer = WalletSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WalletDetailAPIView(APIView):
    """
    Bitta hamyonni ko'rish, yangilash va o'chirish.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Wallet, pk=pk, user=user)

    @extend_schema(
        summary="Hamyon tafsilotlarini ko'rish",
        parameters=[lang_query_param],
        responses={200: WalletSerializer}
    )
    def get(self, request, pk):
        wallet = self.get_object(pk, request.user)
        serializer = WalletSerializer(wallet, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Hamyon ma'lumotlarini yangilash",
        request=WalletSerializer,
        responses={200: WalletSerializer}
    )
    def put(self, request, pk):
        wallet = self.get_object(pk, request.user)
        serializer = WalletSerializer(wallet, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Hamyonni o'chirish",
        parameters=[lang_query_param],
        responses={200: OpenApiTypes.OBJECT}
    )
    def delete(self, request, pk):
        wallet = self.get_object(pk, request.user)
        wallet.delete()
        return Response(
            {"message": _("Hamyon o'chirildi.")},
            status=status.HTTP_200_OK
        )


class CategoryListCreateAPIView(APIView):
    """
    Kategoriyalar ro'yxati va yangi kategoriya yaratish (3 tilda).
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Kategoriyalar ro'yxatini olish",
        description="Foydalanuvchining daromad va xarajat kategoriyalari ro'yxati.",
        parameters=[lang_query_param],
        responses={200: CategorySerializer(many=True)}
    )
    def get(self, request):
        categories = Category.objects.filter(user=request.user)
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Yangi kategoriya yaratish (3 tilda)",
        request=CategorySerializer,
        responses={201: CategorySerializer}
    )
    def post(self, request):
        serializer = CategorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailAPIView(APIView):
    """
    Bitta kategoriyani ko'rish, tahrirlash va o'chirish.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Category, pk=pk, user=user)

    @extend_schema(
        summary="Kategoriya tafsilotlarini olish",
        parameters=[lang_query_param],
        responses={200: CategorySerializer}
    )
    def get(self, request, pk):
        category = self.get_object(pk, request.user)
        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Kategoriyani tahrirlash",
        request=CategorySerializer,
        responses={200: CategorySerializer}
    )
    def put(self, request, pk):
        category = self.get_object(pk, request.user)
        serializer = CategorySerializer(category, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Kategoriyani o'chirish",
        parameters=[lang_query_param],
        responses={200: OpenApiTypes.OBJECT}
    )
    def delete(self, request, pk):
        category = self.get_object(pk, request.user)
        category.delete()
        return Response(
            {"message": _("Kategoriya o'chirildi.")},
            status=status.HTTP_200_OK
        )


class TransactionListCreateAPIView(APIView):
    """
    Tranzaksiyalar ro'yxati (filtrlash bilan) va yangi tranzaksiya qo'shish.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Tranzaksiyalar ro'yxatini olish (Filtrlash bilan)",
        parameters=[
            lang_query_param,
            OpenApiParameter('wallet', OpenApiTypes.INT, description="Hamyon ID bo'yicha filter"),
            OpenApiParameter('category', OpenApiTypes.INT, description="Kategoriya ID bo'yicha filter"),
            OpenApiParameter('type', OpenApiTypes.STR, enum=['income', 'expense'], description="Tranzaksiya turi"),
            OpenApiParameter('start_date', OpenApiTypes.DATE, description="Boshlanish sanasi (YYYY-MM-DD)"),
            OpenApiParameter('end_date', OpenApiTypes.DATE, description="Tugash sanasi (YYYY-MM-DD)"),
        ],
        responses={200: TransactionSerializer(many=True)}
    )
    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user).order_by('-transaction_date')

        wallet_id = request.query_params.get('wallet')
        category_id = request.query_params.get('category')
        trans_type = request.query_params.get('type')  # income yoki expense
        start_date = request.query_params.get('start_date')  # YYYY-MM-DD
        end_date = request.query_params.get('end_date')      # YYYY-MM-DD

        if wallet_id:
            transactions = transactions.filter(wallet_id=wallet_id)
        if category_id:
            transactions = transactions.filter(category_id=category_id)
        if trans_type:
            transactions = transactions.filter(transaction_type=trans_type)
        if start_date:
            transactions = transactions.filter(transaction_date__gte=start_date)
        if end_date:
            transactions = transactions.filter(transaction_date__lte=end_date)

        serializer = TransactionSerializer(transactions, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Yangi tranzaksiya yaratish",
        description="Kirim yoki chiqim tranzaksiyasini qo'shadi va hamyon balansini avtomatik yangilaydi.",
        request=TransactionSerializer,
        responses={201: TransactionSerializer}
    )
    def post(self, request):
        serializer = TransactionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            transaction = serializer.save(user=request.user)

            # Hamyon balansini yangilash
            wallet = transaction.wallet
            if transaction.transaction_type == 'income':
                wallet.balance += transaction.amount
            elif transaction.transaction_type == 'expense':
                wallet.balance -= transaction.amount
            wallet.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetailAPIView(APIView):
    """
    Bitta tranzaksiyani ko'rish va o'chirish (balansni tiklash bilan).
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Transaction, pk=pk, user=user)

    @extend_schema(
        summary="Tranzaksiya tafsilotlarini ko'rish",
        parameters=[lang_query_param],
        responses={200: TransactionSerializer}
    )
    def get(self, request, pk):
        transaction = self.get_object(pk, request.user)
        serializer = TransactionSerializer(transaction, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Tranzaksiyani o'chirish",
        description="Tranzaksiyani o'chiradi va hamyondagi balansni qayta tiklaydi.",
        parameters=[lang_query_param],
        responses={200: OpenApiTypes.OBJECT}
    )
    def delete(self, request, pk):
        transaction = self.get_object(pk, request.user)

        # Balansni qaytarish
        wallet = transaction.wallet
        if transaction.transaction_type == 'income':
            wallet.balance -= transaction.amount
        elif transaction.transaction_type == 'expense':
            wallet.balance += transaction.amount
        wallet.save()

        transaction.delete()
        return Response(
            {"message": _("Tranzaksiya o'chirildi va balans yangilandi.")},
            status=status.HTTP_200_OK
        )


class StatisticsAPIView(APIView):
    """
    Foydalanuvchining moliyaviy umumiy statistikasi.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Umumiy moliya statistikasi",
        description="Jami balans, jami kirim, jami chiqim, sof jamg'arma va hamyonlar ro'yxatini qaytaradi.",
        parameters=[
            lang_query_param,
            OpenApiParameter('start_date', OpenApiTypes.DATE, description="Boshlanish sanasi"),
            OpenApiParameter('end_date', OpenApiTypes.DATE, description="Tugash sanasi"),
        ],
        responses={200: OpenApiTypes.OBJECT}
    )
    def get(self, request):
        user = request.user

        wallets = Wallet.objects.filter(user=user)
        total_balance = wallets.aggregate(total=Sum('balance'))['total'] or 0.00
        wallets_data = WalletSerializer(wallets, many=True, context={'request': request}).data

        transactions = Transaction.objects.filter(user=user)

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if start_date:
            transactions = transactions.filter(transaction_date__gte=start_date)
        if end_date:
            transactions = transactions.filter(transaction_date__lte=end_date)

        total_income = transactions.filter(transaction_type='income').aggregate(total=Sum('amount'))['total'] or 0.00
        total_expense = transactions.filter(transaction_type='expense').aggregate(total=Sum('amount'))['total'] or 0.00

        data = {
            "total_balance": total_balance,
            "total_income": total_income,
            "total_expense": total_expense,
            "net_savings": total_income - total_expense,
            "wallets": wallets_data
        }

        return Response(data, status=status.HTTP_200_OK)