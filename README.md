## Basic Website Server

### Intro

Hello and welcome to my basic website server!

It is pretty basic, all it does is handle HTTP requests

It only fully handles the GET request so far by actually 
sending over my index.html or notFound.html file, but the rest of the 
HTTP requests are responded to with complete headers
along with a brief message stating that this server
cannot handle that yet

### Compiling

Things you will need downloaded for this to work:

- latest version of python3

Libraries:

- socket - for all server needs
- email.utils - for HTTP date formatting
- os - for file finding

To get the latest update of python3 just Google "install latest update of python3 [Operating System]"
To install pip just Google "install pip [Operating System]"
To get these imports to work I updated my pip with the command `pip install --upgrade pip` 
Then I used `pip install [program to install]`
If it does not work try `pip3 install [program to install]`

### Instructions

When running `python3 server.py` you will be prompted to enter a port number;
this is the port number the server will be using when running on your computer
locally, so when you search the server on Google, Safari, Postman, etc., type 
in `localhost:[port number you entered]` or `127.0.0.1:[port number you entered]`

To exit the script and close the server, use Ctrl-C at any time