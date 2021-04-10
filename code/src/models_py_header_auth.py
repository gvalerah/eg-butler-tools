# =============================================================================
# Models File
# Authorization subsystem. 
# Static File. 
# GLVH 2018-12-17
# source: models_py_header_auth.py
# =============================================================================

class Permission:
    CUSTOMER            = 0x001
    VIEW                = 0x002
    DELETE              = 0x004
    MODIFY              = 0x008
    REPORT              = 0x010
    EXPORT              = 0x020
    RESERVED040         = 0x040
    ADMINISTER          = 0x080
    AUDIT               = 0x100
    RESERVED200         = 0x200
    RESERVED400         = 0x400
    GOD                 = 0x8

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


