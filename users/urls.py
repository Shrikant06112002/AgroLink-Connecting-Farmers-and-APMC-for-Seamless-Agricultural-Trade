from django.urls import path
from django.conf import settings
from . import views
from users.views import Home, Contact, Signin, Signus, Slot, BrokerSignin,Slottable,Dailyrate

app_name = "users"

urlpatterns = [
    path('', Home.as_view(), name = "index"),
    path('contact', Contact.as_view(), name='contact'),
    path('signin', Signin.as_view(), name='signin' ),
    path('signup', Signus.as_view(), name='signus'),
    path('slot', Slot.as_view(), name='slot'),
    path('broker-signin', BrokerSignin.as_view(), name='agent'),
    path('table',Slottable.as_view(), name='table'),
    path('dailyrate', Dailyrate.as_view(), name='daily')
]