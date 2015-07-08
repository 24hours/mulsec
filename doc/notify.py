import smtplib
from email.mime.text import MIMEText
import logging
import sys
 

def notify(reciever, file_name):
	try:
		from mail_config import gmail_account, gmail_password
	except ImportError:
		print "Failed to obtain email crediential"
		return 

	# Open a plain text file for reading.  For this example, assume that
	# the text file contains only ASCII characters.
	fp = open(file_name, 'rb')
	# Create a text/plain message
	msg = MIMEText(fp.read())
	fp.close()

	# me == the sender's email address
	# you == the recipient's email address
	msg['Subject'] = 'Mulsec-Cluster Notification sub-system.'
	msg['From'] = gmail_account
	msg['To'] = reciever


	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()

	server.login(gmail_account, gmail_password)
	server.sendmail(gmail_account, reciever, msg.as_string())
	server.quit()



class StreamToLogger(object):
   """
   Fake file-like stream object that redirects writes to a logger instance.
   """
   def __init__(self, logger, log_level=logging.INFO):
      self.logger = logger
      self.log_level = log_level
      self.linebuf = ''
 
   def write(self, buf):
      for line in buf.rstrip().splitlines():
         self.logger.log(self.log_level, line.rstrip())

def pipe_to_file(filename): 
	logging.basicConfig(
	   level=logging.DEBUG,
	   format='%(message)s',
	   filename=filename,
	   filemode='w'
	)
	 
	stdout_logger = logging.getLogger('STDOUT')


	sl = StreamToLogger(stdout_logger, logging.INFO)
	sys.stdout = sl
	 
	stderr_logger = logging.getLogger('STDERR')


	sl = StreamToLogger(stderr_logger, logging.ERROR)
	sys.stderr = sl