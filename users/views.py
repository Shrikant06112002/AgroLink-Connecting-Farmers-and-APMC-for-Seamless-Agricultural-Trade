import json
from pyexpat.errors import messages
from django.shortcuts import render,redirect
from django.views import View
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . import models
from django.conf import settings
from django.core.mail import send_mail
from users.models import Table
import urllib.request




# Create your views here.
class Home(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

class Contact(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'contactus.html')

class Signin(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'SignIn.html')

    def post(self, request, *args, **kwargs):
        username = request.POST['email']   
        password = request.POST['password']


        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse('users:index'))
            else:
                print('TEST')
                messages.info(request, 'Inactive user')
                return redirect(reverse('users:contact'))
        return render(request, 'signus.html')

class Signus(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'SignUS.html')

    def post(self, request, *args, **kwargs):
        name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        print(name,email,password)

        user = User.objects.create(username=name,email=email,password=password)
        user.save()
        return redirect(reverse('users:index'))

class Slot(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'slot.html')

    def post(self,request,*args,**kwargs):
        email = request.POST['email']
        cname = request.POST['cname']
        stype = request.POST['stype']
        qdrop = request.POST['qdrop']
        quantity = request.POST['quantity']
        date = request.POST['date']
        time = request.POST['time']
        price = request.POST['price']

        print(time,date)

        models.Table.objects.create(email=email, price=price, crop_name=cname,seed_type=stype,quality=qdrop,quantity=quantity,date=date, time=time)
        return redirect(reverse('users:index'))
        

class BrokerSignin(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'brokersignin.html')

    def post(self, request, *args, **kwargs):
        username = request.POST['email']   
        password = request.POST['password']


        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active and user.is_staff:
                login(request, user)
                return redirect(reverse('users:table'))
            else:
                print('TEST')
                messages.info(request, 'Inactive user')
                return redirect(reverse('users:contact'))
        return render(request, 'index.html')

class Slottable(View):
    def get(self, request, *args, **kwargs):
        slots = Table.objects.filter()
        return render(request, 'table.html', {"slots":slots})

    def post(self, request, *args, **kwargs):
        required = request.POST['submit']
        table = Table.objects.filter(pk=required)
        subject = 'welcome to GFG world'
        message = f'Dear Farmer,\n Slot confirmed with the APMC on day = {table[0].date} at time = {table[0].time}.\nPlease find the details below : \nCrop = {table[0].crop_name},Quantity={table[0].quantity}.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [table[0].email, ]
        send_mail( subject, message, email_from, recipient_list )

        return render(request, 'index.html')

class Dailyrate(View):
    def get(self, request, *args, **kwargs):

        request_url = urllib.request.urlopen('https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit=10&filters%5Bstate%5D=Maharashtra')
        data = request_url.read()
        JSON_object = json.loads(data.decode('utf-8'))
        return render(request, 'dailyRates.html', {'slots':JSON_object['records'][1::]})