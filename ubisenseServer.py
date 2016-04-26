import time, datetime
import json
import random
import sys
import requests
import argparse
from thread import start_new_thread

allprevloc = ['', '', '', '']

def randomLocation():
    #Warteraum1
    #Warteraum2
    #Warteraum3
    #Warteraum4
    #Arbeitsstation1
    #Arbeitsstation2
    x = random.randint(0,9)
    if x == 0:
        return '"LOCATION" : "Warteraum1"'
    elif x == 1:
        return '"LOCATION" : "Warteraum2"'
    elif x == 2:
        return '"LOCATION" : "Warteraum3"'
    elif x == 3:
        return '"LOCATION" : "Warteraum4"'
    elif x == 4:
        return '"LOCATION" : "Arbeitsstation1"'
    elif x == 5:
        return '"LOCATION" : "Arbeitsstation2"'
    else:
        return '"LOCATION" : ""'

def specificLocation( location ):
    return '"LOCATION" : "' + location + '"'

def sender( tagname ):
    return '"SENDER_ID" : "' + tagname + '"'

def x():
    return "%.3f" % random.uniform(0.0, 10.0)

def y():
    return "%.3f" % random.uniform(0.0, 10.0)

def z():
    return "%.3f" % random.uniform(0.0, 10.0)

def coordinates():
    return '"X" : "' + x() + '", "Y" : "' + y() + '", "Z" : "' + z() + '"'

def tag_info( tagname , location = '', random = 0):
    if (random):
        return '{' + randomLocation() + ', ' + sender(tagname) + ', ' + coordinates() + ' }'
    else:
        return '{' + specificLocation(location) + ', ' + sender(tagname) + ', ' + coordinates() + ' }'

def it_carriers( location, random = 0):
    return '"IT_CARRIERS" : [ ' + tag_info("LTABAS", location, random) + "," + tag_info("LTPROALPHA", location, random) + "," + tag_info("LTASECCO", location, random) + "," + tag_info("LTRESERVE", location, random) + ']'

def sendJson( json_string , url , seconds):
    t_end = time.time() + seconds
    if (seconds < 0):
        #send once
        print json_string
        print "==========================="
        parsed_json = json.loads(json_string)
        data = json.dumps(parsed_json)
        response = requests.post(url, data=data)
        return

    while time.time() < t_end:
        #print json_string
        #print "==========================="
        sys.stdout.write('.')
        sys.stdout.flush()
        parsed_json = json.loads(json_string)
        data = json.dumps(parsed_json)
        # This is an sync call (a.k.a. blocking)
        #response = requests.post(url, data=data)
        # Asyn call using a threadwhile (1):
        start_new_thread(requests.post, (url, data))
        time.sleep(1.5)

# Sends the state for n seconds to the give url
def sendState( new_state, url, seconds ):
    json_string = '{"IF_DATE" : "' + datetime.datetime.now().isoformat() + '",' + it_carriers(new_state) + ' }'
    sendJson(json_string, url, seconds)

def complete_run( url ):
  x = random.randint(0,9) # random behavior
  #x = -1 # no random behavior
  sendState('', url, 3)
  sendState('Warteraum1', url, 5)
  #AS1 finished between x and y seconds
  sendState('Arbeitsstation1', url, random.randint(8,12))
  sendState('Warteraum2', url, 5)
  #Transport finished between x and y  seconds
  sendState('', url, random.randint(8,12))
  if (x == 5):
      #one in ten runs we break together here
      sys.stdout.write('X')
      sys.stdout.flush()
      return
  sendState('Warteraum3', url, 5)
  #AS2 finished between x and y seconds
  sendState('Arbeitsstation2', url, random.randint(13,17))
  if (x == 2):
        #one in ten runs we behave different
        #go back
        sendState('Warteraum3', url, 5)
        #go back again
        sendState('Warteraum2', url, 5)
        #go forward again
        sendState('Warteraum3', url, 5)
        #go forward again
        sendState('Arbeitsstation2', url, 5)
        #and continue normal
        sys.stdout.write('<')
        sys.stdout.flush()
  sendState('Warteraum4', url, 5)
  #now send 40 seconds '' location
  sendState('', url, 40)
  sys.stdout.write('O')
  sys.stdout.flush()

def random_run( url ):
    json_string = '{"IF_DATE" : "' + datetime.datetime.now().isoformat() + '",' + it_carriers('', 1) + ' }'
    sendJson(json_string, url, -1)
    time.sleep(1)

def single_run( url, location ):
    sendState(location, url, -1)

def main( url, location ):
    if location:
        if (location == 'NO'):
            location = ''
        single_run(url, location)
        sys.exit(0)
    while (1):
        complete_run(url)
        #random_run(url)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ubisense Mock Server')
    parser.add_argument('--url', required=True, help='The URL of the endpoint', dest='url')
    parser.add_argument('--location', required=False, help='Send a single requrest with the given location. Use NO for empty location. If omitted the server will run in an loop, playing the specified behavior.', dest='location')
    args = parser.parse_args()
    main(args.url, args.location)
