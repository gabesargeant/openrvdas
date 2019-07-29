#! /usr/bin/env python3

import logging
from collections import OrderedDict

VARS = {
  '%INTERFACE%': '157.132.133.102',
  '%RAW_UDP%': '6224',
  '%CACHE_UDP%': '6225',
  '%WEBSOCKET%': '8766',
  '%BACK_SECONDS%': '640'
}

LOGGERS = [
  'ladc',
  'lais',
  'ldfl',
  'lgar',
  'lguv',
  'lgyr',
  'lknu',
  'lmwx',
  'loxy',
  'lpco',
  'lrtm',
  'lsea',
  'lsep',
  'lsvp',
  'tsg2',
  'utsg',
  'true_wind'
  ]

#######################
# From tethys:/usr/local/packages/rvdas/config/port.tab
# instrument    serial port     baud  datab stopb parity igncr icrnl eol onlcr ocrnl icanon vmin vtime vintr vquit opost
# ----------    -----------     ----- ----- ----- ------ ----- ----- --- ----- ----- ------ ---- ----- ----- ----- -----
#SAMPLE         /dev/ttyy00     9600  8     1     0      1     0     0   1     0     1      1    0     0     0     0
MOXA = {
    # Moxa Box 10.1.1.50
    'lgar': 'Garmin_GPS  /dev/ttyr00  4800  8  1  0  1  1  0  1  0  1  1  0  0  0  0',
    #'': 'Trimble_GPS  /dev/ttyr01  4800  8  1  0  1  1  0  1  0  1  1  0  0  0  0',
    'lgyr': 'GYRO  /dev/ttyr02  4800  8  1  0  1  1  0  1  0  1  1  0  0  0  0',
    'tsg2': 'uTSG2  /dev/ttyr03  4800  8  1  0  1  1  0  1  0  1  1  0  0  0  0',
    #'': '#empty      /dev/ttyr04  4800  8  1  0  1  1  0  1  0  1  1  0  0  0  0',
    'lknu': 'Sonar_Depth  /dev/ttyr05  19200  8  1  0  1  1  0  1  0  1  1  0  0  0  0',
    'utsg': 'uTSG  /dev/ttyr06  4800  8  1  0  1  1  0  1  0  1  1  0  0  0  0',
    'lrtm': 'Remote_Temp  /dev/ttyr07  9600  8  1  0  1  1  0  1  0  1  1  0  0  0  0',
    'lsea': 'SeaWall  /dev/ttyr08  9600  8  1  0  1  1  0  1  0  1  1  0  0  0  0',
    'lpco': 'PCO2  /dev/ttyr09  9600  8  1  0  1  1  0  1  0  1  1  0  0  0  0',
    'loxy': 'OXYG  /dev/ttyr0a  9600  8  1  0  0  1  0  1  0  1  1  0  0  0  0',
    'ldfl': 'Digital_Flr  /dev/ttyr0b  19200  8  1  0  1  1  0  1  0  1  1  0  0  0  0',
    'lsep': 'SeaPath  /dev/ttyr0c  19200  8  1  0  1  1  0  1  0  1  1  0  0  0  0',
    'ladc': 'ADCP  /dev/ttyr0d  9600  8  1  0  1  1  0  1  0  1  1  0  0  0  0',
    'lsvp': 'SV_PROBE  /dev/ttyr0e  19200  8  1  0  1  1  0  1  0  1  1  0  0  0  0',
    'lguv': 'PUV_GUV  /dev/ttyr0f  9600  8  1  0  1  1  0  1  0  1  1  0  0  0  0',

    # Moxa Box 10.1.1.51
    #'': '#Winch  /dev/ttyr10  38400  8  1  0  1  1  0  1  0  1  1  0  0  0  0',
    #'': 'CTD  /dev/ttyr11  9600  8  1  0  1  1  0  1  0  1  1  0  0  0  0',
    #'': 'NetDepth  /dev/ttyr12  9600  7  1  0  1  1  0  1  0  1  1  0  0  0  0',
    #'': 'Oxygen  /dev/ttyr13  9600  8  1  0  1  1  0  1  0  1  1  0  0  0  0',
    'lais': 'AIS  /dev/ttyr14  38400  8  1  0  1  1  0  1  0  1  1  0  0  0  0',
    'lmwx': 'MastWx  /dev/ttyr15  9600  8  1  0  1  1  0  1  0  1  1  0  0  0  0',
    #'': 'Winch  /dev/ttyr16  38400  8  1  0  1  1  0  1  0  1  1  0  0  0  0'
}


