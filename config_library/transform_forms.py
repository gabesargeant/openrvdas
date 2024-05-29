from django import forms
from logger.utils import nmea_parser
from logger.utils import record_parser  # noqa: E402
from logger.utils import timestamp  # noqa: E402
import logging
from .forms import BaseRVDASConfigForm

# These forms represent configurable transforms.
# there's also a set of transforms that are just fixed.

# Fixed transforms
# class CountTransform
# class UniqueTransformForm(BaseRVDASConfigForm):
# class MaxMinTransformForm(forms.Form):
# class CountTransformForm(forms.Form):


# complex transform that require more than just

# class InterpolationTransformForm(forms.Form):
#     field_spec, dict of kv like cached data reader
#     interval,
#     window=0,
#     metadata_interval=None


class InterpolationTransformForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="InterpolationTransform", disabled=True)

    # KWARGS
    interval = forms.CharField(label="Interval")
    window = forms.IntegerField(initial=0, label="Window")
    metadata_interval = forms.CharField(required=False, label="Metadata Interval")


class InterpolationFieldSpecForm(forms.Form):
    interpolated_field = forms.CharField(label="Interpolated field name")
    source = forms.CharField(label="Source")
    # Algorithm
    type = forms.CharField(label="Algorithm Type")
    window = forms.IntegerField(label="Window")


# class NMEAChecksumTransformForm(forms.Form):
#     checksum_optional=False,
#     error_message='Bad checksum for record: ',
#     writer=None
#     pass

# class NMEATransformForm(forms.form):
# very complex and dynamic.

#
# class SelectFieldsTransformForm(forms.Form):
# keep=None, # or a list
# delete=None # or a list

#
# class DerivedDataTransformForm(forms.Form):
#     pass

# class SubsampleTransformForm(forms.Form):
#     field_spec,
#     back_seconds=60*60,
#     metadata_interval=None


# class TrueWindsTransformForm(forms.Form):
#    course_field, speed_field, heading_field,
#                  wind_dir_field, wind_speed_field,
#                  true_dir_name,
#                  true_speed_name,
#                  apparent_dir_name,
#                  update_on_fields=[],
#                  max_field_age={},
#                  zero_line_reference=0,
#                  convert_wind_factor=1,
#                  convert_speed_factor=1,
#                  data_id=None,
#                  metadata_interval=None


#
#
# SIMPLE FORMS THAT HAVE NO DATA.
# These could potentially be replaced with fixture data.
# These forms will get created once.


class CountTransformForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="CountTransform", disabled=True)


class MaxMinTransformForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="MaxMinTransform", disabled=True)


class UniqueTransformForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="UniqueTransform", disabled=True)


#
#
# KWARG FORMS
#
#
class DeltaTransformForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="DeltaTransform", disabled=True)

    # kwargs
    rate = forms.BooleanField(initial=False, required=False, label="Rate")
    field_type = forms.CharField(required=False, label="Field Type")


class ExtractFieldTransformForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="ExtractFieldTransform", disabled=True)

    # kwargs
    field_name = forms.CharField(label="Field Name", initial="")


class FormatTransformForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="FormatTransform", disabled=True)

    # kwargs
    format_str = forms.CharField(label="Format String")
    defaults = forms.CharField(required=False, label="Defaults")


class FromJsonTransformForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="FromJsonTransform", disabled=True)

    # kwargs
    das_record = forms.BooleanField(initial=False, required=False, label="DAS Record")


class GeofenceTransformForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="GeofenceTransform", disabled=True)

    # kwargs
    latitude_field_name = forms.CharField(label="Latitude Field Name")
    longitude_field_name = forms.CharField(label="Longitude Field Name")
    boundary_file_name = forms.CharField(required=False, label="Boundary File Name")
    boundary_dir_name = forms.CharField(required=False, label="Boundary Directory Name")
    distance_from_boundary_in_degrees = forms.FloatField(initial=0, label="Distance from Boundary (in degrees)")
    leaving_boundary_message = forms.CharField(required=False, label="Leaving Boundary Message")
    entering_boundary_message = forms.CharField(required=False, label="Entering Boundary Message")
    seconds_between_checks = forms.IntegerField(initial=0, label="Seconds Between Checks")


class ParseNmeaTransformForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="ParseNmeaTransform", disabled=True)

    # kwargs
    json = forms.BooleanField(initial=False, required=False, label="JSON")
    message_path = forms.CharField(initial=nmea_parser.DEFAULT_MESSAGE_PATH, label="Message Path")
    sensor_path = forms.CharField(initial=nmea_parser.DEFAULT_SENSOR_PATH, label="Sensor Path")
    sensor_model_path = forms.CharField(initial=nmea_parser.DEFAULT_SENSOR_MODEL_PATH, label="Sensor Model Path")
    time_format = forms.CharField(required=False, label="Time Format")


class ParseTransformForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="ParseTransform", disabled=True)

    # kwargs
    record_format = forms.CharField(required=False, label="Record Format")
    field_patterns = forms.CharField(required=False, label="Field Patterns")
    metadata = forms.CharField(required=False, label="Metadata")
    definition_path = forms.CharField(initial=record_parser.DEFAULT_DEFINITION_PATH, label="Definition Path")
    return_json = forms.BooleanField(initial=False, required=False, label="Return JSON")
    return_das_record = forms.BooleanField(initial=False, required=False, label="Return DAS Record")
    metadata_interval = forms.CharField(required=False, label="Metadata Interval")
    strip_unprintable = forms.BooleanField(initial=False, required=False, label="Strip Unprintable")
    quiet = forms.BooleanField(initial=False, required=False, label="Quiet")
    prepend_data_id = forms.BooleanField(initial=False, required=False, label="Prepend Data ID")
    delimiter = forms.CharField(initial=":", label="Delimiter")


class PrefixTransformForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="PrefixTransform", disabled=True)

    # kwargs
    prefix = forms.CharField(required=False, label="Prefix")
    sep = forms.CharField(initial="", label="Separator", required=False)
    quiet = forms.BooleanField(required=False, initial=False, label="Quiet")


class QcFilterTransformForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="QcFilterTransform", disabled=True)

    # kwargs
    bounds = forms.CharField(label="Bounds")
    message = forms.CharField(required=False, label="Message")


class RegexFilterTransformForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="RegexFilterTransform", disabled=True)

    # kwargs
    pattern = forms.CharField(label="Pattern (Regex)")
    flags = forms.IntegerField(initial=0, label="Flags")
    negate = forms.BooleanField(initial=False, required=False, label="Negate")


class RegexReplaceTransformForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="RegexReplaceTransform", disabled=True)

    # kwargs
    patterns = forms.CharField(label="Patterns (Regex)")
    count = forms.IntegerField(initial=0, label="Count")
    flags = forms.IntegerField(initial=0, label="Flags")


class SliceTransformForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="SliceTransform", disabled=True)

    # kwargs
    fields = forms.CharField(required=False, label="Fields")
    sep = forms.CharField(required=False, label="Separator")


class SplitTransformForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="SplitTransform", disabled=True)

    # kwargs
    sep = forms.CharField(initial="\n", label="Separator")


class StripTransformForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="StripTransform", disabled=True)

    # kwargs
    chars = forms.CharField(required=False, label="Characters")
    unprintable = forms.BooleanField(required=False, initial=False, label="Unprintable")
    strip_prefix = forms.BooleanField(required=False, initial=False, label="Strip Prefix")
    strip_suffix = forms.BooleanField(required=False, initial=False, label="Strip Suffix")


class TimestampTransformForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="TimestampTransform", disabled=True)

    # kwargs
    time_format = forms.CharField(initial=timestamp.TIME_FORMAT, label="Time Format")
    time_zone = forms.CharField(initial=timestamp.timezone.utc, label="Time Zone")
    sep = forms.CharField(initial=" ", label="Separator", required=False)


class ToDasRecordTransformForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="ToDasRecordTransform", disabled=True)

    # kwargs
    data_id = forms.CharField(required=False, label="Data ID")
    field_name = forms.CharField(required=False, label="Field Name")


class ToJsonTransformForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="ToJsonTransform", disabled=True)

    # kwargs
    input_format = forms.ChoiceField(choices=[("formats.Python_Record", "Python Record"), ("formats.Text", "Text")], label="Input Format")
    output_format = forms.ChoiceField(choices=[("formats.Python_Record", "Python Record"), ("formats.Text", "Text")], label="Output Format")


class ValueFilterTransformForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="ValueFilterTransform", disabled=True)

    # kwargs
    bounds = forms.CharField(required=False, label="Bounds")
    log_level = forms.ChoiceField(
        choices=[(logging.DEBUG, "DEBUG"), (logging.INFO, "INFO"), (logging.WARNING, "WARNING"), (logging.ERROR, "ERROR"), (logging.CRITICAL, "CRITICAL")],
        label="Log Level",
        initial=logging.INFO,
    )


class XmlAggregatorTransformForm(BaseRVDASConfigForm):
    object_class = forms.CharField(label="class", initial="XmlAggregatorTransform", disabled=True)

    # kwargs
    tag = forms.CharField(max_length=100, label="XML Tag")
