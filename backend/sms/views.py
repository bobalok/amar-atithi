from django.shortcuts import render
from zeep import Client


def send_sms(recipient, message):
    url = 'https://api2.onnorokomsms.com/sendsms.asmx?WSDL'
    client = Client(url)
    apiKey = "63618aa0-f178-41e5-81d1-58b41d6c5e06"
    return client.service.NumberSms(apiKey, message, recipient, "TEXT", "", "")


def SendVerificationSms(user):
    message = "You have successfully registered to Amar Otithi. Your verification code is : {}".format(user.mobile_code)
    send_sms(user.mobile, message)