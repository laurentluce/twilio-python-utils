import sys, os
from email.utils import parsedate
from threading import Thread
import logging
import time

import simplejson
import twilio

from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, ForeignKey, create_engine, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapper, relationship, backref

class Call(object):
  """
  Call resource
  """
  def __init__(self, resource):
    """
    Class instantiation

    @param resource resource JSON attribute
    """
    self.sid = resource['sid']
    self.parentCallSid = resource['parent_call_sid']
    self.dateCreated = convert_rfc822_to_mysql_datetime(resource['date_created'])
    self.dateUpdated = convert_rfc822_to_mysql_datetime(resource['date_updated'])
    self.accountSid = resource['account_sid']
    self.to = resource['to']
    self.cfrom = resource['from']
    self.phoneNumberSid = resource['phone_number_sid']
    self.status = resource['status']
    self.startTime = convert_rfc822_to_mysql_datetime(resource['start_time'])
    self.endTime = convert_rfc822_to_mysql_datetime(resource['end_time'])
    self.duration = resource['duration']
    self.price = resource['price']
    self.direction = resource['direction']
    self.answeredBy = resource['answered_by']
    self.forwardedFrom = resource['forwarded_from']
    self.callerName = resource['caller_name']
    self.uri = resource['uri']
    self.accountId = resource['account_id']
    
  def __repr__(self):
    return "<call('%s')>" % (self.sid)

class Recording(object):
  """
  Recording resource
  """
  def __init__(self, resource):
    """
    Class instantiation

    @param resource resource JSON attribute
    """
    self.sid = resource['sid']
    self.dateCreated = convert_rfc822_to_mysql_datetime(resource['date_created'])
    self.dateUpdated = convert_rfc822_to_mysql_datetime(resource['date_updated'])
    self.accountSid = resource['account_sid']
    self.callSid = resource['call_sid']
    self.duration = resource['duration']
    self.apiVersion = resource['api_version']
    self.uri = resource['uri']
    self.callId = resource['call_id']
    self.accountId = resource['account_id']
    
  def __repr__(self):
    return "<recording('%s')>" % (self.sid)

class Transcription(object):
  """
  Transcription resource
  """
  def __init__(self, resource):
    """
    Class instantiation

    @param resource resource JSON attribute
    """
    self.sid = resource['sid']
    self.dateCreated = convert_rfc822_to_mysql_datetime(resource['date_created'])
    self.dateUpdated = convert_rfc822_to_mysql_datetime(resource['date_updated'])
    self.accountSid = resource['account_sid']
    self.status = resource['status']
    self.recordingSid = resource['recording_sid']
    self.duration = resource['duration']
    self.transcriptionText = resource['transcription_text']
    self.price = resource['price']
    self.uri = resource['uri']
    self.recordingId = resource['recording_id']
    self.accountId = resource['account_id']
    
  def __repr__(self):
    return "<transcription('%s')>" % (self.sid)

class Notification(object):
  """
  Notification resource
  """
  def __init__(self, resource):
    """
    Class instantiation

    @param resource resource JSON attribute
    """
    self.sid = resource['sid']
    self.dateCreated = convert_rfc822_to_mysql_datetime(resource['date_created'])
    self.dateUpdated = convert_rfc822_to_mysql_datetime(resource['date_updated'])
    self.accountSid = resource['account_sid']
    self.callSid = resource['call_sid']
    self.apiVersion = resource['api_version']
    self.log = resource['log']
    self.errorCode = resource['error_code']
    self.moreInfo = resource['more_info']
    self.messageText = resource['message_text']
    self.messageDate = convert_rfc822_to_mysql_datetime(resource['message_date'])
    self.requestUrl = resource['request_url']
    self.requestMethod = resource['request_method']
    self.requestVariables = resource['request_variables']
    self.responseHeaders = resource['response_headers']
    self.responseBody = resource['response_body']
    self.uri = resource['uri']
    self.callId = resource['call_id']
    self.accountId = resource['account_id']
    
  def __repr__(self):
    return "<notification('%s')>" % (self.sid)

