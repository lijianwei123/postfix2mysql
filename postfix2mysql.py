#!/usr/bin/python2
# -*- coding: utf8 -*-

import re;
import MySQLdb;

db_host = 'localhost';
db_user = 'root';
db_pass = 'toor';
db_name = 'maillog'
logfile = 'maillog';

email = re.compile('<[a-zA-Z0-9@.-_]+>');
badwords = ['warning:','disconnect'];

class Record:
    '''Structure for an event with uniq id'''
    _from = '' ;
    _to = '';
    _time = '';

def insertRecord(record):
    pass;


db = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8');
cursor = db.cursor();

records = {};
maillog = open(logfile,'r');
for line in maillog:
    (mailer, msgid, event) = line.split()[4:7];
    if mailer.startswith('postfix') and not (msgid in badwords):
        if not records.has_key(msgid):
                records[msgid] = Record();
        if event.startswith('from'):
                match = email.search(event);
                if (match):
                    records[msgid]._from = email.search(event).group(); 
        if event.startswith('to'):
                match = email.search(event);
                if (match):
                    records[msgid]._from = email.search(event).group(); 
        if event.startswith('removed'):
            pass;

maillog.close();


#for key in records.keys():
#    print records[key]._from;

