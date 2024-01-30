# file imports
import socket
from email.utils import formatdate
from os.path import exists


# handle request function
def handleRequest( request ):
    # initialize response variables
    http = "HTTP/1.1 "
    status = ""
    acceptLanguage = "Accept-Language: en-US\n"
    connection = "Connection: close\n"
    contentEncoding = "Content-Encoding: utf-8\n"
    date = "Date: " + formatdate( timeval = None, localtime = False, usegmt = True ) + "\n"
    server = "Server: Python\n"
    lastModified = "Last-Modified: Tue, 25 Oct 2022\n"
    # TODO contentLength
    contentType = "Content-Type: text/html"
    crlf = "\n\n"
    content = ""

    # handle GET request
    if "GET" in request:
        # set title and filename
        title = "GET"
        fileName = request.partition( "\n" )[0][5:-10]

        # if file name not specified in GET, set filename to index
        if fileName == "" or fileName == "root":
            fileName = "index.html"

        # if file exists set status
        if( exists( fileName ) ):
            status = "200 OK\n"
        # if not, set filename to notFound and set status
        else:
            fileName = "notFound.html"
            status = "404 Not Found\n"

        # open file, set file data to content, close the file
        file = open( fileName )
        try:
            content = file.read()
        # if file type cannot be handled ( not html or text ), set content and status as such
        except UnicodeDecodeError:
            content = "Media format of requested message is not yet supported"
            status = "415 Unsupported Media Type\n"
        file.close()
        
    # handle all request types
    elif "HEAD" in request: title, status = "HEAD", "200 OK\n"
    elif "POST" in request: title = "POST"
    elif "PUT" in request: title = "PUT"
    elif "DELETE" in request: title = "DELETE"
    elif "CONNECT" in request: title = "CONNECT"
    elif "OPTIONS" in request: title = "OPTIONS"
    elif "TRACE" in request: title = "TRACE"
    elif "PATCH" in request: title = "PATCH"
    elif "COPY" in request: title = "COPY"
    elif "LINK" in request and "UNLINK" not in request: title = "LINK"
    elif "UNLINK" in request: title = "UNLINK"
    elif "PURGE" in request: title = "PURGE"
    elif "LOCK" in request and "UNLOCK" not in request: title = "LOCK" 
    elif "UNLOCK" in request: title = "UNLOCK"
    elif "PROPFIND" in request: title = "PROPFIND"
    elif "VIEW" in request: title = "VIEW"
    else: title, status, content = "INVALID", "418 I'm a teapot\n", "The server refuses the attempt to brew coffee with a teapot."

    # set status and content for HTTP requests that cannot be handled yet
    if status == "" and content == "":
        status = "501 Not Implemented\n"
        content = "Server cannot handle " + title + " requests yet"

    # set headers
    headers = http + status + acceptLanguage + connection + contentEncoding + date + server + lastModified + contentType + crlf

    # return request title, response headers and response content
    return [title, headers, content]


# main function
def main():
    # initialize variables
    host = "127.0.0.1" # IP address that the server is running on
    maxline = 1024
    port = -1

    # display starting server
    print( "\n" )
    print( "----------------------------------------------------------" )
    print( "| Welcome to Agua-Chile's server!                        |" )
    print( "| When prompted enter the port number you'd like to use  |" )
    print( "| Enter Ctrl-C to close server and exit python script    |" )
    print( "----------------------------------------------------------" )
    print( "\n" )

    # set port to input, make sure that it is a valid number, create and bind socket
    while port == -1:
        try:
            port = int( input( ">> Enter a port number: " ) )

        # if input is not a number
        except ValueError:
            print( ">> Port entered is not a integer, try again" )
            port = -1

        # if Ctrl-C close the connection
        except KeyboardInterrupt:
            print( "\n>> Keyboard force exit detected, shutting down server" )
            quit()

        # create socket
        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM, 0 )
        sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )

        # bind socket
        try:
            sock.bind( ( host, port ) )

        # if port is busy
        except ( PermissionError, OSError ):
            print( ">> Port number is currently being used by something else, try again" )
            port = -1
            sock.close()
            
        # if input number is to high
        except OverflowError:
            print( ">> Port number must be between 1-65535 try again" )
            port = -1
            sock.close()

        # if input number is 0
        if port == 0:
            print( ">> Port number must be between 1-65535 try again" )
            port = -1
            sock.close()

    # start listening
    sock.listen( 1 )
    print( ">> Listening on port", port )

    # loop continuously
    while True:    
        try:
            # accept client connections
            connection, address = sock.accept()
            print( ">> Connected to client at", address )

            # get the client request
            request = connection.recv( maxline ).decode()
            print( ">> HTTP request recieved" )
            print( "\nHTTP Request:\n", request[:-2] )

            # send HTTP response
            response = handleRequest( request )
            connection.sendall( response[1].encode() + response[2].encode() )
            print( ">>", response[0], "response sent to", address )
            print( "\nHTTP Response:\n", response[1][:-2], "\n" )

        # if Ctrl-C close the connection, socket and script
        except KeyboardInterrupt:
            print( "\n>> Keyboard force exit detected, shutting down server" )
            try:
                connection.close()
            # if connection hasnt been established then pass
            except UnboundLocalError:
                pass
            sock.close()
            quit()

        # close connection
        connection.close()


# main driver
if __name__ == "__main__":
    main()