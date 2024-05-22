from django import forms
from .forms import BaseRVDASConfigForm
from logger.utils import timestamp  # noqa: E402
import logging
from logger.utils.timestamp import time_str, DATE_FORMAT
from datetime import datetime, timedelta, timezone

# Complex forms that need formsets or special views.

# composed_writer
#
# Complex form
# class LoggerManagerWriterForm(BaseRVDASConfigForm):
# object_class = forms.CharField(label='class', initial='LoggerManagerWriter', disabled=True)
# database=None
# api=None
# allowed_prefixes=[]


class CachedDataWriterForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="CachedDataWriter", disabled=True)
    data_server = forms.CharField(max_length=255)
    start_server = forms.BooleanField(required=False, initial=False)
    back_seconds = forms.IntegerField(initial=480)
    cleanup_interval = forms.IntegerField(initial=6)
    update_interval = forms.IntegerField(initial=1)
    max_backup = forms.IntegerField(initial=60 * 60 * 24)
    use_wss = forms.BooleanField(required=False, initial=False)
    check_cert = forms.BooleanField(required=False, initial=False)


class DatabaseWriterForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="DatabaseWriter", disabled=True)
    database = forms.CharField(max_length=255, initial="DEFAULT_DATABASE")
    host = forms.CharField(max_length=255, initial="DEFAULT_DATABASE_HOST")
    user = forms.CharField(max_length=255, initial="DEFAULT_DATABASE_USER")
    password = forms.CharField(widget=forms.PasswordInput, initial="DEFAULT_DATABASE_PASSWORD")
    save_source = forms.BooleanField(required=False, initial=True)


class EmailWriterForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="EmailWriter", disabled=True)
    to = forms.EmailField()
    sender = forms.EmailField(required=False)
    subject = forms.CharField(max_length=255, required=False)
    max_freq = forms.IntegerField(initial=3 * 60)


class FileWriterForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="FileWriter", disabled=True)
    filename = forms.CharField(max_length=255, required=False)
    mode = forms.CharField(max_length=2, initial="a")
    delimiter = forms.CharField(max_length=10, initial="\n")
    flush = forms.BooleanField(required=False, initial=True)
    split_by_time = forms.BooleanField(required=False, initial=False)
    split_interval = forms.IntegerField(required=False)
    header = forms.CharField(max_length=255, required=False)
    header_file = forms.CharField(max_length=255, required=False)
    time_format = forms.CharField(max_length=255, initial="-" + DATE_FORMAT)
    time_zone = forms.CharField(max_length=255, initial=str(timezone.utc))
    create_path = forms.BooleanField(required=False, initial=True)
    encoding = forms.CharField(max_length=255, initial="utf-8")
    encoding_errors = forms.CharField(max_length=255, initial="ignore")


class InfluxDBWriterForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="InfluxDBWriter", disabled=True)
    bucket_name = forms.CharField(max_length=255, initial="INFLUXDB_BUCKET")
    measurement_name = forms.CharField(max_length=255, required=False)
    auth_token = forms.CharField(max_length=255, initial="INFLUXDB_AUTH_TOKEN")
    org = forms.CharField(max_length=255, initial="INFLUXDB_ORG")
    url = forms.URLField(initial="INFLUXDB_URL")
    verify_ssl = forms.BooleanField(initial="INFLUXDB_VERIFY_SS")


class LogfileWriterForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="LogfileWriter", disabled=True)
    filebase = forms.CharField(max_length=255, required=False)
    flush = forms.BooleanField(required=False, initial=True)
    time_format = forms.CharField(max_length=255, initial=timestamp.TIME_FORMAT)
    date_format = forms.CharField(max_length=255, initial=timestamp.DATE_FORMAT)
    split_char = forms.CharField(max_length=10, initial=" ")
    suffix = forms.CharField(max_length=255, required=False, initial="")
    header = forms.CharField(max_length=255, required=False)
    header_file = forms.CharField(max_length=255, required=False)
    rollover_hourly = forms.BooleanField(required=False, initial=False)
    quiet = forms.BooleanField(required=False, initial=False)


class MQTTWriterForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="MQTTWriter", disabled=True)
    broker = forms.CharField(max_length=255)
    channel = forms.CharField(max_length=255)
    client_name = forms.CharField(max_length=255)


class NetworkWriterForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="NetworkWriter", disabled=True)
    network = forms.CharField(max_length=255)
    num_retry = forms.IntegerField(initial=2)
    eol = forms.CharField(max_length=10, initial="")
    encoding = forms.CharField(max_length=255, initial="utf-8")
    encoding_errors = forms.CharField(max_length=255, initial="ignore")


class RedisWriterForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="RedisWriter", disabled=True)
    channel = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, required=False)


class RegexLogfileWriterForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="RegexLogfileWriter", disabled=True)
    filebase = forms.CharField(max_length=255, required=False)
    flush = forms.BooleanField(required=False, initial=True)
    time_format = forms.CharField(max_length=255, initial=timestamp.TIME_FORMAT)
    date_format = forms.CharField(max_length=255, initial=timestamp.DATE_FORMAT)
    split_char = forms.CharField(max_length=10, initial=" ")
    suffix = forms.CharField(max_length=255, required=False, initial="")
    header = forms.CharField(max_length=255, required=False)
    header_file = forms.CharField(max_length=255, required=False)
    rollover_hourly = forms.BooleanField(required=False, initial=False)
    quiet = forms.BooleanField(required=False, initial=False)


class SerialWriterForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="SerialWriter", disabled=True)
    port = forms.CharField(max_length=255)
    baudrate = forms.IntegerField(initial=9600)
    bytesize = forms.IntegerField(initial=8)
    parity = forms.ChoiceField(choices=[("N", "None"), ("E", "Even"), ("O", "Odd"), ("M", "Mark"), ("S", "Space")], initial="N")
    stopbits = forms.FloatField(initial=1)
    timeout = forms.FloatField(required=False)
    xonxoff = forms.BooleanField(required=False, initial=False)
    rtscts = forms.BooleanField(required=False, initial=False)
    write_timeout = forms.FloatField(required=False)
    dsrdtr = forms.BooleanField(required=False, initial=False)
    inter_byte_timeout = forms.FloatField(required=False)
    exclusive = forms.BooleanField(required=False)
    eol = forms.CharField(max_length=10, initial="\n")
    encoding = forms.CharField(max_length=255, initial="utf-8")
    encoding_errors = forms.CharField(max_length=255, initial="ignore")
    quiet = forms.BooleanField(required=False, initial=False)


class TCPWriterForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="TCPWriter", disabled=True)
    destination = forms.CharField(max_length=255)
    port = forms.IntegerField()
    num_retry = forms.IntegerField(initial=2)
    warning_limit = forms.IntegerField(initial=5)
    eol = forms.CharField(max_length=10, initial="")
    reuseaddr = forms.BooleanField(initial=False)
    reuseport = forms.BooleanField(initial=False)
    encoding = forms.CharField(max_length=255, initial="utf-8")
    encoding_errors = forms.CharField(max_length=255, initial="ignore")


class TextFileWriterForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="TextFileWriter", disabled=True)
    filename = forms.CharField(max_length=255, required=False)
    flush = forms.BooleanField(required=False, initial=True)
    truncate = forms.BooleanField(required=False, initial=False)
    split_by_date = forms.BooleanField(required=False, initial=False)
    create_path = forms.BooleanField(required=False, initial=True)
    header = forms.CharField(max_length=255, required=False)
    header_file = forms.CharField(max_length=255, required=False)


class TimeoutWriterForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="TimeoutWriter", disabled=True)
    writer = forms.CharField(max_length=255)
    timeout = forms.FloatField()
    message = forms.CharField(max_length=255, required=False)
    resume_message = forms.CharField(max_length=255, required=False)
    empty_is_okay = forms.BooleanField(required=False, initial=False)
    none_is_okay = forms.BooleanField(required=False, initial=False)


class UDPWriterForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="UDPWriter", disabled=True)
    destination = forms.CharField(max_length=255, required=False)
    port = forms.IntegerField(required=False)
    mc_interface = forms.CharField(max_length=255, required=False)
    mc_ttl = forms.IntegerField(initial=3)
    num_retry = forms.IntegerField(initial=2)
    warning_limit = forms.IntegerField(initial=5)
    eol = forms.CharField(max_length=10, initial="")
    reuseaddr = forms.BooleanField(initial=False)
    reuseport = forms.BooleanField(initial=False)
    encoding = forms.CharField(max_length=255, initial="utf-8")
    encoding_errors = forms.CharField(max_length=255, initial="ignore")


class WebsocketWriterForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="WebsocketWriter", disabled=True)
    uri = forms.URLField()
    cert_file = forms.CharField(max_length=255, required=False)
    key_file = forms.CharField(max_length=255, required=False)
