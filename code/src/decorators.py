# ======================================================================
# Decorators
# source file name: decorators.py
# Static Header File. 
# GLVH 2020-10-11
# ----------------------------------------------------------------------
from functools                          import wraps
from flask                              import abort
from flask_login                        import current_user
from emtec.butler.db.flask_models       import Permission

def permission_required(permission):

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)
# ----------------------------------------------------------------------
