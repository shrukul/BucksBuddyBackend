#!/usr/bin/env python

"""models.py

BucksBuddy App-Engine Class file

$Id: models.py,v 1.1 2014/05/24 22:01:10 wesc Exp $

created on 2014 mar 09

"""

__author__ = 'shrukul99@gmail.com (Shrukul Habib)'

import httplib
import endpoints
from protorpc import messages
from google.appengine.ext import ndb

class ConflictException(endpoints.ServiceException):
    """ConflictException -- exception mapped to HTTP 409 response"""
    http_status = httplib.CONFLICT

class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    data = messages.StringField(1, required=True)

class BooleanMessage(messages.Message):
    """BooleanMessage-- outbound Boolean value message"""
    data = messages.BooleanField(1)

class UserDetails(ndb.Model):
    """ConferenceQueryForms -- multiple ConferenceQueryForm inbound form message"""
    displayName = ndb.StringProperty()
    mainEmail = ndb.StringProperty()
    phoneNumber = ndb.StringProperty()
    balance = ndb.IntegerProperty()

class UserForm(messages.Message):
    displayName = messages.StringField(1)
    mainEmail = messages.StringField(2)
    phoneNumber = messages.StringField(3)
    balance = messages.IntegerField(4)

class UpdateBalanceForm(messages.Message):
    phoneNumber = messages.StringField(1)
    updateAmount = messages.IntegerField(2)
    increment = messages.IntegerField(3)
