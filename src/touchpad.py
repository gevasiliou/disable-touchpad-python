#!/usr/bin/env python
#
# @author: Karthik VJ
# @usage: 
#        python touchpad.py [OPTIONS]
#
# @example
#        python touchpad.py -e
#
# @options:
#        -e
#              Enables the touchpad
#              
#        -d
#              Disables the touchpad
#              
#        -s
#              Display the touchpad device status
#
#        -h
#              Help
#

import sys
import subprocess
import re
from optparse import OptionParser

statusFlag = {'--enable': 'Enabled', '--disable': 'Disabled'}

def getDeviceName(deviceId):
  data = subprocess.check_output(['xinput', '--list', '--name-only', deviceId])
  data = data.decode()
  
  return str(data).rstrip('\n')
  
# Gets the touch device ID
def getDeviceId():
  try:
    data = subprocess.check_output(['xinput', '--list'])
  except Exception:
    print("xinput not found!")
    sys.exit();
        
  deviceId = 'none'
  
  for line in data.splitlines():
    line = line.lower()    
    if 'touchpad' in line and 'pointer' in line:
      line = line.strip()
      match = re.search('id=([0-9]+)', line)
      deviceId = str(match.group(1))
      #print(deviceId)
      #print(line)
          
  if deviceId == 'none':
    print('Touch Device not found')
    sys.exit();
    
  return deviceId

# Enables / Disables the device  
def setEnabled(state):  
  deviceId = getDeviceId()
  flag = 'none'
  print("Device Name: %s" % getDeviceName(deviceId))
  
  if state == 'true':
    flag = '--enable'
  elif state == 'false':
    flag = '--disable'
    
  if(flag != 'none'):
    try:
      subprocess.check_call(['xinput', flag, deviceId])
      print('Status: %s' % statusFlag[flag])
    except Exception:      
      print('Device cannot be set to %s' %flag)       
    


# Gets the enable device property for the device Id  
def getDeviceProp(deviceId):  
  propData = subprocess.check_output(['xinput', '--list-props', deviceId])
  propData = propData.decode()
  
  for line in propData.splitlines():    
    if 'Device Enabled' in line:
      line = line.strip()      
      return line[-1]


# Finds the touchpad status and displays the result to screen      
def deviceStatus():
  deviceId = getDeviceId()  
  print("Device Name: %s" % getDeviceName(deviceId))
  
  status = getDeviceProp(deviceId)
  if status == '0':
    print("Status: %s" % statusFlag['--disable'])
  elif status == '1':
    print("Status: %s" % statusFlag['--enable'])
  else:
    print("Error can not find device status.")


# Main      
def main(): 
  parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0", description="Example: %prog -e")
  parser.add_option("-s", "--status", default=False, action="store_true", help="Display the status of the Touchpad")
  parser.add_option("-e", "--enable", default=False, action="store_true", help="Enable Touchpad Device")
  parser.add_option("-d", "--disable",default=False, action="store_true", help="Disable Touchpad Device")
  (options, args) = parser.parse_args()
        
  if options.status == True:
    print("Touchpad device status...")
    deviceStatus()
  elif options.enable == True:
    print("Enabling the Touchpad device...")
    setEnabled('true')
  elif options.disable == True:
    print("Disabling the Touchpad device...")
    setEnabled('false')
  else:
    parser.print_help()
                      


if __name__ == '__main__':
  main()
