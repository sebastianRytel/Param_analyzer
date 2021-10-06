
def reset_password(reset_req, user):
    _BCRYPT, _DB, form, flash = reset_req
    password = _BCRYPT.generate_password_hash(form.password.data).decode("utf-8")
    user.password = password
    _DB.session.commit()
    flash("Your password has been updated. You are able to log in.")
