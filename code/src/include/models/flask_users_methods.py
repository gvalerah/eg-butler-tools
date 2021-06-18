    # source: code/src/include/models/flask_users_methods.py
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        '''
        if self.role is None:
            if self.username == current_app.config['BUTLER_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xfe).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        '''
        print(f"ENTRO A INIT DE User  con self={self}")
        print(f"ENTRO A INIT DE User  con kwargs={kwargs}")
        if self.role_id is None:
            if self.role is None:
                if self.username == current_app.config['BUTLER_ADMIN']:
                    self.role = Role.query.filter_by(permissions=0xfe).first()
                if self.role is None:
                    self.role = Role.query.filter_by(default=True).first()
        else:
            self.role = Role.query.filter_by(id=self.role_id).first()


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def is_god(self):
        return self.can(Permission.GOD)

    def is_customer(self):
        return self.can(Permission.CUSTOMER)

    def __repr__(self):
        return '<User %r role=%r/%r id=%r>' % (self.username,self.role,self.role_id)