class Conference(object):
  """
  Conference resource
  """
  def __init__(self, resource):
    """
    Class instantiation

    @param resource resource JSON attribute
    """
    self.sid = resource['sid']
    self.friendlyName = resource['friendly_name']
    self.status = resource['status']
    self.dateCreated = convert_rfc822_to_mysql_datetime(resource['date_created'])
    self.dateUpdated = convert_rfc822_to_mysql_datetime(resource['date_updated'])
    self.accountSid = resource['account_sid']
    self.uri = resource['uri']
    self.accountId = resource['account_id']
    
  def __repr__(self):
    return "<conference('%s')>" % (self.sid)

class Participant(object):
  """
  Participant resource
  """
  def __init__(self, resource):
    """
    Class instantiation

    @param resource resource JSON attribute
    """
    self.callSid = resource['call_sid']
    self.conferenceSid = resource['conference_sid']
    self.dateCreated = convert_rfc822_to_mysql_datetime(resource['date_created'])
    self.dateUpdated = convert_rfc822_to_mysql_datetime(resource['date_updated'])
    self.accountSid = resource['account_sid']
    self.muted = resource['muted']
    self.startConferenceOnEnter = resource['start_conference_on_enter']
    self.endConferenceOnExit = resource['start_conference_on_exit']
    self.uri = resource['uri']
    self.callId = resource['call_id']
    self.conferenceId = resource['conference_id']
    self.accountId = resource['account_id']
    
  def __repr__(self):
    return "<participant('%s')>" % (self.sid)

class Account(object):
  """
  Account resource
  """
  def __init__(self, resource):
    """
    Class instantiation

    @param resource resource JSON attribute
    """
    self.sid = resource['sid']
    self.dateCreated = convert_rfc822_to_mysql_datetime(resource['date_created'])
    self.dateUpdated = convert_rfc822_to_mysql_datetime(resource['date_updated'])
    self.friendlyName = resource['friendly_name']
    self.status = resource['status']
    self.authToken = resource['auth_token']
    self.uri = resource['uri']
    
  def __repr__(self):
    return "<account('%s')>" % (self.sid)

class SmsMessage(object):
  """
  Sms message resource
  """
  def __init__(self, resource):
    """
    Class instantiation

    @param resource resource JSON attribute
    """
    self.sid = resource['sid']
    self.dateCreated = convert_rfc822_to_mysql_datetime(resource['date_created'])
    self.dateUpdated = convert_rfc822_to_mysql_datetime(resource['date_updated'])
    self.dateSent = convert_rfc822_to_mysql_datetime(resource['date_sent'])
    self.accountSid = resource['account_sid']
    self.cfrom = resource['from']
    self.to = resource['to']
    self.body = resource['body']
    self.status = resource['status']
    self.direction = resource['direction']
    self.price = resource['price']
    self.apiVersion = resource['api_version']
    self.uri = resource['uri']
    self.accountId = resource['account_id']
    
  def __repr__(self):
    return "<sms_message('%s')>" % (self.sid)

class OutgoingCallerId(object):
  """
  Outgoing caller ID
  """
  def __init__(self, resource):
    """
    Class instantiation

    @param resource resource JSON attribute
    """
    self.sid = resource['sid']
    self.dateCreated = convert_rfc822_to_mysql_datetime(resource['date_created'])
    self.dateUpdated = convert_rfc822_to_mysql_datetime(resource['date_updated'])
    self.friendlyName = resource['friendly_name']
    self.accountSid = resource['account_sid']
    self.phoneNumber = resource['phone_number']
    self.uri = resource['uri']
    self.accountId = resource['account_id']
    
  def __repr__(self):
    return "<outgoing_caller_id('%s')>" % (self.sid)

