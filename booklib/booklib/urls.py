"""
URL configuration for booklib project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from library.views import AuthorAPI, BookAPI, FavoriteBookAPI
from users.views import UserRegisterAPIView

router = DefaultRouter()
router.register(r'books', BookAPI)
router.register(r'authors', AuthorAPI)
router.register(r'fav-book', FavoriteBookAPI)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', UserRegisterAPIView.as_view(), name='register_user'),

]

urlpatterns += router.urls