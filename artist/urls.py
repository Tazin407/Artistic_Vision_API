from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .import views
from  art.views import Artworks, Like

router = DefaultRouter()
router.register('Artists',views.Artists)
router.register('artworks',Artworks)
router.register('likes',Like)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegistrationAPIView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>', views.activate,name='activate' ),
]