HEADER_TEMPLATE = """##########
# Sample YAML cruise definition file for LMG1903, created by hacked-up
# script at local/LMG1903/create_MOXA_cruise_definition.py.

# Note that the one hack necessary is that YAML interprets 'off' (when not
# quoted) as the literal 'False'. So YAML needs to quote 'off'.

########################################
cruise:
  id: LMG1903
  start: '2014-03-26'
  end: '2019-04-09'
"""

TRUE_WIND_TEMPLATE = """
  true_wind->net:
    name: true_wind->net
    readers:
      class: UDPReader
      kwargs:
        port: %CACHE_UDP%
    transforms:
    - class: FromJSONTransform
    - class: ComposedDerivedDataTransform
      kwargs:
        transforms:
        - class: TrueWindsTransform
          kwargs:
            apparent_dir_name: PortApparentWindDir
            convert_speed_factor: 0.5144
            course_field: S330CourseTrue
            heading_field: S330HeadingTrue
            speed_field: S330SpeedKt
            true_dir_name: PortTrueWindDir
            true_speed_name: PortTrueWindSpeed
            update_on_fields:
            - MwxPortRelWindDir
            wind_dir_field: MwxPortRelWindDir
            wind_speed_field: MwxPortRelWindSpeed
        - class: TrueWindsTransform
          kwargs:
            apparent_dir_name: StbdApparentWindDir
            convert_speed_factor: 0.5144
            course_field: S330CourseTrue
            heading_field: S330HeadingTrue
            speed_field: S330SpeedKt
            true_dir_name: StbdTrueWindDir
            true_speed_name: StbdTrueWindSpeed
            update_on_fields:
            - MwxStbdRelWindDir
            wind_dir_field: MwxStbdRelWindDir
            wind_speed_field: MwxStbdRelWindSpeed
    writers:
    - class: UDPWriter          # Write back out to UDP
      kwargs:
        port: %CACHE_UDP%
        interface: %INTERFACE%
    stderr_writers:          # Turn stderr into DASRecord, broadcast to cache
    - class: ComposedWriter  # UDP port for CachedDataServer to pick up.
      kwargs:
        transforms:
        - class: ToDASRecordTransform
          kwargs:
            field_name: 'stderr:logger:true_wind'
        writers:
          class: UDPWriter
          kwargs:
            port: %CACHE_UDP%
            interface: %INTERFACE%

  true_wind->file/net:
    name: true_wind->file/net
    readers:
      class: UDPReader
      kwargs:
        port: %CACHE_UDP%
    transforms:
    - class: FromJSONTransform
    - class: ComposedDerivedDataTransform
      kwargs:
        transforms:
        - class: TrueWindsTransform
          kwargs:
            apparent_dir_name: PortApparentWindDir
            convert_speed_factor: 0.5144
            course_field: S330CourseTrue
            heading_field: S330HeadingTrue
            speed_field: S330SpeedKt
            true_dir_name: PortTrueWindDir
            true_speed_name: PortTrueWindSpeed
            update_on_fields:
            - MwxPortRelWindDir
            wind_dir_field: MwxPortRelWindDir
            wind_speed_field: MwxPortRelWindSpeed
        - class: TrueWindsTransform
          kwargs:
            apparent_dir_name: StbdApparentWindDir
            convert_speed_factor: 0.5144
            course_field: S330CourseTrue
            heading_field: S330HeadingTrue
            speed_field: S330SpeedKt
            true_dir_name: StbdTrueWindDir
            true_speed_name: StbdTrueWindSpeed
            update_on_fields:
            - MwxStbdRelWindDir
            wind_dir_field: MwxStbdRelWindDir
            wind_speed_field: MwxStbdRelWindSpeed
    writers:
    - class: UDPWriter          # Write back out to UDP
      kwargs:
        port: %CACHE_UDP%
        interface: %INTERFACE%
    stderr_writers:          # Turn stderr into DASRecord, broadcast to cache
    - class: ComposedWriter  # UDP port for CachedDataServer to pick up.
      kwargs:
        transforms:
        - class: ToDASRecordTransform
          kwargs:
            field_name: 'stderr:logger:true_wind'
        writers:
          class: UDPWriter
          kwargs:
            port: %CACHE_UDP%
            interface: %INTERFACE%

  true_wind->file/net/db:
    name: true_wind->file/net/db
    readers:
      class: UDPReader
      kwargs:
        port: %CACHE_UDP%
    transforms:
    - class: FromJSONTransform
    - class: ComposedDerivedDataTransform
      kwargs:
        transforms:
        - class: TrueWindsTransform
          kwargs:
            apparent_dir_name: PortApparentWindDir
            convert_speed_factor: 0.5144
            course_field: S330CourseTrue
            heading_field: S330HeadingTrue
            speed_field: S330SpeedKt
            true_dir_name: PortTrueWindDir
            true_speed_name: PortTrueWindSpeed
            update_on_fields:
            - MwxPortRelWindDir
            wind_dir_field: MwxPortRelWindDir
            wind_speed_field: MwxPortRelWindSpeed
        - class: TrueWindsTransform
          kwargs:
            apparent_dir_name: StbdApparentWindDir
            convert_speed_factor: 0.5144
            course_field: S330CourseTrue
            heading_field: S330HeadingTrue
            speed_field: S330SpeedKt
            true_dir_name: StbdTrueWindDir
            true_speed_name: StbdTrueWindSpeed
            update_on_fields:
            - MwxStbdRelWindDir
            wind_dir_field: MwxStbdRelWindDir
            wind_speed_field: MwxStbdRelWindSpeed
    writers:
    - class: UDPWriter          # Write back out to UDP
      kwargs:
        port: %CACHE_UDP%
        interface: %INTERFACE%
    stderr_writers:          # Turn stderr into DASRecord, broadcast to cache
    - class: ComposedWriter  # UDP port for CachedDataServer to pick up.
      kwargs:
        transforms:
        - class: ToDASRecordTransform
          kwargs:
            field_name: 'stderr:logger:true_wind'
        writers:
          class: UDPWriter
          kwargs:
            port: %CACHE_UDP%
            interface: %INTERFACE%
"""

