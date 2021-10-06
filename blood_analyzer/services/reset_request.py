from flask import url_for
from flask_mail import Message

from blood_analyzer import _MAIL

def send_mail_with_reset(reset_req, server_reset_token):
    User, form, flash = reset_req
    user = User.query.filter_by(email=form.email.data).first()
    send_reset_email(user, server_reset_token)
    flash("An email has been sent with instructions to reset your password", "info")


def send_reset_email(user, server_reset_token):
    token = user.get_reset_token()
    msg = Message("Password Reset Request",
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f"""To reset your password, visit following link:
{url_for(server_reset_token, token=token, _external=True)}

If you didn't make this request then simply ignore this email and no change will be made.
"""
    _MAIL.send(msg)
