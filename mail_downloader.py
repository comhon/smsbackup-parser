import imaplib
import base64
import os
import email
import keyring
import mail_creds
import sys
import traceback
import langstrs
import email.header
import time
import datetime

service_id = 'comhon.smsbackup'

email_user = mail_creds.imap_user()
email_pass = mail_creds.imap_pass(email_user)

mail = imaplib.IMAP4_SSL(mail_creds.imap_host,mail_creds.imap_port)

res = None

#IMAP server login
print(langstrs.imap_logging_in) 

try:
    res, login_message = mail.login(email_user, email_pass)
except Exception as e:    
    print(e.args[0].decode())

#In case of failed login, terminate
if (res == None):
    sys.exit()

def this_logout():
    #IMAP server log out

    res, login_message = mail.logout()

    print(res)
    print(login_message[0].decode())


print(res)
print(login_message[0].decode())

print(langstrs.imap_opening_folder % mail_creds.imap_smsfolder) 

res = None
res, data = mail.select(mail_creds.imap_smsfolder, readonly=True)

if (res != 'OK'):
    print(langstrs.imap_folder_fail_open % mail_creds.imap_smsfolder)
    this_logout()
    sys.exit()

print(langstrs.imap_listing_emails) 

try:
    res = None
    res, data = mail.search(None, 'ALL')

except Exception as e:    
    print(langstrs.msgprefix_error+langstrs.imap_search_fail % str(e))

if (res == None):    
    this_logout()
    sys.exit()

mail_ids = data[0]
id_list = mail_ids.split()

print(langstrs.found_item_count % len(id_list))
print()

for num in mail_ids.split():
    
    print(langstrs.item_iteration % num.decode())
    typ, data = mail.fetch(num, '(RFC822)' )
    raw_email = data[0][1]

    for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1].decode('utf-8'))
                
                X_smssync_address       =msg["X-smssync-address"]
                X_smssync_datatype      =msg["X-smssync-datatype"]
                X_smssync_backup_time   =msg["X-smssync-backup-time"]
                X_smssync_version       =msg["X-smssync-version"]
                X_smssync_id            =msg["X-smssync-id"]
                X_smssync_type          =msg["X-smssync-type"]
                X_smssync_date          =msg["X-smssync-date"]
                X_smssync_thread        =msg["X-smssync-thread"]
                X_smssync_read          =msg["X-smssync-read"]
                X_smssync_status        =msg["X-smssync-status"]
                X_smssync_protocol      =msg["X-smssync-protocol"]
                X_smssync_service_center=msg["X-smssync-service_center"]

                email_subject = msg['Subject']
                email_mime_version= msg['MIME-Version']
                email_content_type= msg['Content-Type']
                email_from = msg['From']               
                email_to = msg['To']
                email_references = msg['References']
                email_message_id = msg['Message-ID']
                email_date = msg['Date']

                email_payload = msg.get_payload(decode=True)

                #email subject
                email_subject_parsed = email.header.decode_header(email_subject)
                if email_subject_parsed[0][1] == None:
                    print(langstrs.header_subject % email_subject_parsed[0][0])
                else:
                    print(langstrs.header_subject % email_subject_parsed[0][0].decode()) 

                #telephone number
                print( langstrs.smssync_address % X_smssync_address )  

                if (X_smssync_type == '1'):
                    print( langstrs.smssync_type % langstrs.str_inbound )

                if (X_smssync_type == '2'):
                    print( langstrs.smssync_type % langstrs.str_outbound )

                
                #date and time                
                #print( langstrs.email_header_date % email_date )
                #print( langstrs.smssync_date % X_smssync_date)
                epoch = int(X_smssync_date[0 : 10])
                print( langstrs.smssync_date % datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S'))
                              
                #print( langstrs.header_from % email.header.decode_header(email_from) )
                #print( langstrs.header_to % email.header.decode_header(email_to) )
             
                if (email_payload != None):
                    print (langstrs.email_message % email_payload.decode())
                else:
                    print()

this_logout()
print()