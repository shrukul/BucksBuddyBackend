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


class UserDetails(ndb.Model):
    displayName = ndb.StringProperty()
    mainEmail = ndb.StringProperty()
    phoneNumber = ndb.StringProperty()
    balance = ndb.IntegerProperty()
    pin = ndb.IntegerProperty()
    uri = ndb.StringProperty()
    regid = ndb.StringProperty()

    @classmethod
    def GoogleLogin(cls, mainEmail, uri):
        return cls.query(ndb.AND(cls.mainEmail == mainEmail,cls.uri == uri))   

class MerchantDetails(ndb.Model):
    displayName = ndb.StringProperty()
    phoneNumber = ndb.StringProperty()
    balance = ndb.IntegerProperty()
    pin = ndb.IntegerProperty()


class ConflictException(endpoints.ServiceException):
    """ConflictException -- exception mapped to HTTP 409 response"""
    http_status = httplib.CONFLICT

class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    data = messages.StringField(1, required=True)

class BooleanMessage(messages.Message):
    """BooleanMessage-- outbound Boolean value message"""
    data = messages.BooleanField(1)


class UserForm(messages.Message):
    displayName = messages.StringField(1)
    mainEmail = messages.StringField(2)
    phoneNumber = messages.StringField(3)
    pin = messages.IntegerField(5)
    uri = messages.StringField(6)

class LoginForm(messages.Message):
    phoneNumber = messages.StringField(1)
    pin = messages.IntegerField(2)

class GoogleLoginForm(messages.Message):
    mainEmail = messages.StringField(1)
    uri = messages.StringField(2)
    displayName = messages.StringField(3)

class MerchantForm(messages.Message):
    displayName = messages.StringField(1)
    phoneNumber = messages.StringField(3)
    balance = messages.IntegerField(4)
    pin = messages.IntegerField(5)

class UpdateBalanceForm(messages.Message):
    phoneNumber = messages.StringField(1)
    updateAmount = messages.IntegerField(2)
    increment = messages.IntegerField(3)

class GetBalanceForm(messages.Message):
    phoneNumber = messages.StringField(1)

class TransferForm(messages.Message):
    sender = messages.StringField(1)
    receiver = messages.StringField(2)
    amount = messages.IntegerField(3)

class BillShareForm(messages.Message):
    sender = messages.StringField(1)
    receiver = messages.StringField(2)
    amount = messages.IntegerField(3)
    sender_pin = messages.IntegerField(4)

class BillPayForm(messages.Message):
    sender = messages.StringField(1)
    receiver = messages.StringField(2)
    amount = messages.IntegerField(3)
    sender_pin = messages.IntegerField(4)
    receiver_pin = messages.IntegerField(5)

class ProfileForm(messages.Message):
    displayName = messages.StringField(1)
    mainEmail = messages.StringField(2)
    phoneNumber = messages.StringField(3)
    balance = messages.IntegerField(4)
    success = messages.IntegerField(5)
    uri = messages.StringField(6)

class TransactionForm(messages.Message):
    displayName = messages.StringField(1)
    mainEmail = messages.StringField(2)
    phoneNumber = messages.StringField(3)
    balance = messages.IntegerField(4)
    success = messages.IntegerField(5)
    amount = messages.IntegerField(6)

class CreditForm(messages.Message):
    sender = messages.StringField(1)
    amount = messages.IntegerField(2)

class GCMForm(messages.Message):
    sender = messages.StringField(1)
    regid = messages.StringField(2)