class IncomingPhoneNumber(object):
  """
  Call resource
  """
  def __init__(self, resource):
    """
    Class instantiation

    @param resource resource JSON attribute
    """
    self.sid = resource['sid']
    self.dateCreated = convert_rfc822_to_mysql_datetime(resource['date_created'])
    self.dateUpdated = convert_rfc822_to_mysql_datetime(resource['date_updated'])
    self.friendlyName = resource['friendly_name']
    self.accountSid = resource['account_sid']
    self.phoneNumber = resource['phone_number']
    self.apiVersion = resource['api_version']
    self.voiceCallerIdLookup = resource['voice_caller_id_lookup']
    self.voiceUrl = resource['voice_url']
    self.voiceMethod = resource['voice_method']
    self.voiceFallbackUrl = resource['voice_fallback_url']
    self.voiceFallbackMethod = resource['voice_fallback_method']
    self.statusCallback = resource['status_callback']
    self.statusCallbackMethod = resource['status_callback_method']
    self.smsUrl = resource['sms_url']
    self.smsMethod = resource['sms_method']
    self.smsFallbackUrl = resource['sms_fallback_url']
    self.smsFallbackMethod = resource['sms_fallback_method']
    self.uri = resource['uri']
    self.accountId = resource['account_id']
    
  def __repr__(self):
    return "<incoming_phone_number('%s')>" % (self.sid)


