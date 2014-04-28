import StringIO
import socket
import urllib

import socks  # SocksiPy module
import stem.process
import stem.connection
import stem.socket

from stem.util import term

class tor:

    def __init__(self, country, sock_port = 7000, ip = '127.0.0.1'):
        # Perform DNS resolution through the socket
        def getaddrinfo(*args):
          return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

        self.sock_port = sock_port
        self.ip = ip
        self.country = country.lower()

        # Set socks proxy and wrap the urllib module
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, self.ip, self.sock_port)
        socket.socket = socks.socksocket
        socket.getaddrinfo = getaddrinfo


    # Start an instance of Tor configured to only exit through Russia. This prints
    # Tor's bootstrap information as it starts. Note that this likely will not
    # work if you have another Tor instance running.
    def start(self):
        def print_bootstrap_lines(line):
          if "Bootstrapped " in line:
            print term.format(line, term.Color.BLUE)


        print term.format("Starting Tor:\n", term.Attr.BOLD)

        self.tor_process = stem.process.launch_tor_with_config(
          config = {
            'SocksPort': str(self.sock_port),
            'ExitNodes': '{'+self.country+'}',
          },
          init_msg_handler = print_bootstrap_lines,
        )

    def status(self):
        try:
            control_socket = stem.socket.ControlPort(self.sock_port)
            stem.connection.authenticate(control_socket)
        except stem.SocketError as exc:
            print "Unable to connect to tor on port "+self.sock_port+": %s" % exc
            return False
        except stem.connection.AuthenticationFailure as exc:
            print "Unable to authenticate: %s" % exc
            return False

        return control_socket.is_alive()

    def stop(self):
        self.tor_process.kill()  # stops tor