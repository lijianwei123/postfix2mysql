#!/usr/bin/python2

badwords = ['warning:','disconnect'];
records = {};
class Record:
    pass;

maillog = open ('maillog','r');
for line in maillog:
    (mailer, msgid) = line.split()[4:6];
    if mailer.startswith('postfix') and not (msgid in badwords):
        if not records.has_key(msgid):
                records[msgid] = Record();
            
maillog.close();


print records.keys(); 
