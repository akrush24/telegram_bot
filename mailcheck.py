#!/usr/bin/env python3
from exchangelib import DELEGATE, Account, Credentials
mailcount = 5
from passwd import mailuser, mailpasswd

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
# Print first 100 inbox messages in reverse order
for item in account.inbox.filter(is_read=False).order_by('-datetime_received')[:mailcount]:
#for item in account.inbox.all().order_by('-datetime_received')[:2]:
    print(str(item.datetime_received) + ": " + "FROM: " + str(item.sender.email_address) + "; SUBJ: " + item.subject)
    #print(item.subject, item.body, item.attachments)
