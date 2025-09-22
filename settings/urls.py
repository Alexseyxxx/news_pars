"""
URL configuration for settings project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from users.views import RegisterViewSet, ActivateAccountViewSet
from news.views import ArticleListView, UpdateArticlesView

# Swagger schema
schema_view = get_schema_view(
    openapi.Info(
        title="News Service API",
        default_version="v1",
        description="API для экзамена",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Router для User
router = DefaultRouter()
router.register("auth/register", RegisterViewSet, basename="register")
router.register("auth/activate", ActivateAccountViewSet, basename="activate")

urlpatterns = [
    # редирект с / на Swagger
    path("", lambda request: redirect("swagger/")),

    # admin
    path("admin/", admin.site.urls),

    # JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Users (через router)
    path("api/", include(router.urls)),

    # Articles
    path("api/articles/", ArticleListView.as_view(), name="articles-list"),
    path("api/articles/update/", UpdateArticlesView.as_view(), name="articles-update"),

    # Swagger
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

   
]
