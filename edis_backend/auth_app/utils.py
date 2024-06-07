from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data["email_subject"],
            body=data["email_body"],
            to=[data["email_to"]],
        )
        email.content_subtype = "html"
        email.send()

    @staticmethod
    def get_verification_email_body(user_name, verification_url):
        template_path = "email_verification.html"
        context = {"user_name": user_name, "verification_url": verification_url}
        html_message = render_to_string(template_path, context)
        return html_message

    @staticmethod
    def get_password_reset_email_body(user_name, reset_url):
        template_path = "reset_password.html"
        context = {"user_name": user_name, "reset_url": reset_url}
        html_message = render_to_string(template_path, context)
        return html_message
