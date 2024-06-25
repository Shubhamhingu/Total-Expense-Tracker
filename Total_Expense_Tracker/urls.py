from django.urls import path # type: ignore
from .views import add_shift, transactionresult, add_transaction, shiftresult, homepage

urlpatterns = [
    path('', homepage, name='homepage'),
    path('add_shift/', add_shift, name='add_shift'),
    path('transactionresult/', transactionresult, name='transactionresult'),
    path('shiftresult/', shiftresult, name='transactionresult'),
    path('add_transaction/', add_transaction, name='result'),
]
