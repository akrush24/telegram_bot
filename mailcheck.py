#!/usr/bin/env python3
from exchangelib import DELEGATE, Account, Credentials
from passwd import mailuser, mailpasswd

def mailcheck(mailuser, mailpasswd, mailcount):
    if mailcount is None:
        mailcount = 5

    credentials = Credentials(
        username=mailuser,
        password=mailpasswd
    )

    account = Account(
        primary_smtp_address=mailuser,
        credentials=credentials,
        autodiscover=True,
        access_type=DELEGATE
    )

    res = []
    for item in account.inbox.filter(is_read=False).order_by('-datetime_received')[:mailcount]:
        res.append("[" + str(item.datetime_received) + "]\n" + "F: " + str(item.sender.email_address) + "\nS: " + item.subject)
        #print(item.subject, item.body, item.attachments)

    return res
try:
    print ( str(mailcheck(mailuser, mailpasswd, 2)) )
except:
    pass
