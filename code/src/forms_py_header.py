# ----------------------------------------------------------------------
# code/src/forms_py_header.py
# Flask required modules
from flask_wtf              import FlaskForm as Form
from wtforms                import Field
from wtforms                import StringField
from wtforms                import TextField
from wtforms                import TextAreaField
from wtforms                import IntegerField
from wtforms                import DecimalField
from wtforms                import DateTimeField
from wtforms                import BooleanField
from wtforms                import SelectField
from wtforms                import SubmitField
from wtforms                import RadioField
from wtforms_components     import TimeField
from wtforms.fields.html5   import DateField
from wtforms.validators     import Required, AnyOf, DataRequired, Email
from wtforms.validators     import EqualTo, HostnameValidation
from wtforms.validators     import IPAddress, InputRequired, Length
from wtforms.validators     import MacAddress, NoneOf, NumberRange
from wtforms.validators     import Optional
from wtforms.validators     import Regexp, Required
# ----------------------------------------------------------------------

