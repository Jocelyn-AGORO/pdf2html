from django.urls import path
from .views import conversion_page, convert, upload

urlpatterns = [
    path('', conversion_page, name='conversion_page'),
    path('convert/', convert, name='conversion'),
    path('upload/', upload, name='upload')
]
