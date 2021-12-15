from django.urls import path
from . import views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('book/', views.getBooks),
    path('review/<int:book_id>', views.review),
    path('review_list/<int:book_id>', views.review_list),
    path('userHome/<str:name>', views.userHome),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.register)
]