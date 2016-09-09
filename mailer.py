import getpass
import os
import imaplib
import email
from OpenSSL.crypto import load_certificate, FILETYPE_PEM


def getMsgs(servername="imap.google.com"):
    usernm = getpass.getuser()
    passwd = getpass.getpass()
    subject = 'Your SSL Certificate'
    conn = imaplib.IMAP4_SSL(servername)
    conn.login(usernm, passwd)
    conn.select('Inbox')
    typ, data = conn.search(None, '(UNSEEN SUBJECT "%s")' % subject)
    for num in data[0].split():
        typ, data = conn.fetch(num, '(RFC822)')
        msg = email.message_from_string(data[0][1])
        typ, data = conn.store(num, '-FLAGS', '\\Seen')
        yield msg


def getAttachment(msg, check):
    for part in msg.walk():
        if part.get_content_type() == 'application/octet-stream':
            if check(part.get_filename()):
                return part.get_payload(decode=1)
if __name__ == '__main__':
    for msg in getMsgs():
        payload = getAttachment(msg, lambda x: x.endswith('.pem'))
        if not payload:
            continue
        try:
            cert = load_certificate(FILETYPE_PEM, payload)
        except:
            cert = None
        if cert:
            cn = cert.get_subject().commonName
            filename = "%s.pem" % cn
            if not os.path.exists(filename):
                open(filename, 'w').write(payload)
                print "Writing to %s" % filename
            else:
                print "%s already exists" % filename
