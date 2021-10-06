from blood_analyzer.db.models import User


def login_to_app(login_req):
    _BCRYPT, form, flash, login_user = login_req
    user = User.query.filter_by(email=form.email.data).first()
    if user and _BCRYPT.check_password_hash(user.password, form.password.data):
        login_user(user, remember=form.remember.data)
        flash("You have successfully logged in.", "success")
    else:
        flash("Login Unsuccessful. Please check email and password!", "danger")
