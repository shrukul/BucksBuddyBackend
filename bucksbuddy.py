#!/usr/bin/env python

"""
conference.py -- Udacity conference server-side Python App Engine API;
    uses Google Cloud Endpoints

$Id: conference.py,v 1.25 2014/05/24 23:42:19 wesc Exp wesc $

created by wesc on 2014 apr 21

"""

__author__ = 'shrukul99@gmail.com (Shrukul Habib)'


from datetime import datetime

import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

from google.appengine.api import memcache
from google.appengine.api import taskqueue
from google.appengine.ext import ndb

from models import ConflictException
from models import StringMessage
from models import BooleanMessage
from models import UserDetails
from models import MerchantDetails
from models import UserForm
from models import UpdateBalanceForm
from models import GetBalanceForm
from models import TransferForm
from models import BillShareForm
from models import MerchantForm
from models import BillPayForm
from models import LoginForm
from models import ProfileForm
from models import GoogleLoginForm
from models import TransactionForm
from models import CreditForm
from models import GCMForm

from settings import WEB_CLIENT_ID
from settings import ANDROID_CLIENT_ID
from settings import IOS_CLIENT_ID
from settings import ANDROID_AUDIENCE

import random
import json
import urllib2
import google.appengine.ext.db

EMAIL_SCOPE = endpoints.EMAIL_SCOPE
API_EXPLORER_CLIENT_ID = endpoints.API_EXPLORER_CLIENT_ID
MEMCACHE_ANNOUNCEMENTS_KEY = "RECENT_ANNOUNCEMENTS"
ANNOUNCEMENT_TPL = ('Last chance to attend! The following conferences '
                    'are nearly sold out: %s')
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

DEFAULTS = {
    "city": "Default City",
    "maxAttendees": 0,
    "seatsAvailable": 0,
    "topics": [ "Default", "Topic" ],
}

OPERATORS = {
            'EQ':   '=',
            'GT':   '>',
            'GTEQ': '>=',
            'LT':   '<',
            'LTEQ': '<=',
            'NE':   '!='
            }

FIELDS =    {
            'CITY': 'city',
            'TOPIC': 'topics',
            'MONTH': 'month',
            'MAX_ATTENDEES': 'maxAttendees',
            }

CONF_GET_REQUEST = endpoints.ResourceContainer(
    message_types.VoidMessage,
    websafeConferenceKey=messages.StringField(1),
)

CONF_POST_REQUEST = endpoints.ResourceContainer(
    UserForm,
    websafeConferenceKey=messages.StringField(1),
)

def SendGCM(regid, msg, msgType, balance):
        url = 'https://android.googleapis.com/gcm/send'
        data = json.dumps({ "registration_ids" : [""+ regid +""], "data" : { "message" : msg, "type" : msgType, "balance" : balance} })
        headers = {'Content-Type' : 'application/json', 'Authorization' : 'key=AIzaSyB4-yMAlsh874AGjTqAuQik7mCDRWjq5BU'}
        request = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(request)
        html = response.read()
        print html

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


@endpoints.api(name='bucksbuddy', version='v1', audiences=[ANDROID_AUDIENCE],
    allowed_client_ids=[WEB_CLIENT_ID, API_EXPLORER_CLIENT_ID, ANDROID_CLIENT_ID, IOS_CLIENT_ID],
    scopes=[EMAIL_SCOPE])
