from django.urls import path
from .views import conversion_page, convert, upload, conversion

urlpatterns = [
    path('', conversion_page, name='conversion_page'),
    path('convert/<docxfile>/', conversion, name='conversion'),
    path('upload/', upload, name='upload')
]
