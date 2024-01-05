from django.shortcuts import render
import csv
import datetime
from django.http import JsonResponse
import telepot
from .models import Dht11
from django.shortcuts import render
import csv
from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.utils import timezone

from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.

def test(request):
    return HttpResponse('Iot Project')


def dht_tab(request):
    tab = Dht11.objects.all()
    s = {'tab': tab}
    return render(request, 'table.html', s)


def table(request):
    derniere_ligne = Dht11.objects.last()
    derniere_date = Dht11.objects.last().dt
    delta_temps = timezone.now() - derniere_date
    difference_minutes = delta_temps.seconds // 60
    temps_ecoule = ' il y a ' + str(difference_minutes) + ' min'
    if difference_minutes > 60:
        temps_ecoule = 'il y ' + str(difference_minutes // 60) + 'h' + str(difference_minutes % 60) + 'min'
    valeurs = {'date': temps_ecoule, 'id': derniere_ligne.id, 'temp':derniere_ligne.temp, 'hum': derniere_ligne.hum}
    return render(request, 'value.html', {'valeurs': valeurs})


def download_csv(request):
    model_values = Dht11.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dht.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'temp', 'hum', 'dt'])
    liste = model_values.values_list('id', 'temp', 'hum', 'dt')
    for row in liste:
        writer.writerow(row)
    return response


# pour afficher navbar de template
def index_view(request):
    return render(request, 'index.html')


# pour afficher les graphes
def graphique(request):
    return render(request, 'Chart.html')


# récupérer toutes les valeur de température et humidity sous forme un
# fichier json
def chart_data(request):
    dht = Dht11.objects.all()

    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)


# pour récupérer les valeurs de température et humidité de dernier 24h
# et envoie sous forme JSON

def chart_data_jour(request):
    dht = Dht11.objects.all()
    now = timezone.now()
    last_24_hours = now - timezone.timedelta(hours=24)
    # Récupérer tous les objets de Module créés au cours des 24 dernières heures
    dht = Dht11.objects.filter(dt__range=(last_24_hours, now))
    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)


# pour récupérer les valeurs de température et humidité de dernier semaine
# et envoie sous forme JSON
def chart_data_semaine(request):
    dht = Dht11.objects.all()
    # calcul de la date de début de la semaine dernière
    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=7)
    print(datetime.timedelta(days=7))
    print(date_debut_semaine)
    # filtrer les enregistrements créés depuis le début de la semainedernière
    dht = Dht11.objects.filter(dt__gte=date_debut_semaine)
    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)


# pour récupérer les valeurs de température et humidité de dernier moins
# et envoie sous forme JSON
def chart_data_mois(request):
    dht = Dht11.objects.all()
    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=30)
    print(datetime.timedelta(days=30))
    print(date_debut_semaine)
    # filtrer les enregistrements créés depuis le début de la semaine dernière
    dht = Dht11.objects.filter(dt__gte=date_debut_semaine)
    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)


def sendtele(request, message):
    token = '6317292446:AAH_syCW5E9ZwMEg6ZevKSvvda0L9OM-3LY'
    rece_id = '6644914334'
    bot = telepot.Bot(token)
    bot.sendMessage(rece_id, message)
    print(bot.sendMessage(rece_id, 'OK.'))



@csrf_exempt
def receive_data(request):
    print(request)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("data :", data)
            temperature = data['temp']
            humidity = data['hum']
            Dht11.objects.create(temp=temperature, hum=humidity)
            testCapteur(request, humidity, temperature)

            print('success')
            return JsonResponse({'status': 'success'})
        except Exception as e:
            print('error 1')
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        print('error 2')
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'})


def testCapteur(request, hum, temp):
    if temp > 10:
        sendtele(request, 'alert Température')
        subject = 'Alerte'
        message = 'Il y a une alerte importante sur votre Capteur latempérature dépasse le seuil'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['hajar.eznati20@ump.ac.ma']
        send_mail(subject, message, email_from, recipient_list)
    if hum > 40:
        sendtele(request, 'alert Humidité')
        subject = 'Alerte'
        message = 'Il y a une alerte importante sur votre Capteur latempérature dépasse le seuil'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['hajar.eznati20@ump.ac.ma']
        send_mail(subject, message, email_from, recipient_list)