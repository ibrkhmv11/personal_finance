import os
from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import render
from django.views import View


class TestUIView(View):
    """
    Postman kabi qulay va chiroyli interaktiv API testlash interfeysi (UI).
    3 ta tilda (uz, ru, en) barcha API larni brauzerning o'zida jonli sinash imkonini beradi.
    """
    def get(self, request):
        return render(request, 'api_tester.html')


class DownloadPostmanCollectionView(View):
    """
    Postmanga import qilish uchun tayyor Collection JSON faylini yuklab beradi.
    """
    def get(self, request):
        file_path = settings.BASE_DIR / 'Personal_Finance_API.postman_collection.json'
        if os.path.exists(file_path):
            return FileResponse(
                open(file_path, 'rb'),
                as_attachment=True,
                filename='Personal_Finance_API.postman_collection.json'
            )
        raise Http404("Postman collection fayli topilmadi.")
