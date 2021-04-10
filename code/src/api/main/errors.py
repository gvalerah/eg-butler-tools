# ======================================================================
# Main Module: Error handling definitions
# Implements standard return codes error handlers
# source file name: __init__.py
# Static Header File. 
# GLVH 2020-10-11
# ----------------------------------------------------------------------
from flask  import render_template
from .      import main

""" Application decorators for routes """
""" Decorators specify main routes to be handled by Butler Solution """

@main.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

"""
# 7-6 Blueprint with error handlers
from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
"""
# ----------------------------------------------------------------------
