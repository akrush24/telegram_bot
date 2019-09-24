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
        res.append(str(item.datetime_received) + "\n" + "FROM: " + str(item.sender.email_address) + "; SUB: " + item.subject + "\n" + item.body)
        #print(item.subject, item.body, item.attachments)

    return res

#print ( str(mailcheck(mailuser, mailpasswd, 2)) )
