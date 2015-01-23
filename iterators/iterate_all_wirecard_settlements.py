# An iterator for stepping through invoice emails via imap.
import os

try:
	address = os.environ['WIRECARD_EMAIL']
	password = os.environ['WIRECARD_EMAIL_PASSWORD']
except:
	print "Set your email and password in environment variables WIRECARD_EMAIL and WIRECARD_EMAIL_PASSWORD."
	print
	print "For example"
	print "  export WIRECARD_EMAIL=me@bemmu.com"
	print "  export WIRECARD_PASSWORD=veryverysecret"
	exit()

def iterate_wirecard_settlements():
	import imaplib
	import email
	import base64

	mail = imaplib.IMAP4_SSL('imap.gmail.com')
	mail.login(address, password)
	mail.select("[Gmail]/All Mail")

	# "Settlement Note for TMI"
	# from:noreply@wirecard.com

	result, data = mail.uid('search', '(HEADER From "noreply@wirecard.com")')

	for uid in data[0].split():
		result, data = mail.uid('fetch', uid, '(RFC822)')
		raw_email = data[0][1]
		email_message = email.message_from_string(raw_email)

		if email_message['Subject'].startswith("Settlement Note") or email_message['Subject'].startswith("Balance Note"):
			assert(email_message.is_multipart())
			pdf = email_message.get_payload(1)
			pdf = base64.b64decode(pdf.get_payload())
			assert(pdf[1:4] == "PDF")

			yield {
				"Subject" : email_message['Subject'],
				"pdf" : pdf
			}

if __name__ == "__main__":
	for settlement in iterate_wirecard_settlements():
		print settlement["Subject"]