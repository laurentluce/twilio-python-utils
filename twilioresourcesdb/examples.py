import resources
import time

if __name__ == '__main__':
  # settings
  settings = {}
  # Twilio account
  settings['account_sid'] = 'ACa8e1bcd8948d695aa731bcc128b772dd'
  settings['account_token'] = 'cd88c470c893f3db8d727f1eca6dba63'
  # DB
  settings['database_type'] = 'mysql'
  settings['database_user'] = 'root'
  settings['database_password'] = 'belize09'
  settings['database_host'] = 'localhost'
  settings['database_port'] = '3306'
  settings['database_name'] = 'twilio'
  # Resources options
  settings['recording_path'] = '/home/laurent/github/twilio-python-utils/twilioresourcesdb/recordings/'
  settings['recording_format'] = 'wav'

  # instantiate resources object
  r = resources.Resources(settings)

  # start process loop to download resources from server continously
  r.start()

  while True:
    try:
      time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
      r.stop = True
      r.join()
      break

