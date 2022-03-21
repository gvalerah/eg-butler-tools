# ----------------------------------------------------------------------
# code/src/forms_py_header.py
# Flask required modules
import os
from flask                  import current_app
from flask_wtf              import FlaskForm as Form
from wtforms                import Field
from wtforms                import StringField
# GV 20220224  Obsolete TextField will be replaced by StrigField
# GV System Wide 
# GV from wtforms           import TextField
from wtforms                import TextAreaField
from wtforms                import IntegerField
from wtforms                import DecimalField
from wtforms                import DateTimeField
from wtforms                import BooleanField
from wtforms                import SelectField
from wtforms                import SubmitField
from wtforms                import RadioField
from wtforms_components     import TimeField
#if wtforms.__version__ < "3.0.0":
#    from wtforms.fields.html5   import DateField
#else:
#    from wtforms.fields     import DateField
from wtforms.fields         import DateField
from wtforms.validators     import DataRequired as Required
from wtforms.validators     import AnyOf, DataRequired, Email
from wtforms.validators     import EqualTo, HostnameValidation
from wtforms.validators     import IPAddress, InputRequired, Length
from wtforms.validators     import MacAddress, NoneOf, NumberRange
from wtforms.validators     import Optional
from wtforms.validators     import Regexp
# ----------------------------------------------------------------------

