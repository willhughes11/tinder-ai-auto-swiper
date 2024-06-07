#!/usr/bin/env python3
import subprocess
import time
import sys

def process_maintenance(cmd,split_by,remove):
    output = subprocess.check_output(cmd,shell=True)
    encoding = 'utf-8'
    output = str(output, encoding)
    ps_output = list(output.split(split_by))
    while(remove in ps_output):
         ps_output.remove(remove)
    
    return ps_output

def start_remote_server():
    print("Starting Remote Selenium Server...")
    
    platform = sys.platform
    path = './chromedriver_osx' if platform == 'darwin' else './chromedriver_linux'
    
    java_hub = f"java -Dwebdriver.chrome.driver={path} -jar selenium-server-4.0.0-beta-4.jar hub"
    java_node = f"java -Dwebdriver.chrome.driver={path} -jar selenium-server-4.0.0-beta-4.jar node"
    subprocess.Popen(java_hub.split(), stdout=subprocess.PIPE)
    subprocess.Popen(java_node.split(), stdout=subprocess.PIPE)
    print("Done")

def selenium_server():
    ps_return = process_maintenance("ps -ef | grep java"," ","")
    if '/usr/bin/java' not in ps_return:
        start_remote_server()
    else:
        print("Selenium Processes Already Running...")
        pid_to_kill = process_maintenance("ps -ef | grep 'java' | awk '{print $2}'","\n","")
        for i in pid_to_kill:
            print(f"Killing Java PID: {i}")
            try:
                subprocess.Popen(f"kill {i}".split(), stdout=subprocess.PIPE)
            except:
                print(f"Error Killing Java PID: {i}")
        time.sleep(0.1)
        start_remote_server()

if __name__ == "__main__":
    selenium_server()