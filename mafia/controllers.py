# -*- coding: utf-8 -*-
"""This module contains the controller classes of the application."""

# symbols which are imported by "from mafia.controllers import *"
__all__ = ['Root']

# standard library imports
# import logging
import datetime

# third-party imports
from cherrypy import request
from turbogears import controllers, expose, flash, identity, redirect, visit

# project specific imports
# from mafia import model
# from mafia import json


# log = logging.getLogger("mafia.controllers")


class Root(controllers.RootController):
    """The root controller of the application."""

    @expose(template="mafia.templates.welcome")
    # @identity.require(identity.in_group("admin"))
    def index(self):
        """"Show the welcome page."""
        # log.debug("Happy TurboGears Controller Responding For Duty")
        return dict(now=datetime.datetime.now())

    @expose(template="mafia.templates.forums")
    def forums(self):
        return dict()

    @expose(template="mafia.templates.rules")
    def rules(self):
	return dict()

    @expose(template="mafia.templates.archives")
    def archives(self):
        return dict()

    @expose(template="mafia.templates.create_account")
    def create_account(self, message=None):
        if message:
            return dict(msg=message)
        return dict()

    def save_account(self, args):
        redirect("/")

    @expose(template="mafia.templates.create_game")
    def create_game(self):
        return dict()

    @expose(template="mafia.templates.contact")
    def contact(self):
        return dict()

    @expose(template="mafia.templates.login")
    def login(self, forward_url=None, *args, **kw):
        """Show the login form or forward user to previously requested page."""

        if forward_url:
            if isinstance(forward_url, list):
                forward_url = forward_url.pop(0)
            else:
                del request.params['forward_url']

        new_visit = visit.current()
        if new_visit:
            new_visit = new_visit.is_new

        if (not new_visit and not identity.current.anonymous
                and identity.was_login_attempted()
                and not identity.get_identity_errors()):
            redirect(forward_url or '/', kw)

        if identity.was_login_attempted():
            if new_visit:
                msg = _(u"Cannot log in because your browser "
                         "does not support session cookies.")
            else:
                msg = _(u"The credentials you supplied were not correct or "
                         "did not grant access to this resource.")
        elif identity.get_identity_errors():
            msg = _(u"You must provide your credentials before accessing "
                     "this resource.")
        else:
            msg = _(u"Please log in.")
            if not forward_url:
                forward_url = request.headers.get("Referer", "/")

        # we do not set the response status here anymore since it
        # is now handled in the identity exception.
        return dict(logging_in=True, message=msg,
            forward_url=forward_url, previous_url=request.path_info,
            original_parameters=request.params)

    @expose()
    def logout(self):
        """Log out the current identity and redirect to start page."""
        identity.current.logout()
        redirect("/")
