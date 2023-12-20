# Remote Code Runner

Intended for use with my dissertation project Bookie, an extended Markdown syntax.
To use this app:
  - start the Flask server in app.py,
  - send a POST request to the server (currently there is only support to 127.0.0.1:5000, but this will change later) with a code file,
  - recieve the stdout of the program, or an error code 
