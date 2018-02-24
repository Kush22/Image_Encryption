from twilio.rest import TwilioRestClient
import os


def messagePhoneSend(sendTo, messageBody):
	try:
		print "Send Message"
		account = "DEFAULT_ACCOUNT_NUMBER"
		token = "DEFAULT_TOKEN"
		client = TwilioRestClient(account, token)

		sendNumber = "+91"+sendTo
		print sendNumber
		message = client.messages.create(to=sendNumber, from_="+19402022817",
		                                 body=messageBody)
		os.system("notify-send Encrypto: 'Key Sent Successfully through Phone'")
	except:
		os.system("notify-send Encrypto: 'Error Sending the Key Through Phone'")

if __name__ == '__main__':
	messageSend("8376071713", "Encrypto Message")
