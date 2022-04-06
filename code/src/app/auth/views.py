# app/auth/views.py    
from flask                              import render_template, redirect, request, url_for, flash
from flask_login                        import login_user
from .                                  import auth
from emtec.debug                        import *
from emtec.ldap                         import *
from emtec.butler.db.flask_models       import User
from .forms                             import LoginForm
from .forms                             import ChangePasswordForm
from .forms                             import ResetPasswordForm
from .forms                             import ChangeEmailForm
from .forms                             import RegistrationForm

from ..                                 import db,logger

# Authorization sub-system
from ..decorators                       import admin_required, permission_required

from flask_login                        import login_user
from flask_login                        import logout_user
from flask_login                        import login_required
from flask_login                        import current_user
from flask_babel                        import gettext
from flask_babel                        import lazy_gettext
from flask                              import current_app

@auth.route('/login', methods=['GET', 'POST'])
def login():
    #20210710 GV logger not checked is mandatory now: logger=check_logger()
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
        success = False
        if user.ldap:
            flash(f"user {user} requires LDAP authentication")
            try:
                # LDAP default methos is SIMPLE, otherwise needs to be specified
                if user.ldap_method is None:
                    method = 'SIMPLE'
                else:
                    method = user.ldap_method.strip().upper()
                if len(method):
                    flash(f"method= {method}")
                    ldap_user_name = user.ldap_user
                    ldap_common_name = user.ldap_common
                    host   = user.ldap_host   if user.ldap_host   is not None else current_app.config.get('LDAP_HOST')
                    port   = user.ldap_port   if user.ldap_port               else current_app.config.get('LDAP_PORT')
                    domain = user.ldap_domain if user.ldap_domain is not None else current_app.config.get('LDAP_DOMAIN')
                    # Elemental very simple OPEN LDAP Authentication
                    if method == 'SIMPLE': 
                        LDAP_username = ldap_username(username=ldap_user_name,common_name=ldap_common_name,domain=domain)
                        success = ldap_authentication(LDAP_username, form.password.data,host=host,port=port,logger=logger)


                    """
                    def ldap_authentication_msad(address, username, password,
                                protocol_version = 3,
                                options          = [(ldap.OPT_REFERRALS,0)],
                                return_connection = False,
                                logger            = logging.getLogger(),
                        ):
                    """

                    # MS Windows Active Directory Authentication
                    elif method in ['MSAD','WINDOWS']:
                        # Gets sure LDAP username format is DOMAIN\USERNAME
                        if ldap_user_name.find("\\")>-1: pass
                        elif ldap_user_name.find("@")>-1: pass
                        else: ldap_user_name = f"{domain.upper()}\\{ldap_user_name}"
                        options = {}
                        # defaults
                        '''
                        protocol = 3
                        options  = [(ldap.OPT_REFERRALS,0)]
                        if len(user.vars):
                            pairs = user.vars.split(',')
                            for pair in pairs:
                                var,value=pair.split('=')
                                variables.update({var:value})
                            for variable in variables:
                                if variable == 'protocol':protocol=int(value)
                                else:
                                    key = getattr(ldap,key)
                                    if key is not None:
                                        # cast value to int if possible
                                        try:
                                            value=int(value)
                                        except:
                                            pass
                                        options.append((key,value))
                        '''
                        if len(user.vars):
                            vars = json.loads(user.vars)
                        else:
                            vars = {}
                        flash(f"host={host} user={ldap_user_name} pwd={form.password.data} vars={vars}")
                        success = ldap_authentication_msad(host, ldap_user_name, form.password.data, logger=logger,**vars)
                    # Legacy NT Lan Manager authentication should be considered obsolete
                    elif method in ['NTLM']: 
                        if ldap_user_name.find("\\")>-1: pass
                        elif ldap_user_name.find("@")>-1:
                            usr,dom = ldap_user_name.split('@',1)
                            ldap_user_name = f"{str(dom).upper()}\\{usr}"
                        else: ldap_user_name = f"{domain.upper()}\\{ldap_user_name}"
                        flash(f"host={host} user={ldap_user_name} pwd={form.password.data}")
                        vars = json.loads(user.vars)
                        url = f"http://{domain}/{vars.get('endpoint')}"
                        success = ldap_authentication_ntlm(url, ldap_user_name, form.password.data,logger=logger)
                    if success:
                        login_user(user, False)
                        return redirect(request.args.get('next') or url_for('main.index'))
                    else:
                        flash(gettext('Invalid username or password.'),'error')
                else:
                    flash(gettext('Invalid authentication method required.'),'error')
            except Exception as e:
                flash(f"EXCEPTION: {str(e)}",'error')
        else:
            logger.debug(f"2 user={user}")
            if user is not None and user.verify_password(form.password.data.strip()):
                #login_user(user, form.remember_me.data)
                login_user(user, False)
                try:
                    logger.debug(f'auth.login 2.1 after login current user={current_user}')
                except Exception as e: 
                    logger.error(f'auth.login 2.2 after login exception: {str(e)}') 
                logger.debug(f"3.1 request.args.get('next')={request.args.get('next')}")
                logger.debug(f"3.2 url_for('main.index')   ={url_for('main.index')}")
                return redirect(request.args.get('next') or url_for('main.index'))
            flash(gettext('Invalid username or password.'),'error')
    else:
        try:
            logger.warning("auth.login 4 FORM NOT VALIDATED YET")        
        except Exception as e:
            logger.error(f"app auth login: EXCEPTION: {str(e)}")
    logger.debug(f"auth.login 5 will render template auth/login.html ...")
    return render_template('auth/login.html', form=form)
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(gettext('You have been logged out.'))
    return redirect(url_for('main.index'))
    
# Only Administrator can register users, include decorator here
@auth.route('/register', methods=['GET', 'POST'])
@login_required
@admin_required
def register():
    #20210710 GV logger not checkd is mandatiry now: logger=check_logger()
    form = RegistrationForm()
    try:
        db.session.flush()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.close()
        emtec_handle_general_exception(e,logger=logger)
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
            try:
                db.session.close()
                db.session.add(user)
                db.session.flush()
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                db.session.close()
                emtec_handle_general_exception(e,logger=logger)
            logger.debug('New user "%s" can login now.'%form.username.data)
            flash('New user "%s" can login now.'%form.username.data)
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            db.session.close()
            flash('Form Data is: [name=%s,role_id=%s,email=%s,password=%s]'%( form.username.data, form.role_id.data, form.email.data, form.password.data))
            flash('Error creating new user. %s'%(e))
            emtec_handle_general_exception(e,logger=logger)
            return redirect(url_for('auth.register'))
            
    return render_template('auth/register.html', form=form)
    
@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    # 20210609 cambio 
    try:
        db.session.flush()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.close()
        emtec_handle_general_exception(e,logger=logger)
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
            try:
                db.session.merge(user)
                db.session.flush()
                db.session.commit()
                if user.username == current_user.username:
                    flash('Your password has been updated.')
                else:
                    flash(f"'{user.username}' password has been updated.")
            except Exception as e:
                db.session.rollback()
                db.session.close()
                emtec_handle_general_exception(e,logger=logger)
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
