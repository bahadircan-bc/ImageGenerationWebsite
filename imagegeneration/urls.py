from django.contrib import admin
from django.urls import path
from .views import generate_any_image, index, generate_with_prompt

urlpatterns = [
    path('<int:height>/<int:width>/any/', generate_any_image),
    path('<int:height>/<int:width>/', generate_any_image),
    path('<int:height>/<int:width>/<str:prompt>/', generate_with_prompt),
    path('', index)
]
