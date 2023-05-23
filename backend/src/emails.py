import urllib

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


from env import HOME_URL
from src.settings import media_url, EMAIL_HOST_USER


def SendVerificationMail(user):
    # 0 == user not found
    # 1 = success
    # 2 = already verified

    link = "{}/verify/{}/{}".format(HOME_URL, user.email, user.email_code)
    htmly = get_template('verification-email.html')

    context = {
        'home': HOME_URL,
        'logo': media_url("assets/images/tw-logo.png"),
        'link': link,
        'receiver': user.nickname
    }

    subject = 'Welcome to Amar Otithi'
    html_content = htmly.render(context)
    text_content = 'Hi {},\n\r Welcome to Amar Otithi. In order to verify your email address, please click the link below: - {}\r\rThanks.' \
        .format(user.nickname, link)
    msg = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, [user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    # EmailLogs.objects.create(
    #     to=to,
    #     subject=subject,
    #     body=text_content,
    #     pid="verification_email",
    #     logged_user=request.user
    # )
