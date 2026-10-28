"""
Django settings for core project.
3 ta tilda (O'zbekcha, Ruscha, Inglizcha) to'liq ishga tushirish uchun sozlangan.
"""

from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Asosiy loyiha katalogi
BASE_DIR = Path(__file__).resolve().parent.parent

# Xavfsizlik kaliti (Production muhitida maxfiy tutilishi shart)
SECRET_KEY = 'django-insecure-=jt)d^jif-ldm=_=bb-k*(n*tfsy=07!7vmuja#%67jaz1kq(h'

# Debug rejimi
DEBUG = True

ALLOWED_HOSTS = ['*']


# ==============================================================================
# O'RNATILGAN ILOVALAR (INSTALLED_APPS)
# ==============================================================================
INSTALLED_APPS = [
    # DIQQAT: modeltranslation ilovasi django.contrib.admin dan OLDIN turishi SHART!
    # Bu orqali Django Admin panelida tillar bo'yicha maydonlar (tablar) to'g'ri ko'rinadi.
    'modeltranslation',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Uchinchi tomon kutubxonalari
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',

    # Loyihaning asosiy ilovasi
    'finance.apps.FinanceConfig',
]


# ==============================================================================
# MIDDLEWARE (ORALIQ DASTURLAR)
# ==============================================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # 1. Django rasmiy til oraliq dasturi (LocaleMiddleware):
    # Har bir HTTP so'rovdagi 'Accept-Language' sarlavhasi (header) va cookie orqali tilni aniqlaydi.
    # U doimo SessionMiddleware dan keyin va CommonMiddleware dan oldin joylashishi lozim.
    'django.middleware.locale.LocaleMiddleware',

    # 2. Maxsus qo'shimcha middleware:
    # URL parametri orqali kelgan tilni (?lang=uz, ?lang=ru, ?lang=en) darhol aktivlashtiradi
    # va Content-Language sarlavhasini javobga qo'shadi.
    'core.middleware.QueryParameterLanguageMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Shablonlarda (templates) joriy til va tillar ro'yxatidan foydalanish uchun:
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# ==============================================================================
# MA'LUMOTLAR BAZASI (DATABASES)
# ==============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ==============================================================================
# PAROLNI TEKSHIRISH (AUTH PASSWORD VALIDATORS)
# ==============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ==============================================================================
# 3 TA TILNI SOZLASH (INTERNATIONALIZATION - i18n & l10n)
# ==============================================================================
# Xalqaro tillar tizimini yoqish
USE_I18N = True

# Loyihaning standart/boshlang'ich tili - O'zbek tili ('uz')
LANGUAGE_CODE = 'uz'

# Loyihada qo'llab-quvvatlanadigan umumiy 3 ta til ro'yxati
LANGUAGES = [
    ('uz', _("O'zbekcha")),
    ('ru', _('Русский')),
    ('en', _('English')),
]

# Tizim xabarlari (.po va .mo fayllar) saqlanadigan papka
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Django ModelTranslation kutubxonasi uchun 3 ta til sozlamalari
MODELTRANSLATION_DEFAULT_LANGUAGE = 'uz'           # Standart til
MODELTRANSLATION_LANGUAGES = ('uz', 'ru', 'en')     # Bazada yaratiladigan ustunlar tillari (_uz, _ru, _en)
MODELTRANSLATION_FALLBACK_LANGUAGES = ('uz', 'ru', 'en')  # Agar biror tilda qiymat kiritilmagan bo'lsa, zaxira til
MODELTRANSLATION_PREPOPULATE_LANGUAGE = 'uz'

TIME_ZONE = 'Asia/Tashkent'
USE_TZ = True


# ==============================================================================
# STATIK FAYLLAR
# ==============================================================================
STATIC_URL = 'static/'


# ==============================================================================
# EMAIL VA BOSHQA SOZLAMALAR
# ==============================================================================
MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}


# ==============================================================================
# REST FRAMEWORK VA SWAGGER (DRF-SPECTACULAR)
# ==============================================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Wallet & Finance API (Multilingual: UZ / RU / EN)',
    'DESCRIPTION': 'Kirim-chiqim, hamyonlar va moliyaviy statistika API loyihasi. 3 ta tilda (uz, ru, en) ishlaydi.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}