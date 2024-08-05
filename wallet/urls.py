from django.urls import path

from .views import CreateWallet, SendToken

urlpatterns = [
    path('create/', CreateWallet.as_view()),
    path('send_token/', SendToken.as_view()),
]