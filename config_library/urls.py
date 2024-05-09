from django.contrib import admin

from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'config_library'

urlpatterns = [
    path('', views.index, name='index'),
    path('library', views.library, name='library'),
    path('reader/cached_data_reader/', views.CachedDataReaderView.as_view(), name='cached_data_reader'),
    path('readers/database_reader/', views.DatabaseReaderView.as_view(), name='database_reader'),
    path('readers/logfile_reader/', views.LogFileReaderView.as_view(), name='logfile_reader'),
    path('readers/modbus_reader/', views.ModbusReaderView.as_view(), name='modbus_reader'),
    path('readers/mqtt_reader/', views.MqttReaderView.as_view(), name='mqtt_reader'),
    path('readers/polled_serial_reader/', views.PolledSerialReaderView.as_view(), name='polled_serial_reader'),
    path('readers/redis_reader/', views.RedisReaderView.as_view(), name='redis_reader'),
    path('readers/serial_reader/', views.SerialReaderView.as_view(), name='serial_reader'),
    path('readers/tcp_reader/', views.TcpReaderView.as_view(), name='tcp_reader'),
    path('readers/text_file_reader/', views.TextFileReaderView.as_view(), name='text_file_reader'),
    path('readers/timeout_reader/', views.TimeoutReaderView.as_view(), name='timeout_reader'),
    path('readers/udp_reader/', views.UdpReaderView.as_view(), name='udp_reader'),
    path('readers/websockets_reader/', views.WebsocketReaderView.as_view(), name='websockets_reader'),
    ]