OFF_TEMPLATE="""
  %LOGGER%->off:
    name: %LOGGER%->off
"""

NET_WRITER_TEMPLATE="""
  %LOGGER%->net:
    name: %LOGGER%->net
    readers:                    # Read from simulated serial port
      class: SerialReader
      kwargs:
        baudrate: %BAUD%
        port: %TTY%
    transforms:                 # Add timestamp and logger label
    - class: TimestampTransform
    - class: PrefixTransform
      kwargs:
        prefix: %LOGGER%
    writers:
    - class: UDPWriter      # Send raw NMEA to UDP
      kwargs:
        port: %RAW_UDP%
        interface: %INTERFACE%
    - class: ComposedWriter     # Also parse to fields and send to CACHE UDP
      kwargs:                   # port for CachedDataServer to pick up
        transforms:
        - class: ParseTransform
          kwargs:
            definition_path: local/devices/*.yaml,local/lmg/devices/*.yaml
        writers:
          class: UDPWriter
          kwargs:
            port: %CACHE_UDP%
            interface: %INTERFACE%
    stderr_writers:          # Turn stderr into DASRecord, broadcast to cache
    - class: ComposedWriter  # UDP port for CachedDataServer to pick up.
      kwargs:
        transforms:
        - class: ToDASRecordTransform
          kwargs:
            field_name: 'stderr:logger:%LOGGER%'
        writers:
          class: UDPWriter
          kwargs:
            port: %CACHE_UDP%
            interface: %INTERFACE%
"""

