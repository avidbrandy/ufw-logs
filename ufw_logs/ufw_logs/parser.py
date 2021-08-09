from ufw_logs.models import Host, IP, Log, Login, Port

from django.utils import timezone

import csv
import os


def parse_logs(filepath):

    # input is the filepath for ufw logs (ensure file permissions)
    # parses the logs and adds them to database

    file = open(filepath, 'r')
    reader = csv.reader(file)
    logs = []
    srcs = []
    year = timezone.now().year
    for line in reader:

        try:
            # days 1-9 seem to have an extra space for padding
            data = line[0].replace('  ',' ').split(' ')

            # rewrite this later. very inefficient
            for entry in data:

                # acquire destination IP, then create the Host object if needed using IP object
                # this has to be done first, then we iterate through to fill in the other variables
                if 'DST=' in entry:
                    if 'dst' in locals():
                        if dst.address == entry.split('=')[1]:
                            pass
                        else:
                            dst, _new = IP.objects.get_or_create(address=entry.split('=')[1])
                    else:
                        dst, _new = IP.objects.get_or_create(address=entry.split('=')[1])

                    if 'host' in locals():
                        if host.ip == dst and host.name == data[3]:
                            pass
                        else:
                            host, _new = Host.objects.get_or_create(name=data[3], ip=dst)
                    else:
                        host, _new = Host.objects.get_or_create(name=data[3], ip=dst)
                    break

            # create timestamp
            # might be a bug here if logs are from December and this function in run in January

            month = timezone.datetime.strptime(data[0], '%b').month

            # unknown error where day was empty value ''
            # this try statement will usually fix it by reusing the day value from the previous entry
            try:
                day = int(data[1])
            except:
                print(f'Error with {filepath}')
                print(f'{line[0]}')

            time = timezone.datetime.strptime(data[2], '%H:%M:%S')
            timestamp = timezone.datetime(year, month, day, time.hour, time.minute, time.second).replace(tzinfo=timezone.utc)

            src = IP(address=[entry.split('=')[1] for entry in data if 'SRC=' in entry][0])
            packetid = int([entry.split('=')[1] for entry in data if 'ID=' in entry][0])
            try:
                spt = Port(number=int([entry.split('=')[1] for entry in data if 'SPT=' in entry][0]))
                dpt = Port(number=int([entry.split('=')[1] for entry in data if 'DPT=' in entry][0]))
                log_id = f'{src.address}:{spt.number} {str(timestamp)[:-6]} {dst.address}:{dpt.number} - {packetid}'
            except:
                spt = Port(number=0)
                dpt = Port(number=0)
                log_id = f'{src.address}:{spt} {str(timestamp)[:-6]} {dst.address}:{dpt} - {packetid}'
            log = Log(log_id=log_id, timestamp=timestamp, host=host, dst=dst, src=src, packetid=packetid, spt=spt, dpt=dpt)

            for entry in data:

                if 'LEN=' in entry:
                    log.packetlength = int(entry.split('=')[1])
                elif 'TOS=' in entry:
                    log.tos = entry.split('=')[1]
                elif 'PREC=' in entry:
                    log.precedence = entry.split('=')[1]
                elif 'TTL=' in entry:
                    log.ttl = int(entry.split('=')[1])
                elif 'PROTO=' in entry:
                    log.protocol = entry.split('=')[1]
                elif 'WINDOW=' in entry:
                    log.windowsize = int(entry.split('=')[1])
                elif 'RES=' in entry:
                    log.res = entry.split('=')[1]
                elif entry == 'DF':
                    log.df = True

            logs.append(log)
            srcs.append(src)
            print(src.address)

        except:
            print(f'Error with {filepath}')
            print(f'{line[0]}')

        if len(logs) >= 500:
            IP.objects.bulk_create(srcs, ignore_conflicts=True)
            srcs = []
            Log.objects.bulk_create(logs, ignore_conflicts=True)
            logs = []


    IP.objects.bulk_create(srcs, ignore_conflicts=True)
    Log.objects.bulk_create(logs, ignore_conflicts=True)
    return