class BucksBuddyApi(remote.Service):
    """BucksBuddy API v0.1"""

    """ """
    @endpoints.method(UserForm, ProfileForm,
            path='registerUser',
            http_method='POST', name='registerUser')
    def registerUser(self, request):    
        p_key=ndb.Key(UserDetails,request.phoneNumber)
        succ = 1
        user = UserDetails(
            key=p_key,
            displayName=request.displayName,
            mainEmail=request.mainEmail,
            balance=0,
            phoneNumber=request.phoneNumber,
            pin=random.randint(999, 9999),
            uri=request.uri,
            )
        try:
            user.put()
        except datastore_errors.DuplicatePropertyError:
            succ = 0
        prof = ProfileForm()
        if succ == 1:
            prof.displayName = user.displayName
            prof.uri = user.uri
            prof.mainEmail = user.mainEmail
            prof.balance = user.balance
            prof.phoneNumber = user.phoneNumber
        prof.success = succ
        return prof


    @endpoints.method(LoginForm, ProfileForm,
            path='loginUser',
            http_method='POST', name='loginUser')
    def loginUser(self, request):    
        p_key = ndb.Key(UserDetails,request.phoneNumber)
        user = p_key.get()
        succ = 1
        if user is None:
            succ = 0
        elif user.pin != request.pin:
            succ = 2
        prof = ProfileForm()
        if succ == 1:
            prof.displayName = user.displayName
            prof.mainEmail = user.mainEmail
            prof.phoneNumber = user.phoneNumber
            prof.balance = user.balance
            prof.uri = user.uri
        prof.success = succ
        return prof

    @endpoints.method(GoogleLoginForm, ProfileForm,
            path='googleLoginUser',
            http_method='POST', name='googleLoginUser')
    def googleLoginUser(self, request):    
        qry = UserDetails.GoogleLogin(request.mainEmail,request.uri)
        succ = 1
        user = qry.get();
        prof = ProfileForm()
        if user is None:
            succ = 0
        elif succ == 1:
            prof.displayName = user.displayName
            prof.mainEmail = user.mainEmail
            prof.phoneNumber = user.phoneNumber
            prof.balance = user.balance
            prof.uri = user.uri
        prof.success = succ
        return prof


    @endpoints.method(MerchantForm, BooleanMessage,
            path='registerMerchant',
            http_method='POST', name='registerMerchant')
    def registerMerchant(self, request):    
        p_key=ndb.Key(MerchantDetails,request.displayName)
        merchant = MerchantDetails(
            key=p_key,
            displayName=request.displayName,
            balance=request.balance,
            phoneNumber=request.phoneNumber,
            pin=request.pin,
            )
        merchant.put()  
        return BooleanMessage(data=True)
            

    @endpoints.method(UpdateBalanceForm, BooleanMessage,
            path='updateBalance',
            http_method='POST', name='updateBalance')
    def updateBalance(self,request):
        p_key=ndb.Key(UserDetails,request.phoneNumber)
        result = p_key.get()
        if not result:
            return BooleanMessage(data=False)
        if request.increment == 1 :
            result.balance = result.balance + request.updateAmount
            result.put()
        elif request.increment == 0:
            if result.balance >= request.updateAmount:
                result.balance = result.balance - request.updateAmount
                result.put()
            else:
                return BooleanMessage(data=False)
        return BooleanMessage(data=True)

    @endpoints.method(GetBalanceForm, StringMessage,
            path='getBalance',
            http_method='POST', name='getBalance')
    def getBalance(self,request):
        p_key=ndb.Key(UserDetails,request.phoneNumber)
        result = p_key.get()
        if result:
            return StringMessage(data=str(result.balance))
        else:
            return StringMessage(data="Phone number does not exist")

    @endpoints.method(TransferForm, BooleanMessage,
            path='transferAmount',
            http_method='POST', name='transferAmount')
    def transferAmount(self,request):
        p_key=ndb.Key(UserDetails,request.sender)
        send = p_key.get()
        if not send:
            return BooleanMessage(data=False)
        if send.balance < request.amount:
            return BooleanMessage(data=False)

        p_key2=ndb.Key(UserDetails,request.receiver)
        recv = p_key2.get()
        if not recv:
            return BooleanMessage(data=False)

        send.balance = send.balance - request.amount
        send.put()
        recv.balance = recv.balance + request.amount
        recv.put()
        return BooleanMessage(data=True)

    @endpoints.method(BillShareForm, TransactionForm,
            path='billShare',
            http_method='POST', name='billShare')
    def billShare(self,request):
        p_key = ndb.Key(UserDetails,request.sender)
        send = p_key.get()
        succ = 1
        if not send:
            succ = 0
        elif send.pin != request.sender_pin:
            succ = 2
        if succ == 1 and send.balance < request.amount:
            succ = 3

        p_key2=ndb.Key(UserDetails,request.receiver)
        recv = p_key2.get()
        if not recv:
            succ = 4

        trans = TransactionForm()

        if succ == 1:
            trans.displayName = recv.displayName
            trans.mainEmail = recv.mainEmail
            trans.phoneNumber = recv.phoneNumber
            send.balance = send.balance - request.amount
            send.put()
            recv.balance = recv.balance + request.amount
            recv.put()
            trans.balance = send.balance
            trans.amount = request.amount
            SendGCM(send.regid,request.amount,-1,send.balance)
            SendGCM(recv.regid,request.amount,1,recv.balance)
        trans.success = succ
        return trans

    @endpoints.method(BillPayForm, TransactionForm,
            path='billPay',
            http_method='POST', name='billPay')
    def billPay(self,request):
        p_key = ndb.Key(UserDetails,request.sender)
        send = p_key.get()
        succ = 1
        if not send:
            succ = 0
        elif send.pin != request.sender_pin:
            succ = 2
        if succ == 1 and send.balance < request.amount:
            succ = 3

        p_key2=ndb.Key(MerchantDetails,request.receiver)
        recv = p_key2.get()
        if not recv:
            succ = 4
        if succ == 1 and recv.pin != request.receiver_pin:
            succ = 5

        trans = TransactionForm()

        if succ == 1:
            trans.displayName = recv.displayName
            trans.phoneNumber = recv.phoneNumber
            send.balance = send.balance - request.amount
            send.put()
            recv.balance = recv.balance + request.amount
            recv.put()
            trans.balance = send.balance
            trans.amount = request.amount
            SendGCM(send.regid,request.amount,-1,send.balance)
        trans.success = succ
        return trans

    @endpoints.method(CreditForm, TransactionForm,
            path='credit',
            http_method='POST', name='credit')
    def credit(self,request):
        p_key = ndb.Key(UserDetails,request.sender)
        send = p_key.get()
        succ = 1
        if not send:
            succ = 0

        trans = TransactionForm()

        if succ == 1:
            send.balance = send.balance + request.amount
            send.put()
            trans.balance = send.balance
            trans.amount = request.amount
            SendGCM(send.regid, request.amount, 1, send.balance)
        trans.success = succ
        return trans

    @endpoints.method(GCMForm, BooleanMessage,
            path='registerGCM',
            http_method='POST', name='registerGCM')
    def registerGCM(self,request):
        p_key = ndb.Key(UserDetails,request.sender)
        user = p_key.get()
        succ = 1
        if not user:
            succ = 0

        if succ == 1:
            user.regid = request.regid
            user.put()
        
        if(succ == 0):
            result = BooleanMessage(data=False)
        else:
            result = BooleanMessage(data=True)
        return result
    #TODO : GetField(field,input)
    #TODO : CheckLogin(phone_no,pin)   

    

api = endpoints.api_server([BucksBuddyApi]) # register APIni
