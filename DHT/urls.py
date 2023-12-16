from django.urls import path
from . import views,api
urlpatterns=[
        path('test/',views.test),
        path("api/",api.dhtser,name='json'),
        path('data/',views.dht_tab,name='Data'),
        path ('chart-data/',views.chart_data, name='chart-data'),
        path('chart-data-jour/',views.chart_data_jour,name='chart-data-jour'),
        path('chart-data-semaine/',views.chart_data_semaine,name='chart-datasemaine'),
        path('chart-data-mois/',views.chart_data_mois,name='chart-data-mois'),
        path('download_csv/', views.download_csv, name='download_csv'),
        path('index/',views.index_view,name='index'),
        path('table/',views.table,name='table'),
        path('myChart/',views.graphique,name='myChart'),
        path('recieve/',views.receive_data,name='recieve'),

]