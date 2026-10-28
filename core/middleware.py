from django.utils import translation
from django.conf import settings

class QueryParameterLanguageMiddleware:
    """
    So'rovda yuborilgan '?lang=uz|ru|en' parametrini o'qib olib,
    tizim tilini (request tili) shu tilga o'zgartiruvchi middleware.
    
    Bu API so'rovlarini brauzer, Swagger yoki Postman orqali
    ?lang=ru yoki ?lang=en ko'rinishida oson tekshirish imkonini beradi.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. URL parametri orqali kelgan tilni tekshiramiz (?lang=ru kabi)
        lang = request.GET.get('lang')
        valid_languages = [code for code, name in settings.LANGUAGES]

        if lang and lang in valid_languages:
            # Agar ko'rsatilgan til loyihada mavjud bo'lsa, uni aktivlashtiramiz
            translation.activate(lang)
            request.LANGUAGE_CODE = lang
        elif hasattr(request, 'LANGUAGE_CODE') and request.LANGUAGE_CODE:
            # Aks holda LocaleMiddleware tomonidan aniqlangan tilni aktivlashtiramiz
            translation.activate(request.LANGUAGE_CODE)

        response = self.get_response(request)

        # Har bir javobga tanlangan til kodini header sifatida ham qo'shib qaytaramiz
        current_lang = translation.get_language()
        response['Content-Language'] = current_lang
        return response
