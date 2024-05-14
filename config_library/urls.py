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
    # Transforms
    path('transforms/delta_transform/', views.DeltaTransformView.as_view() , name='delta_transform'),
    path('transforms/extract_field_transform/', views.ExtractFieldTransformView.as_view() , name='extract_field_transform'),
    path('transforms/format_transform/', views.FormatTransformView.as_view() , name='format_transform'),
    path('transforms/from_json_transform/', views.FromJsonTransformView.as_view() , name='from_json_transform'),
    path('transforms/geofence_transform/', views.GeofenceTransformView.as_view() , name='geofence_transform'),
    path('transforms/parse_nmea_transform/', views.ParseNmeaTransformView.as_view() , name='parse_nmea_transform'),
    path('transforms/parse_transform/', views.ParseTransformView.as_view() , name='parse_transform'),
    path('transforms/prefix_transform/', views.PrefixTransformView.as_view() , name='prefix_transform'),
    path('transforms/qc_filter_transform/', views.QcFilterTransformView.as_view() , name='qc_filter_transform'),
    path('transforms/regex_filter_transform/', views.RegexFilterTransformView.as_view() , name='regex_filter_transform'),
    path('transforms/regex_replace_transform/', views.RegexReplaceTransformView.as_view() , name='regex_replace_transform'),
    path('transforms/slice_transform/', views.SliceTransformView.as_view() , name='slice_transform'),
    path('transforms/split_transform/', views.SplitTransformView.as_view() , name='split_transform'),
    path('transforms/strip_transform/', views.StripTransformView.as_view() , name='strip_transform'),
    path('transforms/timestamp_transform/', views.TimestampTransformView.as_view() , name='timestamp_transform'),
    path('transforms/to_das_record_transform/', views.ToDasRecordTransformView.as_view() , name='to_das_record_transform'),
    path('transforms/to_json_transform/', views.ToJsonTransformView.as_view() , name='to_json_transform'),
    path('transforms/value_filter_transform/', views.ValueFilterTransformView.as_view() , name='value_filter_transform'),
    path('transforms/xml_aggregator_transform/', views.XmlAggregatorTransformView.as_view() , name='xml_aggregator_transform'),



    ]
