from django import forms
from .forms import BaseRVDASConfigForm

class CachedDataReaderForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label='class', initial='CachedDataReader', disabled=True)
    
    #kwargs
    data_server = forms.CharField(label='data_server', initial='localhost:8766')
    use_wss = forms.BooleanField(label='use_wss', initial=False, required=False)
    check_cert=forms.BooleanField(label='check_cert', initial=False, required=False)  
    # Serializer is a dict formset
    #Subscription_fields

class SubscriptionFields(forms.Form):
    field = forms.CharField(label='field', required=False)
    seconds = forms.IntegerField(label='seconds', initial=0, required=False)
    pass

#
#
# KWARG FORMS
#
#
class DatabaseReaderForm(BaseRVDASConfigForm):    
    object_class = forms.CharField(label='class', initial='DatabaseReader', disabled=True)
    
    #kwargs
    #kwargs
    database = forms.CharField(initial='DEFAULT_DATABASE')
    host = forms.CharField(initial='DEFAULT_DATABASE_HOST')
    user = forms.CharField(initial='DEFAULT_DATABASE_USER')
    password = forms.CharField(initial='DEFAULT_DATABASE_PASSWORD')
    tail = forms.BooleanField(initial=False, required=False)
    sleep_interval = forms.FloatField(initial=1.0)


class LogFileReaderForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label='class', initial='LogFileReader', disabled=True)
    
    #kwargs
    filebase = forms.CharField(required=False)
    tail = forms.BooleanField(required=False, initial=False)
    refresh_file_spec = forms.BooleanField(required=False, initial=False)
    retry_interval = forms.FloatField(required=False, initial=0.1)
    interval = forms.FloatField(required=False, initial=0)
    use_timestamps = forms.BooleanField(required=False, initial=False)
    record_format = forms.CharField(required=False)
    time_format = forms.CharField(required=False, initial='timestamp.TIME_FORMAT')
    date_format = forms.CharField(required=False, initial='timestamp.DATE_FORMAT')
    eol = forms.CharField(required=False)
    quiet = forms.BooleanField(required=False, initial=False)

class ModbusReaderForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label='class', initial='ModbusReader', disabled=True)
    
    #kwargs
    registers = forms.CharField()
    host = forms.CharField(initial='localhost')
    port = forms.IntegerField(initial=502)
    interval = forms.IntegerField(initial=10)
    sep = forms.CharField(initial=' ')
    encoding = forms.CharField(initial='utf-8')
    encoding_errors = forms.CharField(initial='ignore')

class MqttReaderForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label='class', initial='MqttReader', disabled=True)
    
    #kwargs
    broker = forms.CharField()
    channel = forms.CharField()
    client_name = forms.CharField()

#Complex handling.
class PolledSerialReaderForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label='class', initial='PolledSerialReader', disabled=True)
    
    #kwargs
    port = forms.CharField()
    baudrate = forms.IntegerField(initial=9600)
    bytesize = forms.IntegerField(initial=8)
    parity = forms.CharField(initial='N')
    stopbits = forms.IntegerField(initial=1)
    timeout = forms.FloatField(required=False)
    xonxoff = forms.BooleanField(required=False, initial=False)
    rtscts = forms.BooleanField(required=False, initial=False)
    write_timeout = forms.FloatField(required=False)
    dsrdtr = forms.BooleanField(required=False, initial=False)
    inter_byte_timeout = forms.FloatField(required=False)
    exclusive = forms.BooleanField(required=False)
    max_bytes = forms.IntegerField(required=False)
    eol = forms.CharField(required=False)
    encoding = forms.CharField(initial='utf-8')
    encoding_errors = forms.CharField(initial='ignore')
    #can be lists of strings - need to get example of this
    start_cmd = forms.CharField(required=False)
    pre_read_cmd = forms.CharField(required=False)
    stop_cmd = forms.CharField(required=False)

#As evertthing is a subclass, I'm not sure about needing this form. 
# class ReaderForm(BaseRVDASConfigForm):
    # pass

class RedisReaderForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label='class', initial='RedisReader', disabled=True)
    
    #kwargs
    channel = forms.CharField()
    password = forms.CharField(required=False)

class SerialReaderForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label='class', initial='SerialReader', disabled=True)
    
    #kwargs
    port = forms.CharField(initial=9876)
    baudrate = forms.IntegerField(initial=9600)
    bytesize = forms.IntegerField(initial=8)
    parity = forms.CharField(initial='N')
    stopbits = forms.IntegerField(initial=1)
    timeout = forms.FloatField(required=False)
    xonxoff = forms.BooleanField(required=False, initial=False)
    rtscts = forms.BooleanField(required=False, initial=False)
    write_timeout = forms.FloatField(required=False)
    dsrdtr = forms.BooleanField(required=False, initial=False)
    inter_byte_timeout = forms.FloatField(required=False)
    exclusive = forms.BooleanField(required=False)
    max_bytes = forms.IntegerField(required=False)
    eol = forms.CharField(required=False)
    encoding = forms.CharField(initial='utf-8')
    encoding_errors = forms.CharField(initial='ignore')

class TcpReaderForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label='class', initial='TcpReader', disabled=True)
    
    #kwargs
    interface = forms.CharField(required=False)
    port = forms.IntegerField(required=False)
    eol = forms.CharField(required=False)
    reuseaddr = forms.BooleanField(required=False, initial=True)
    reuseport = forms.BooleanField(required=False, initial=False)
    encoding = forms.CharField(initial='utf-8')
    encoding_errors = forms.CharField(initial='ignore')

class TextFileReaderForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label='class', initial='TextFileReader', disabled=True)
    
    #kwargs
    file_spec = forms.CharField(required=False)
    tail = forms.BooleanField(required=False, initial=False)
    refresh_file_spec = forms.BooleanField(required=False, initial=False)
    retry_interval = forms.FloatField(required=False, initial=0.1)
    interval = forms.FloatField(required=False, initial=0)
    eol = forms.CharField(required=False)

class TimeoutReaderForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label='class', initial='TimeoutReader', disabled=True)
    
    #kwargs
    reader = forms.CharField()
    timeout = forms.FloatField()
    message = forms.CharField(required=False)

class UdpReaderForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label='class', initial='UdpReader', disabled=True)
    
    #kwargs
    interface = forms.CharField(required=False)
    port = forms.IntegerField(required=False)
    mc_group = forms.CharField(required=False)
    reuseaddr = forms.BooleanField(required=False, initial=False)
    reuseport = forms.BooleanField(required=False, initial=False)
    encoding = forms.CharField(initial='utf-8')
    encoding_errors = forms.CharField(initial='ignore')
    this_is_a_test = forms.BooleanField(required=False)

class WebsocketReaderForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label='class', initial='WebsocketReader', disabled=True)
    
    #kwargs
    uri = forms.CharField(required=False)
    check_cert = forms.BooleanField(required=False, initial=False)
    


