from blood_analyzer.db.models import _DB, User


def register_to_app(register_req, server_login):
    _BCRYPT, form, redirect, flash, url_for = register_req
    password = _BCRYPT.generate_password_hash(form.password.data).decode("utf-8")
    new_user = User(
        username=form.username.data, email=form.email.data, password=password
    )
    _DB.session.add(new_user)
    _DB.session.commit()
    flash(f"Account created for Doctor {form.username.data}!", "success")
    return redirect(url_for(server_login))
