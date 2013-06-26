#!/usr/bin/python2
# -*- coding: utf8 -*-

import re;
import MySQLdb;

db_host = 'localhost';
db_user = 'root';
db_pass = 'toor';
db_name = 'maillog'
logfile = 'maillog_';

email = re.compile('<[a-zA-Z0-9@.-_]+>');
badwords = ['warning:','disconnect'];

class Record:
    '''Structure for an event with uniq id'''
    _from = '' ;
    _to = '';
    _time = '';

def insertRecord(db, record):
    sql = '''INSERT INTO `log` (`time`, `from`, `to`) VALUES ('%(time)s', '%(from)s', '%(to)s');'''%{'time':record._time, 'from':record._from, 'to':record._to};
    print sql;
    db.query(sql);
    db.commit();

def createTable(db):
    sql = '''CREATE TABLE IF NOT EXISTS `log` (`id` INT NOT NULL AUTO_INCREMENT,`time` CHAR(60),`from` CHAR(60),`to` CHAR(60), PRIMARY KEY (`id`));'''
    db.query(sql);
    db.commit();

db = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8');
createTable(db);

records = {};
maillog = open(logfile,'r');
for line in maillog:
    (mailer, msgid, event) = line.split()[4:7];
    if mailer.startswith('postfix') and not (msgid in badwords):
        if not records.has_key(msgid):
                records[msgid] = Record();
                records[msgid]._time = " ".join(line.split()[0:3]);
        if event.startswith('from'):
                match = email.search(event);
                if (match):
                    records[msgid]._from = email.search(event).group(); 
        if event.startswith('to'):
                match = email.search(event);
                if (match):
                    records[msgid]._from = email.search(event).group(); 
        if event.startswith('removed'):
            insertRecord(db, records[msgid]);
            del (records[msgid]);
maillog.close();
