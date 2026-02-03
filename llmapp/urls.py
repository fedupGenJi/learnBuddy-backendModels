from django.urls import path
from .views import index, api_generate_mcq, api_solve

urlpatterns = [
    path("", index, name="index"),
    path("api/mcq", api_generate_mcq),
    path("api/solve", api_solve),
]
