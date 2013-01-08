#!/usr/bin/env python
#
# @author: Karthik VJ
# @usage: 
#        python touchpad.py [OPTIONS]
#
# @example
#        python touchpad.py enable
#
# @options:
#        enable
#              Enables the touchpad
#              
#        disable
#              Disables the touchpad
#              
#        status
#              Display the touchpad device status
#

import sys
import subprocess
import re

statusFlag = {'--enable': 'Enabled', '--disable': 'Disabled'}

def getDeviceName(deviceId):
  data = subprocess.check_output(['xinput', '--list', '--name-only', deviceId])
  data = data.decode()
  
  return str(data).rstrip('\n')
  
# Gets the touch device ID
def getDeviceId():
  data = subprocess.check_output(['xinput', '--list'])    
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
      subprocess.check_call(['xinputs', flag, deviceId])
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
  operation = 'none'  
  
  # action argument
  if(len(sys.argv) > 1):  
    operation = sys.argv[1]
        
  if operation == 'status':
    deviceStatus()
  elif operation == 'enable':
    setEnabled('true')
  elif operation == 'disable':
    setEnabled('false')
  else:
    print("Use [enable, disable, status] as options!")
                      


if __name__ == '__main__':
  main()
