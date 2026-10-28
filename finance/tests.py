from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import translation
from django.utils.translation import gettext as _
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import Wallet, Category, Transaction


class MultilingualTestCase(TestCase):
    """
    3 ta tilda (uz, ru, en) ishlashini tekshiruvchi testlar.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_gettext_translations(self):
        """Tizim xabarlarining 3 tilda tarjima qilinishini tekshirish."""
        translation.activate('uz')
        self.assertEqual(_("Hamyon o'chirildi."), "Hamyon o'chirildi.")

        translation.activate('ru')
        self.assertEqual(_("Hamyon o'chirildi."), "Кошелек удален.")

        translation.activate('en')
        self.assertEqual(_("Hamyon o'chirildi."), "Wallet deleted.")

    def test_modeltranslation_wallet(self):
        """Model maydonlarining 3 tilda saqlanishi va qaytarilishini tekshirish."""
        wallet = Wallet.objects.create(
            user=self.user,
            name_uz='Asosiy hamyon',
            name_ru='Основной кошелек',
            name_en='Main wallet',
            balance=500000,
            currency='UZS'
        )

        translation.activate('uz')
        self.assertEqual(wallet.name, 'Asosiy hamyon')

        translation.activate('ru')
        self.assertEqual(wallet.name, 'Основной кошелек')

        translation.activate('en')
        self.assertEqual(wallet.name, 'Main wallet')

    def test_api_language_via_query_param(self):
        """API orqali ?lang= parametri bilan ma'lumot olishni tekshirish."""
        Wallet.objects.create(
            user=self.user,
            name_uz='Plastik karta',
            name_ru='Пластиковая карта',
            name_en='Plastic card',
            balance=100000,
            currency='UZS'
        )

        # 1. O'zbekcha
        res_uz = self.client.get('/api/wallets/?lang=uz')
        self.assertEqual(res_uz.status_code, 200)
        self.assertEqual(res_uz.json()[0]['name'], 'Plastik karta')

        # 2. Ruscha
        res_ru = self.client.get('/api/wallets/?lang=ru')
        self.assertEqual(res_ru.status_code, 200)
        self.assertEqual(res_ru.json()[0]['name'], 'Пластиковая карта')

        # 3. Inglizcha
        res_en = self.client.get('/api/wallets/?lang=en')
        self.assertEqual(res_en.status_code, 200)
        self.assertEqual(res_en.json()[0]['name'], 'Plastic card')

    def test_api_language_via_accept_language_header(self):
        """API orqali HTTP Accept-Language sarlavhasi bilan ma'lumot olishni tekshirish."""
        Wallet.objects.create(
            user=self.user,
            name_uz='Jamg‘arma',
            name_ru='Сбережения',
            name_en='Savings',
            balance=200000,
            currency='UZS'
        )

        res_ru = self.client.get('/api/wallets/', HTTP_ACCEPT_LANGUAGE='ru')
        self.assertEqual(res_ru.status_code, 200)
        self.assertEqual(res_ru.json()[0]['name'], 'Сбережения')

        res_en = self.client.get('/api/wallets/', HTTP_ACCEPT_LANGUAGE='en')
        self.assertEqual(res_en.status_code, 200)
        self.assertEqual(res_en.json()[0]['name'], 'Savings')
