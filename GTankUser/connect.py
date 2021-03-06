from fabric import Connection
from invoke import Responder

def start(userMap, userPath):
  beRoot = Responder(
    pattern=r"password:",
    response="fxr\n"
  )
  runCommand = Responder(
    pattern=r"u",
    response="\n"
  )
  with Connection("192.168.50.1", port = 22, user = "root", connect_kwargs = {"password" : "fxr"}) as c:
    #c.run("sudo python3 python/GTankRPI/auto_code.py" + userMap + userPath, pty=True, watchers=[beRoot])
    result = c.run("python3 ../home/pi/python/GTankRPI/auto_code.py " + userMap + " " + userPath, pty=True, warn=True, watchers=[beRoot])
    return result.stdout
    
    
    

