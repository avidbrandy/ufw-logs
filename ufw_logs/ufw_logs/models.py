from django.db import models
from django.utils import timezone


class Host(models.Model):

    name = models.CharField(max_length=64)
    creation_time = models.DateTimeField(null=True, help_text='timestamp when host was created')
    destruction_time = models.DateTimeField(null=True, help_text='timestamp when host was deleted')
    ip = models.ForeignKey('IP', related_name='hosts', on_delete=models.PROTECT)


class IP(models.Model):
    
    address = models.CharField(primary_key=True, unique=True, max_length=39)
    

class Log(models.Model):
    
    log_id = models.CharField(primary_key=True, unique=True, max_length=100, 
                              help_text='{src.address}:{spt.number} {str(timestamp)[:-6]} {dst.address}:{dpt.number} - {packetid}')
    timestamp = models.DateTimeField()
    host = models.ForeignKey(Host, related_name='logs', on_delete=models.PROTECT)
    src = models.ForeignKey(IP, related_name='logs_as_src', on_delete=models.PROTECT, help_text='source IP address')
    dst = models.ForeignKey(IP, related_name='logs_as_dst', on_delete=models.PROTECT, help_text='destination IP address')
    spt = models.ForeignKey('Port', null=True, related_name='sources', on_delete=models.PROTECT, help_text='source port')
    dpt = models.ForeignKey('Port', null=True, related_name='destinations', on_delete=models.PROTECT, help_text='destination port')
    protocol = models.CharField(null=True, max_length=5, help_text='https://en.wikipedia.org/wiki/List_of_IP_protocol_numbers')
    packetlength = models.IntegerField(null=True)
    windowsize = models.IntegerField(null=True)
#    syn = models.BooleanField(null=True, help_text='whether or not this logged attempt was an initial SYN')
    ttl = models.IntegerField(null=True, help_text='time to live')
    df = models.BooleanField(default=0, help_text='dont fragment bit')
    tos = models.CharField(null=True, max_length=5, help_text='https://linuxreviews.org/Type_of_Service_(ToS)_and_DSCP_Values')
    precedence = models.CharField(null=True, max_length=5, help_text='https://linuxreviews.org/Type_of_Service_(ToS)_and_DSCP_Values')
    res = models.CharField(null=True, max_length=5, 
                           help_text='Reserved bits. This field is used, optionally, for things like ECNE and CWR.')
    packetid = models.IntegerField(null=True, help_text='unique ID for datagram. If packet is a fragment, all fragments share same ID.')
    login = models.ForeignKey('Login', null=True, related_name='attempts', on_delete=models.PROTECT)
    

class Login(models.Model):
    
    username = models.CharField(max_length=64)
    password = models.CharField(null=True, max_length=64)
    ip = models.ForeignKey(IP, null=True, related_name='aliases', on_delete=models.PROTECT, 
                           help_text='IP address that used this Login')


class Port(models.Model):
    
    number = models.IntegerField(primary_key=True, unique=True, help_text='just your standard port number')