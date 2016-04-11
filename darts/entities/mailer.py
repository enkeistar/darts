from darts import app
from flask_mail import Mail, Message

class Mailer():

	def send(self, subject, body):
		mail = Mail(app)
		messages = Message(subject, sender = ("XPX Darts App", "brettmeyerxpx@gmail.com"), recipients = ["brettmeyerxpx@gmail.com"])
		messages.body = body
		mail.send(messages)
