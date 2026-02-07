from django.urls import path
from .views import index, api_generate_mcq, api_solve, api_solve_routed

urlpatterns = [
    path("", index, name="index"),
    path("api/mcq", api_generate_mcq),
    path("api/solve", api_solve),
    path("api/solve_auto", api_solve_routed),
]