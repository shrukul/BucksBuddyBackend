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
from models import UserForm
from models import UpdateBalanceForm

from settings import WEB_CLIENT_ID
from settings import ANDROID_CLIENT_ID
from settings import IOS_CLIENT_ID
from settings import ANDROID_AUDIENCE

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

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


@endpoints.api(name='bucksbuddy', version='v1', audiences=[ANDROID_AUDIENCE],
    allowed_client_ids=[WEB_CLIENT_ID, API_EXPLORER_CLIENT_ID, ANDROID_CLIENT_ID, IOS_CLIENT_ID],
    scopes=[EMAIL_SCOPE])
class BucksBuddyApi(remote.Service):
    """BucksBuddy API v0.1"""

    """ """
    @endpoints.method(UserForm, BooleanMessage,
            path='registerUser',
            http_method='POST', name='registerUser')
    def registerUser(self, request):    
        p_key=ndb.Key(UserDetails,request.phoneNumber)
        user = UserDetails(
            key=p_key,
            displayName=request.displayName,
            mainEmail=request.mainEmail,
            balance=request.balance,
            phoneNumber=request.phoneNumber,
            )
        user.put()  
        return BooleanMessage(data=True)

    @endpoints.method(UpdateBalanceForm, BooleanMessage,
            path='updateBalance',
            http_method='POST', name='updateBalance')
    def updateBalance(self,request):
        p_key=ndb.Key(UserDetails,request.phoneNumber)
        result = p_key.get()
        if request.increment == 1 :
            setattr(result,balance,result.balance + request.updateAmount)
            result.put()
        elif request.increment == 0:
            if result.balance >= request.updateAmount:
                setattr(result,balance,result.balance - request.updateAmount)
                result.put()
            else:
                return BooleanMessage(data=False)
        return BooleanMessage(data=True)



api = endpoints.api_server([BucksBuddyApi]) # register API
