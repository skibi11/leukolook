# config/urls.py

from django.contrib import admin
from django.urls import path
from django.http import HttpResponse  # <--- IMPORT THIS
from api.views import EyeDetectionView

# A simple view to handle requests to the root URL
def home(request):
    return HttpResponse("LeukoLook API is active.", status=200)

urlpatterns = [
    path('admin/', admin.site.urls),

    # This is your main API endpoint
    path('api/eye-detect/', EyeDetectionView.as_view(), name='eye_detect'),

    # This new path handles the root URL "/"
    path('', home, name='home'), # <--- ADD THIS LINE
]