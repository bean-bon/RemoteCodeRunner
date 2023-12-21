# Remote Code Runner

Intended for use with my dissertation project Bookie, an extended Markdown syntax.
To use this app:
  - start the Flask server in app.py,
  - send a POST request to the server with a form object containing fields 'code' (string representation of the code) and 
'lang' (language name),
  - receive the output of the program, or an error code 