class Resources(Thread):
  """
  Main class 
  """
  def __init__(self, settings):
    """
    Class instantiation

    @param settings dict of settings
    """
    Thread.__init__(self)
    # settings passed
    if not 'account_sid' in settings:
      raise TwilioException("Twilio account SID is required")
    if not 'account_token' in settings:
      raise TwilioException("Twilio account token is required")
    self.account_sid = settings['account_sid']
    self.account_token = settings['account_token']
    self.api_version = '2010-04-01'
    if not 'database_type' in settings:
      raise TwilioException("Database type is required")
    self.database_type = settings['database_type']
    if not 'database_name' in settings:
      raise TwilioException("Database name is required")
    self.database_name = settings['database_name'] 
    if not 'database_user' in settings:
      self.database_user = 'root'
    else:
      self.database_user = settings['database_user'] 
    if not 'database_password' in settings:
      raise TwilioException("Database user password is required")
    self.database_password = settings['database_password']
    if not 'database_host' in settings:
      self.database_host = 'localhost'
    else:
      self.database_host = settings['database_host']
    if not 'database_port' in settings:
      self.database_port = 3306
    else:
      self.database_port = settings['database_port']
    if not 'download_recordings' in settings:
      self.download_recordings = False
    else:
      self.download_recordings = settings['download_recordings']
    if self.download_recordings:
      self.recording_format = settings['recording_format']
      self.recording_path = settings['recording_path']
      if not os.path.exists(self.recording_path):
        os.mkdir(self.recording_path)
    if not 'page_size' in settings:
      self.page_size = 50
    else:
      self.page_size = settings['page_size']
    if not 'check_frequency' in settings:
      self.check_frequency = 5
    else:
      self.check_frequency = settings['check_frequency']
    self.engine = None
    self.metadata = None
    self.session = None
    self.stop = False
    self.dbg_level = 2
    # add list of resources to process
    self.list_resources = []
    resources = (('account', Account),
                 ('call', Call),
                 ('sms_message', SmsMessage), 
                 ('recording', Recording), 
                 ('transcription', Transcription), 
                 ('notification', Notification), 
                 ('conference', Conference), 
                 #('participant', Participant), 
                 ('outgoing_caller_id', OutgoingCallerId),
                 ('incoming_phone_number', IncomingPhoneNumber) 
                 )
    for t, c in resources:
      lr = dict(type=t, items=0, active={}, cls=c)
      self.list_resources.append(lr)

    self.setup_connection()
    self.setup_tables()

  def run(self):
    """
    Start main process loop
    """
    self.process(loop=True)

  def setup_connection(self):
    """
    Create DB session
    """
    self.engine = create_engine('%s://%s:%s@%s:%d/%s' % (self.database_type, self.database_user, self.database_password, self.database_host, self.database_port, self.database_name))
    Session = sessionmaker(bind=self.engine)
    self.session = Session()
  
  def setup_tables(self):
    """
    Create tables if non existing, create relations between tables and mapping between
    tables and classes.
    """
    self.metadata = MetaData()
   
    # Calls table
    calls_table = Table('calls', self.metadata,
      Column('id', Integer, primary_key=True),
      Column('sid', String(34), unique=True),
      Column('parentCallSid', String(34)),
      Column('dateCreated', DateTime),
      Column('dateUpdated', DateTime),
      Column('accountSid', String(34)),
      Column('to', String(15)),
      Column('cfrom', String(15)),
      Column('phoneNumberSid', String(34)),
      Column('status', String(16)),
      Column('startTime', DateTime),
      Column('endTime', DateTime),
      Column('duration', Integer),
      Column('price', String(16)),
      Column('direction', String(16)),
      Column('answeredBy', String(16)),
      Column('forwardedFrom', String(15)),
      Column('callerName', Text),
      Column('uri', Text),
      Column('accountId', Integer, ForeignKey('accounts.id'))
    )
    rel = relationship(Account, backref=backref('calls', order_by=id))
    
    # Recordings table
    recordings_table = Table('recordings', self.metadata,
      Column('id', Integer, primary_key=True),
      Column('sid', String(34), unique=True),
      Column('dateCreated', DateTime),
      Column('dateUpdated', DateTime),
      Column('accountSid', String(34)),
      Column('callSid', String(34)),
      Column('duration', Integer),
      Column('apiVersion', String(10)),
      Column('uri', Text),
      Column('callId', Integer, ForeignKey('calls.id')),
      Column('accountId', Integer, ForeignKey('accounts.id'))
    )
    rel = relationship(Call, backref=backref('recordings', order_by=id))
    rel = relationship(Account, backref=backref('recordings', order_by=id))
  
    # Transcription table
    transcriptions_table = Table('transcriptions', self.metadata,
      Column('id', Integer, primary_key=True),
      Column('sid', String(34), unique=True),
      Column('dateCreated', DateTime),
      Column('dateUpdated', DateTime),
      Column('accountSid', String(34)),
      Column('status', String(16)),
      Column('recordingSid', String(34)),
      Column('duration', Integer),
      Column('transcriptionText', Text),
      Column('price', String(16)),
      Column('uri', Text),
      Column('recordingId', Integer, ForeignKey('recordings.id')),
      Column('accountId', Integer, ForeignKey('accounts.id'))
    )
    rel = relationship(Recording, backref=backref('transcriptions', order_by=id))
    rel = relationship(Account, backref=backref('transcriptions', order_by=id))

    # Notifications table
    notifications_table = Table('notifications', self.metadata,
      Column('id', Integer, primary_key=True),
      Column('sid', String(34), unique=True),
      Column('dateCreated', DateTime),
      Column('dateUpdated', DateTime),
      Column('accountSid', String(34)),
      Column('callSid', String(34)),
      Column('apiVersion', String(10)),
      Column('log', Integer),
      Column('errorCode', Integer),
      Column('moreInfo', Text),
      Column('messageText', Text),
      Column('messageDate', DateTime),
      Column('requestMethod', String(16)),
      Column('requestVariables', Text),
      Column('requestHeaders', Text),
      Column('requestBody', Text),
      Column('uri', Text),
      Column('callId', Integer, ForeignKey('calls.id')),
      Column('accountId', Integer, ForeignKey('accounts.id'))
    )
    rel = relationship(Call, backref=backref('notifications', order_by=id))
    rel = relationship(Account, backref=backref('notifications', order_by=id))

    # Conferences table
    conferences_table = Table('conferences', self.metadata,
      Column('id', Integer, primary_key=True),
      Column('sid', String(34), unique=True),
      Column('friendlyName', Text),
      Column('status', String(16)),
      Column('dateCreated', DateTime),
      Column('dateUpdated', DateTime),
      Column('accountSid', String(34)),
      Column('uri', Text),
      Column('accountId', Integer, ForeignKey('accounts.id'))
    )
    rel = relationship(Account, backref=backref('conferences', order_by=id))

    # Participants table
    participants_table = Table('participants', self.metadata,
      Column('id', Integer, primary_key=True),
      Column('callSid', String(34)),
      Column('conferenceSid', String(34)),
      Column('dateCreated', DateTime),
      Column('dateUpdated', DateTime),
      Column('accountSid', String(34)),
      Column('muted', Boolean),
      Column('startConferenceOnEnter', Boolean),
      Column('endConferenceOnExit', Boolean),
      Column('uri', Text),
      Column('callId', Integer, ForeignKey('calls.id')),
      Column('conferenceId', Integer, ForeignKey('conferences.id')),
      Column('accountId', Integer, ForeignKey('accounts.id'))
    )
    rel = relationship(Call, backref=backref('participants', order_by=id))
    rel = relationship(Conference, backref=backref('participants', order_by=id))
    rel = relationship(Account, backref=backref('participants', order_by=id))

    # Accounts table
    accounts_table = Table('accounts', self.metadata,
      Column('id', Integer, primary_key=True),
      Column('sid', String(34)),
      Column('dateCreated', DateTime),
      Column('dateUpdated', DateTime),
      Column('friendlyName', String(34)),
      Column('status', String(16)),
      Column('authToken', String(34)),
      Column('uri', Text),
    )
  
    # SMS messages table
    sms_messages_table = Table('sms_messages', self.metadata,
      Column('id', Integer, primary_key=True),
      Column('sid', String(34), unique=True),
      Column('dateCreated', DateTime),
      Column('dateUpdated', DateTime),
      Column('dateSent', DateTime),
      Column('accountSid', String(34)),
      Column('cfrom', String(15)),
      Column('to', String(15)),
      Column('body', String(160)),
      Column('status', String(16)),
      Column('direction', String(16)),
      Column('price', String(16)),
      Column('apiVersion', String(10)),
      Column('uri', Text),
      Column('accountId', Integer, ForeignKey('accounts.id'))
    )
    rel = relationship(Account, backref=backref('sms_messages', order_by=id))

    # Outgoing caller IDs table
    outgoing_caller_ids_table = Table('outgoing_caller_ids', self.metadata,
      Column('id', Integer, primary_key=True),
      Column('sid', String(34), unique=True),
      Column('dateCreated', DateTime),
      Column('dateUpdated', DateTime),
      Column('friendlyName', Text),
      Column('phoneNumber', String(15)),
      Column('accountSid', String(34)),
      Column('uri', Text),
      Column('accountId', Integer, ForeignKey('accounts.id'))
    )
    rel = relationship(Account, backref=backref('outgoing_caller_ids', order_by=id))

    # Incoming phone numbers table
    incoming_phone_numbers_table = Table('incoming_phone_numbers', self.metadata,
      Column('id', Integer, primary_key=True),
      Column('sid', String(34), unique=True),
      Column('dateCreated', DateTime),
      Column('dateUpdated', DateTime),
      Column('friendlyName', Text),
      Column('accountSid', String(34)),
      Column('phoneNumber', String(15)),
      Column('apiVersion', String(10)),
      Column('voiceCallerIdLookup', Boolean),
      Column('voiceUrl', Text),
      Column('voiceMethod', String(16)),
      Column('voiceFallbackUrl', Text),
      Column('voiceFallbackMethod', String(16)),
      Column('statusCallback', Text),
      Column('statusCallbackMethod', String(16)),
      Column('smsUrl', Text),
      Column('smsMethod', String(16)),
      Column('smsFallbackUrl', Text),
      Column('smsFallbackMethod', String(16)),
      Column('uri', Text),
      Column('accountId', Integer, ForeignKey('accounts.id'))
    )
    rel = relationship(Account, backref=backref('incoming_phone_numbers', order_by=id))

    # create tables: ok to call multiple times
    self.metadata.create_all(self.engine)

    # mapping between tables and classes
    mapper(Call, calls_table)
    mapper(Recording, recordings_table)
    mapper(Transcription, transcriptions_table)
    mapper(Notification, notifications_table)
    mapper(Conference, conferences_table)
    mapper(Participant, participants_table)
    mapper(Account, accounts_table)
    mapper(SmsMessage, sms_messages_table)
    mapper(OutgoingCallerId, outgoing_caller_ids_table)
    mapper(IncomingPhoneNumber, incoming_phone_numbers_table)

  def get_resource(self, resource_type, id):
    """
    Get resource from server

    @param resource_type type of resource: call, sms message...
    @param id resource sid: 34 bytes
    @return JSON representation
    """
    if resource_type == 'account':
      url = '/%s/Accounts/%s.json' % (self.api_version, id)
    elif resource_type == 'sms_message':
      url = '/%s/Accounts/%s/SMS/Messages/%s.json' % (self.api_version, self.account_sid, id)
    elif resource_type == 'recording':
      url = '/%s/Accounts/%s/%s/%s' % (self.api_version, self.account_sid, self.format_url_resource_name(resource_type) + 's', id)
    else:
      url = '/%s/Accounts/%s/%s/%s.json' % (self.api_version, self.account_sid, self.format_url_resource_name(resource_type) + 's', id)
    self.debug(url, 2)
    account = twilio.Account(self.account_sid, self.account_token)
    try:
      d = simplejson.loads(account.request(url, 'GET'))
      return d
    except Exception, e:
      self.debug(e, 1)
      return None

  def get_resources_list(self, resource_type, page):
    """
    Get list of resources from server: calls, sms messages...

    @param resource_type type of resource: call, sms message...
    @return JSON representation
    """
    if resource_type == 'account':
      url = '/%s/Accounts.json' % self.api_version
    elif resource_type == 'sms_message':
      url = '/%s/Accounts/%s/SMS/Messages.json?PageSize=%d&Page=%d' % (self.api_version, self.account_sid, self.page_size, page)
    else:
      url = '/%s/Accounts/%s/%s.json?PageSize=%d&Page=%d' % (self.api_version, self.account_sid, self.format_url_resource_name(resource_type) + 's', self.page_size, page)
    self.debug(url, 2)
    account = twilio.Account(self.account_sid, self.account_token)
    try:
      d = simplejson.loads(account.request(url, 'GET'))
      d = self.test_get_resource(resource_type, d)
      return d
    except Exception, e:
      self.debug(e, 1)
      return None

  def test_get_resource(self, resource_type, d):
    """
    Testing different resources by filling them up manually instead of getting them
    from the server
    """
    if resource_type == 'recording':
      d['total'] = 1
      d['num_pages'] = 1
      d['recordings'] = []
      recording = {}
      recording['sid'] = 'REda6f1e11047ebd6fe7a55f120be3a900'
      recording['account_sid'] = 'ACa8e1bcd8948d695aa731bcc128b772dd'
      recording['api_version'] = '2010-01-01'
      recording['call_sid'] = 'CA73ac207638841f3ab868f95b4d201c02'
      recording['date_created'] = 'Fri, 17 Jul 2009 01:52:49 +0000'
      recording['date_updated'] = 'Fri, 17 Jul 2009 01:52:49 +0000'
      recording['duration'] = '1'
      recording['uri'] = ''
      d['recordings'].append(recording)
    elif resource_type == 'transcription':
      d['total'] = 1
      d['num_pages'] = 1
      d['transcriptions'] = []
      resource = {}
      resource['sid'] = 'ACda6f1e11047ebd6fe7a55f120be3a900'
      resource['account_sid'] = 'ACa8e1bcd8948d695aa731bcc128b772dd'
      resource['status'] = 'completed'
      resource['recording_sid'] = 'REda6f1e11047ebd6fe7a55f120be3a900'
      resource['date_created'] = 'Fri, 17 Jul 2009 01:52:49 +0000'
      resource['date_updated'] = 'Fri, 17 Jul 2009 01:52:49 +0000'
      resource['duration'] = '1'
      resource['transcription_text'] = 'bla bla'
      resource['price'] = '1'
      resource['uri'] = ''
      d['transcriptions'].append(resource)
    elif resource_type == 'notification':
      d['total'] = 1
      d['num_pages'] = 1
      d['notifications'] = []
      resource = {}
      resource['sid'] = 'ACda6f1e11047ebd6fe7a55f120be3a900'
      resource['account_sid'] = 'ACa8e1bcd8948d695aa731bcc128b772dd'
      resource['status'] = 'completed'
      resource['call_sid'] = 'CA97f95df0c70ab2fdbc379b457fa6fbfc'
      resource['date_created'] = 'Fri, 17 Jul 2009 01:52:49 +0000'
      resource['date_updated'] = 'Fri, 17 Jul 2009 01:52:49 +0000'
      resource['api_version'] = '2010-01-01'
      resource['log'] = '1'
      resource['error_code'] = '1'
      resource['more_info'] = ''
      resource['message_text'] = ''
      resource['message_date'] = 'Fri, 17 Jul 2009 01:52:49 +0000'
      resource['request_url'] = ''
      resource['request_method'] = ''
      resource['request_variables'] = ''
      resource['response_headers'] = ''
      resource['response_body'] = ''
      resource['uri'] = ''
      d['notifications'].append(resource)
    elif resource_type == 'conference':
      d['total'] = 1
      d['num_pages'] = 1
      d['conferences'] = []
      resource = {}
      resource['sid'] = 'CFda6f1e11047ebd6fe7a55f120be3a900'
      resource['friendly_name'] = ''
      resource['status'] = 'completed'
      resource['date_created'] = 'Fri, 17 Jul 2009 01:52:49 +0000'
      resource['date_updated'] = 'Fri, 17 Jul 2009 01:52:49 +0000'
      resource['account_sid'] = 'ACa8e1bcd8948d695aa731bcc128b772dd'
      resource['uri'] = ''
      d['conferences'].append(resource)
    elif resource_type == 'participant':
      d['total'] = 1
      d['num_pages'] = 1
      d['participants'] = []
      resource = {}
      resource['call_sid'] = 'CA97f95df0c70ab2fdbc379b457fa6fbfc'
      resource['conference_sid'] = 'CFda6f1e11047ebd6fe7a55f120be3a900'
      resource['date_created'] = 'Fri, 17 Jul 2009 01:52:49 +0000'
      resource['date_updated'] = 'Fri, 17 Jul 2009 01:52:49 +0000'
      resource['account_sid'] = 'ACa8e1bcd8948d695aa731bcc128b772dd'
      resource['muted'] = '0'
      resource['start_conference_on_enter'] = '0'
      resource['end_conference_on_exit'] = '0'
      resource['uri'] = ''
      d['participants'].append(resource)
    return d

  def process(self, loop):
    """
    Main loop processing new resources and active ones to make sure
    we always have the latest resources data in the DB

    @param loop loop or not
    """
    while not self.stop:
      for lr in self.list_resources:
        # process active resources list
        self.process_active(lr)
        # check for new resources
        self.process_new(lr)
      if not loop:
        break
      time.sleep(self.check_frequency)

  def process_active(self, lr):
    """
    Process active resources like active calls to always have the latest resources
    data in the DB. We don't add the resource until it is in an end state like
    'completed'.

    @param lr list resource to process
    """
    for key, res in lr['active'].items():
      # get resource from server and check for completion
      res = self.get_resource(lr['type'], res['sid'])
      if res:
        # if resource status done, add it to DB
        if not self.active_resource(lr['type'], res):
          self.debug('%s: %s completed - add it to DB' % (lr['type'], res['sid']), 1)
          # create object and add it
          self.add_resource(lr, res)
          del lr['active'][key]
    self.session.commit()

  def process_new(self, lr):
    """
    Process new resources and add them to DB if their status is done

    @param lr list resource to process
    """
    page = 0
    res = self.get_resources_list(lr['type'], page)
    # check if we have more items to process
    if res and res['total'] > lr['items']:
      count = res['total'] - lr['items']
      self.debug('processing %d new %ss' % (count, lr['type']), 1)
      items = 0
      while True:
        sitems = 0
        if res:
          for r in res[lr['type']+'s']:
            print r
            # process resources received
            # if active resource, add it to the active list
            # if not, add to DB
            if self.active_resource(lr['type'], r):
              if r['sid'] in lr['active']:
                break
              self.debug('add %s - %s to active list - will add it to DB when completed' % (lr['type'], r['sid']), 1)
              lr['active'][r['sid']] = r
            else:
              if self.add_resource(lr, r) == False:
                break
            items += 1
            sitems += 1
          self.session.commit()
          self.debug('%d / %d' % (items, count), 1)
          # process resources dependencies
          self.process_resources_dependencies(lr, res[lr['type']+'s'][:sitems])
          # process next page if any
          if res['next_page_uri'] == None:
            lr['items'] += count
            self.debug('save items: %d' % (lr['items']), 2)
            break
          else:
            self.debug('get next page', 2)
            page += 1
            res = self.get_resources_list(lr['type'], page)


  def active_resource(self, resource_type, resource):
    """
    Is this resource active or completed?

    @param resource_type type of resource: call, sms...
    @return True if resource is active or False if not
    """
    if (resource_type in ('call', 'transcription', 'conference', 'sms_message') and
        resource['status'] in ('queued', 'ringing', 'in-progress', 'init', 'sending')):
        return True
    return False
    
  def add_resource(self, lr, resource):
    """
    Add resource object to DB. Set relations.

    @param lr list resource
    @param resource resource JSON
    """
    # check if resource is in DB
    if self.resource_exists(lr, resource):
      return False
    # if object has a relation with another object, set it
    if lr['type'] != 'account':
      # get account id
      account = self.session.query(Account).filter_by(sid=resource['account_sid'])[0]
      resource['account_id'] = account.id
    if lr['type'] in ('recording', 'notification'):
      # get call id
      call = self.session.query(Call).filter_by(sid=resource['call_sid'])[0]
      resource['call_id'] = call.id
    elif lr['type'] == 'transcription':
      # get recording id
      recording = self.session.query(Recording).filter_by(sid=resource['recording_sid'])[0]
      resource['recording_id'] = recording.id
    elif lr['type'] == 'participant':
      # get call and conference id 
      call = self.session.query(Call).filter_by(sid=resource['call_sid'])[0]
      resource['call_id'] = call.id
      conference = self.session.query(Conference).filter_by(sid=resource['conference_sid'])[0]
      resource['conference_id'] = conference.id
    # create object and add it
    o = lr['cls'](resource)
    self.session.add(o)
    return True

  def resource_exists(self, lr, resource):
    """
    Check if a resource exists in the DB

    @param lr list resource
    @param resource JSON resource
    @return True if exists, False if not
    """
    if 'sid' in resource:
      if self.session.query(lr['cls']).filter_by(sid=resource['sid']).count():
        return True
    return False

  def process_resources_dependencies(self, lr, resources):
    """
    Process each resource dependencies

    Example: download recording file for each recording resource

    @param lr list resource
    @param resources resources JSON
    """
    if resources:
      if lr['type'] == 'recording' and self.download_recordings:
        self.debug('downloading %d recordings' % (len(resources)), 1)
        for res in resources:
          data = self.get_resource(lr['type'], res['sid'])
          if data:
            f = open(self.recording_path+'/'+res['sid'], 'w+')
            f.write(data)
            f.close


  def format_url_resource_name(self, name):
    """
    """
    s = ''.join(self.lower_camelcase(word if word else '_' for word in name.split('_')))
    self.debug(s, 2)
    return s

  def lower_camelcase(self, seq):
    """
    """
    it = iter(seq)
    #for word in it:
    #  yield word.lower()
    #  if word.isalnum(): break
    for word in it:
      yield word.capitalize()

  def debug(self, s, level):
    """
    """
    if self.dbg_level >= level:
      print s


def convert_rfc822_to_mysql_datetime(str):
  """
  """
  d = parsedate(str)
  return '%d-%d-%d %02d:%02d:%02d' % (d[0], d[1], d[2], d[3], d[4], d[5])

class TException(Exception): pass