FILE_NET_WRITER_TEMPLATE="""
  %LOGGER%->file/net:
    name: %LOGGER%->file/net
    readers:                    # Read from simulated serial port
      class: SerialReader
      kwargs:
        baudrate: %BAUD%
        port: %TTY%
    transforms:                 # Add timestamp
    - class: TimestampTransform
    writers:
    - class: LogfileWriter      # Write to logfile
      kwargs:
        filebase: /var/tmp/log/LMG1903/%LOGGER%/raw/LMG1903_%LOGGER%
    - class: ComposedWriter     # Also prefix with logger name and broadcast
      kwargs:                   # raw NMEA on UDP
        transforms:
        - class: PrefixTransform
          kwargs:
            prefix: %LOGGER%
        writers:
        - class: UDPWriter      # Send raw NMEA to UDP
          kwargs:
            port: %RAW_UDP%
            interface: %INTERFACE%
    - class: ComposedWriter     # Also parse to fields and send to CACHE UDP
      kwargs:                   # port for CachedDataServer to pick up
        transforms:
        - class: PrefixTransform
          kwargs:
            prefix: %LOGGER%
        - class: ParseTransform
          kwargs:
            definition_path: local/devices/*.yaml,local/lmg/devices/*.yaml
        writers:
        - class: UDPWriter
          kwargs:
            port: %CACHE_UDP%
            interface: %INTERFACE%
    stderr_writers:          # Turn stderr into DASRecord, broadcast to cache
    - class: ComposedWriter  # UDP port for CachedDataServer to pick up.
      kwargs:
        transforms:
        - class: ToDASRecordTransform
          kwargs:
            field_name: 'stderr:logger:%LOGGER%'
        writers:
          class: UDPWriter
          kwargs:
            port: %CACHE_UDP%
            interface: %INTERFACE%
"""

FULL_WRITER_TEMPLATE="""
  %LOGGER%->file/net/db:
    name: %LOGGER%->file/net/db
    readers:                    # Read from simulated serial port
      class: SerialReader
      kwargs:
        baudrate: %BAUD%
        port: %TTY%
    transforms:                 # Add timestamp
    - class: TimestampTransform
    writers:
    - class: LogfileWriter      # Write to logfile
      kwargs:
        filebase: /var/tmp/log/LMG1903/%LOGGER%/raw/LMG1903_%LOGGER%
    - class: ComposedWriter     # Also prefix with logger name and broadcast
      kwargs:                   # raw NMEA on UDP
        transforms:
        - class: PrefixTransform
          kwargs:
            prefix: %LOGGER%
        writers:
        - class: UDPWriter      # Send raw NMEA to UDP
          kwargs:
            port: %RAW_UDP%
            interface: %INTERFACE%
    - class: ComposedWriter     # Also parse to fields and send to CACHE UDP
      kwargs:                   # port for CachedDataServer to pick up
        transforms:
        - class: PrefixTransform
          kwargs:
            prefix: %LOGGER%
        - class: ParseTransform
          kwargs:
            definition_path: local/devices/*.yaml,local/lmg/devices/*.yaml
        writers:
        - class: UDPWriter
          kwargs:
            port: %CACHE_UDP%
            interface: %INTERFACE%
    - class: ComposedWriter     # Also write parsed data to database
      kwargs:
        transforms:
        - class: PrefixTransform
          kwargs:
            prefix: %LOGGER%
        - class: ParseTransform
          kwargs:
            definition_path: local/devices/*.yaml,local/lmg/devices/*.yaml
        writers:
        - class: DatabaseWriter
    stderr_writers:          # Turn stderr into DASRecord, broadcast to cache
    - class: ComposedWriter  # UDP port for CachedDataServer to pick up.
      kwargs:
        transforms:
        - class: ToDASRecordTransform
          kwargs:
            field_name: 'stderr:logger:%LOGGER%'
        writers:
          class: UDPWriter
          kwargs:
            port: %CACHE_UDP%
            interface: %INTERFACE%
"""

