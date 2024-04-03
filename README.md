# Remote Code Runner

Intended for use with my dissertation project Bookie, an extended Markdown syntax editor with web server compilation features.
To use this app:
  - start the Flask server in app.py,
  - send a POST request to the server with a form object containing fields 'code' (string representation of the code), 
'lang' (language name), and optionally 'name', containing the intended executable file name (useful for Java)
  - receive the output of the program (on key 'output'), and the run result message (on key 'exit_code')
