# app/auth/views.py    
from flask                              import render_template, redirect, request, url_for, flash
from flask_login                        import login_user
from .                                  import auth
from emtec.debug                        import *
from emtec.butler.db.flask_models       import User
from .forms                             import LoginForm
from .forms                             import ChangePasswordForm
from .forms                             import ResetPasswordForm
from .forms                             import ChangeEmailForm
from .forms                             import RegistrationForm

from ..                                 import db

# Authorization sub-system
from ..decorators                       import admin_required, permission_required

from flask_login                        import login_user
from flask_login                        import logout_user
from flask_login                        import login_required
from flask_login                        import current_user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    #20210710 GV logger not checkd is mandatiry now: logger=check_logger()
    try:
        logger.debug("auth.login login in course ...")
    except:
        logger.warning("auth.login 1.1 logger is not available")
    try:    logger.debug(f'current user={current_user}')
    except Exception as e: print(f'current user no definido aun: {str(e)}') 
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        try:    logger.debug(f'auth.login user={current_user}')
        except Exception as e: print(f'auth.login user ??? : {str(e)}')
        logger.debug("2 user=",user)
        if user is not None and user.verify_password(form.password.data):
            #login_user(user, form.remember_me.data)
            login_user(user, False)
            try:
                logger.debug(f'auth.login 2.1 after login current user={current_user}')
            except Exception as e: 
                logger.error(f'auth.login 2.2 after login exception: {str(e)}') 
            logger.debug("3.1 request.args.get('next')=",request.args.get('next'))
            logger.debug("3.2 url_for('main.index')   =",url_for('main.index'))
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    else:
        pass
        logger.warning("auth.login 4 FORM NOT VALIDATED YET")        
    logger.debug("auth.login 5 will render template auth/login.html ...")
    return render_template('auth/login.html', form=form)
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
    
    
# Only Administrator can register users, include decorator here
@auth.route('/register', methods=['GET', 'POST'])
@login_required
@admin_required
def register():
    #20210710 GV logger not checkd is mandatiry now: logger=check_logger()
    form = RegistrationForm()
    db.session.flush()
    db.session.commit()
    if form.validate_on_submit():
        logger.debug(f"form.username.data = {form.username.data}")
        logger.debug(f"form.role_id.data  = {form.role_id.data}")
        logger.debug(f"form.email.data    = {form.email.data}")
        logger.debug(f"form.password.data = {form.password.data}")
        
        user = User(username=form.username.data,
            role_id=form.role_id.data,
            email=form.email.data,
            password=form.password.data)
        flash('Register')
        try:
            logger.debug("Trying to register user: '%s'"%user)
            user.role_id=form.role_id.data
            logger.debug("Trying to register user: '%s'"%user)
            db.session.close()
            db.session.add(user)
            db.session.flush()
            db.session.commit()
            logger.debug('New user "%s" can login now.'%form.username.data)
            flash('New user "%s" can login now.'%form.username.data)
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            db.session.close()
            flash('Form Data is: [name=%s,role_id=%s,email=%s,password=%s]'%( form.username.data, form.role_id.data, form.email.data, form.password.data))
            flash('Error creating new user. %s'%(e))
            return redirect(url_for('auth.register'))
            
    return render_template('auth/register.html', form=form)
    
@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    # 20210609 cambio 
    db.session.flush()
    db.session.commit()
    if current_user.role_id in (4,6):
        form = ResetPasswordForm()
    else:
        form = ChangePasswordForm()
        username = current_user.username
    if form.validate_on_submit():
        flash('Change Password')
        if current_user.verify_password(form.old_password.data):
            if hasattr(form,'username'):
                user = db.session.query(User).filter(User.username==form.username.data).first()
            else:
                user = current_user
            user.password = form.password.data
            db.session.merge(user)
            db.session.flush()
            db.session.commit()
            if user.username == current_user.username:
                flash('Your password has been updated.')
            else:
                flash(f"'{user.username}' password has been updated.")
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form,user=current_user)

@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template("auth/change_email.html", form=form)

    
"""    
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm,\
    PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template("auth/change_email.html", form=form)


@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('main.index'))
    
"""    
    
    
