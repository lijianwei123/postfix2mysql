#!/usr/bin/python2
# -*- coding: utf8 -*-

import re;
import MySQLdb;
import sys;
import os;

db = {
    'host' : 'localhost',
    'user' : 'root',
    'passwd' : 'toor',
    'name' : 'maillog'
};

ignore = ['viruscontrol@trade.su'];

if len(sys.argv) > 1:
    logfile = sys.argv[1];
else:
    logfile = "maillog"

email = re.compile('<[a-zA-Z0-9@.-_]+>');
badwords = ['warning:','disconnect'];


class Record:
    '''Structure to store an event with uniq id'''
    _from = '' ;
    _to = '';
    _time = '';

def insertRecord(db, record):
    sql = '''INSERT INTO `log` (`time`, `from`, `to`) VALUES ('%(time)s', '%(from)s', '%(to)s');'''%{'time':record._time, 'from':record._from, 'to':record._to.strip()};
    print sql;
    db.query(sql);
    db.commit();

def createTable(db):
    sql = '''CREATE TABLE IF NOT EXISTS `log` (`id` INT NOT NULL AUTO_INCREMENT,`time` CHAR(60),`from` CHAR(60),`to` CHAR(60), PRIMARY KEY (`id`));'''
    db.query(sql);
    db.commit();

try:
    db = MySQLdb.connect(host=db['host'], user=db['user'], passwd=db['passwd'], db=db['name'], charset='utf8');
    createTable(db);
except Exception, e:
    print 'Database connection error: '+repr(e);
    sys.exit();

records = {};
if os.path.isfile(logfile):
    with open(logfile,'r') as maillog: 
        for line in maillog:
            (mailer, msgid, event) = line.split()[4:7];
            if mailer.startswith('postfix') and msgid not in badwords:
                if not records.has_key(msgid):
                        records[msgid] = Record();
                        records[msgid]._time = " ".join(line.split()[0:3]);
                if event.startswith('from'):
                        match = email.search(event);
                        if match and match not in ignore:
                            records[msgid]._from = email.search(event).group().strip('><');
                if event.startswith('to'):
                        match = email.search(event);
                        if match and match not in ignore:
                            records[msgid]._to += email.search(event).group().strip('><')+" "; 
                if event.startswith('removed'):
                    insertRecord(db, records[msgid]);
                    del (records[msgid]);
else:
    print logfile+" : file not found"