def fill_vars(template, vars):
  output = template
  for src, dest in vars.items():
    output = output.replace(src, dest)
  return output

################################################################################
################################################################################

output = HEADER_TEMPLATE

################################################################################
# Fill in the logger definitions
output += """
########################################
loggers:
"""

LOGGER_DEF = """  %LOGGER%:
    configs:
    - %LOGGER%->off
    - %LOGGER%->net
    - %LOGGER%->file/net
    - %LOGGER%->file/net/db
"""
for logger in LOGGERS:
  output += fill_vars(LOGGER_DEF, VARS).replace('%LOGGER%', logger)

################################################################################
# Fill in mode definitions
output += """
########################################
modes:
  'off':
"""
for logger in LOGGERS:
  output += '    %LOGGER%: %LOGGER%->off\n'.replace('%LOGGER%', logger)
#### monitor
output += """
  monitor:
"""
for logger in LOGGERS:
  output += '    %LOGGER%: %LOGGER%->net\n'.replace('%LOGGER%', logger)
#### log
output += """
  log:
"""
for logger in LOGGERS:
  if logger:
    output += '    %LOGGER%: %LOGGER%->file/net\n'.replace('%LOGGER%', logger)
#### log+db
output += """
  'log+db':
"""
for logger in LOGGERS:
  if logger:
    output += '    %LOGGER%: %LOGGER%->file/net/db\n'.replace('%LOGGER%', logger)

output += """
########################################
default_mode: 'off'
"""

################################################################################
# Now output configs
output += """
########################################
configs:
"""
for logger in LOGGERS:
  output += """  ########"""
  output += fill_vars(OFF_TEMPLATE, VARS).replace('%LOGGER%', logger)
  # Special case for true winds, which is a derived logger
  if logger == 'true_wind':
    output += fill_vars(TRUE_WIND_TEMPLATE, VARS)
    continue

  # Look up port.tab values for this logger
  if not logger in MOXA:
    logging.warning('No port.tab entry found for %s; skipping...', logger)
    continue

  (inst, tty, baud, datab, stopb, parity, igncr, icrnl, eol, onlcr,
   ocrnl, icanon, vmin, vtime, vintr, vquit, opost) = MOXA[logger].split()
  net_writer = fill_vars(NET_WRITER_TEMPLATE, VARS)
  net_writer = net_writer.replace('%LOGGER%', logger)
  net_writer = net_writer.replace('%TTY%', tty)
  net_writer = net_writer.replace('%BAUD%', baud)
  output += net_writer

  file_net_writer = fill_vars(FILE_NET_WRITER_TEMPLATE, VARS)
  file_net_writer = file_net_writer.replace('%LOGGER%', logger)
  file_net_writer = file_net_writer.replace('%TTY%', tty)
  file_net_writer = file_net_writer.replace('%BAUD%', baud)
  output += file_net_writer

  full_writer = fill_vars(FULL_WRITER_TEMPLATE, VARS)
  full_writer = full_writer.replace('%LOGGER%', logger)
  full_writer = full_writer.replace('%TTY%', tty)
  full_writer = full_writer.replace('%BAUD%', baud)
  output += full_writer

print(output)

#display = DISPLAY_TEMPLATE

#output += fill_vars(DISPLAY_TEMPLATE, VARS)
#for logger in LOGGERS:
#  output += fill_vars(
