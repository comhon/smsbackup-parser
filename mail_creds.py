import keyring
import langstrs
import getpass

imap_host = 'imap.volny.cz'

imap_port = 993 #check for tiemout error

imap_smsfolder = 'SMS'

service_id = 'comhon.smsbackup'
service_id_user = 'comhon.smsbackup.user'
username_value = 'value'

def imap_user():
    username = keyring.get_password(service_id_user, username_value) # retrieve username 
    if (username == None):
        username = input(langstrs.imap_username_prompt % imap_host )

    return username

def imap_pass():
    return imap_pass(imap_user())

def imap_pass(username):    
    password = keyring.get_password(service_id, username) # retrieve password 
    if (password == None):
        password = getpass.getpass(langstrs.imap_pass_prompt % (username,imap_host) )

    return password

def storeusername():
    print('Saving username...')
    username_str = imap_user()    
    keyring.set_password(service_id_user,username_value,username_str)

def storepass():
    print('Saving password...')
    password_str = imap_pass()    
    keyring.set_password(service_id,imap_user,password_str)

def clearpass():
    keyring.delete_password(service_id,imap_user)
