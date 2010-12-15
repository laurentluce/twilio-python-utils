import sys, os
from email.utils import parsedate

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
    
  def __repr__(self):
    return "<sms_message('%s')>" % (self.sid)

class Resources:
  """
  Main class 
  """
  def __init__(self, settings):
    """
    Class instantiation

    @param settings dict of settings
    """
    # settings passed
    self.account_sid = settings['account_sid']
    self.account_token = settings['account_token']
    self.api_version = settings['api_version']
    self.database_type = settings['database_type']
    self.database_name = settings['database_name'] 
    self.database_user = settings['database_user'] 
    self.database_password = settings['database_password'] 
    self.database_host = settings['database_host']
    self.database_port = settings['database_port']
    self.engine = None
    self.metadata = None
    self.session = None
    # add list of resources to process
    self.list_resources = []
    resources = (('call', Call),
                 ('sms_message', SmsMessage), 
                 ('recording', Recording), 
                 ('transcription', Transcription), 
                 ('notification', Notification), 
                 ('conference', Conference), 
                 #('participant', Participant), 
                 ('account', Account)
                 )
    for t, c in resources:
      lr = dict(type=t, page=0, offset=0, pages=0, items=0, active={}, c=c)
      self.list_resources.append(lr)

    self.setup_connection()
    self.setup_tables()
    self.process()

  def setup_connection(self):
    """
    Create DB session
    """
    self.engine = create_engine('%s://%s:%s@%s:%s/%s' % (self.database_type, self.database_user, self.database_password, self.database_host, self.database_port, self.database_name))
    Session = sessionmaker(bind=self.engine)
    self.session = Session()
  
  def setup_tables(self):
    """
    Create tables if non existing, create relations between tables and mapping between
    tables and classes.
    """
    self.metadata = MetaData()
    
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
      Column('price', Integer),
      Column('direction', String(16)),
      Column('answeredBy', String(16)),
      Column('forwardedFrom', String(15)),
      Column('callerName', Text),
      Column('uri', Text)
    )
    
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
      Column('callId', Integer, ForeignKey('calls.id'))
    )
    rel = relationship(Call, backref=backref('recordings', order_by=id))
   
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
      Column('price', Integer),
      Column('uri', Text),
      Column('recordingId', Integer, ForeignKey('recordings.id'))
    )
    rel = relationship(Recording, backref=backref('transcriptions', order_by=id))

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
      Column('callId', Integer, ForeignKey('calls.id'))
    )
    rel = relationship(Call, backref=backref('notifications', order_by=id))

    conferences_table = Table('conferences', self.metadata,
      Column('id', Integer, primary_key=True),
      Column('sid', String(34), unique=True),
      Column('friendlyName', Text),
      Column('status', String(16)),
      Column('dateCreated', DateTime),
      Column('dateUpdated', DateTime),
      Column('accountSid', String(34)),
      Column('uri', Text)
    )

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
      Column('conferenceId', Integer, ForeignKey('conferences.id'))
    )
    rel = relationship(Call, backref=backref('participants', order_by=id))
    rel = relationship(Conference, backref=backref('participants', order_by=id))

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
      Column('price', Integer),
      Column('apiVersion', String(10)),
      Column('uri', Text)
    )

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

  def get_resource(self, resource_type, id):
    """
    Get resource from server

    @param resource_type type of resource: call, sms message...
    @param id resource sid: 34 bytes
    @return JSON representation
    """
    if resource_type == 'account':
      url = '/%s/Accounts/%s.json' % (settings.API_VERSION, id)
    elif resource_type == 'sms_message':
      url = '/%s/Accounts/%s/SMS/Messages/%s.json' % (settings.API_VERSION, self.account_sid, id)
    else:
      url = '/%s/Accounts/%s/%s/%s.json' % (settings.API_VERSION, self.account_sid, resource_type.capitalize() + 's', id)
    print url
    account = twilio.Account(self.account_sid, self.account_token)
    d = simplejson.loads(account.request(url, 'GET'))
    return d

  def get_resources_list(self, resource_type, page):
    """
    Get list of resources from server: calls, sms messages...

    @param resource_type type of resource: call, sms message...
    @return JSON representation
    """
    if resource_type == 'account':
      url = '/%s/Accounts.json' % settings.API_VERSION
    elif resource_type == 'sms_message':
      url = '/%s/Accounts/%s/SMS/Messages.json' % (settings.API_VERSION, self.account_sid)
    else:
      url = '/%s/Accounts/%s/%s.json?PageSize=50&Page=%d' % (settings.API_VERSION, self.account_sid, resource_type.capitalize() + 's', page)
    print url
    account = twilio.Account(self.account_sid, self.account_token)
    d = simplejson.loads(account.request(url, 'GET'))
    # test
    #d = self.testGetResource(resource_type)
    print 'page: %s' % d['page']
    print 'num_pages: %s' % d['num_pages']
    print 'next_page_uri: %s' % d['next_page_uri']
    return d

  def testGetResource(self, resource_type):
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
      recording['account_sid'] = 'ACda6f1e11047ebd6fe7a55f120be3a900'
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
      resource['account_sid'] = 'ACda6f1e11047ebd6fe7a55f120be3a900'
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
      resource['account_sid'] = 'ACda6f1e11047ebd6fe7a55f120be3a900'
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
      resource['account_sid'] = 'ACda6f1e11047ebd6fe7a55f120be3a900'
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
      resource['account_sid'] = 'ACda6f1e11047ebd6fe7a55f120be3a900'
      resource['muted'] = '0'
      resource['start_conference_on_enter'] = '0'
      resource['end_conference_on_exit'] = '0'
      resource['uri'] = ''
      d['participants'].append(resource)

  def process(self):
    """
    Main loop processing new resources and active ones to make sure
    we always have the latest resources data in the DB
    """
    while True:
      for lr in self.list_resources:
        # process active resources list
        self.process_active(lr)
        # check for new resources
        self.process_new(lr)
      break

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
      # if resource status done, add it to DB
      if not self.active_resource(lr['type'], res):
        # create object and add it
        self.add_object(lr, res)
      self.session.commit()

  def process_new(self, lr):
    """
    Process new resources and add them to DB if their status is done

    @param lr list resource to process
    """
    res = self.get_resources_list(lr['type'], lr['page'])
    # check if we have more items to process
    if res['total'] > lr['items']:
      while True:
        for r in res[lr['type']+'s'][lr['offset']:]:
          # process resources received
          # if active resource, add it to the active list
          # if not, add to DB
          if self.active_resource(lr['type'], r):
            lr['active'][r['sid']] = r
          else:
            self.add_object(lr, r)
        self.session.commit()
        # process next page if any
        if res['next_page_uri'] == None:
          lr['offset'] = res['end'] + 1
          lr['items'] = res['total']
          break
        else:
          lr['page'] += 1
          lr['offset'] = 0
          res = self.get_resources_list(lr['type'], lr['page'])


  def active_resource(self, resource_type, resource):
    """
    Is this resource active or finished?

    @param resource_type type of resource: call, sms...
    @return True if resource is active or False if not
    """
    if (resource_type in ('call', 'transcription', 'conference') and
        resource['status'] in ('queued', 'ringing', 'in-progress', 'init')):
        return True
    return False
    
  def add_object(self, lr, resource):
    """
    Add resource object to DB. Set relations.

    @param lr list resource
    @param resource resource JSON
    """
    # if object has a relation with another object, set it
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
    o = lr['c'](resource)
    self.session.add(o)

def convert_rfc822_to_mysql_datetime(str):
  d = parsedate(str)
  return '%d-%d-%d %02d:%02d:%02d' % (d[0], d[1], d[2], d[3], d[4], d[5])

