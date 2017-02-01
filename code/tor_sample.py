#Using "To Russia with love" tutorial to connect & stablish a TOR circuit
# https://stem.torproject.org/tutorials/to_russia_with_love.html
#
# This code is different from the provided by the tutorial due special configuration 
# needed for tor_process in MacOS

import socks  # SocksiPy module
import socket
import urllib
import io

import stem.process
from stem.util import term

SOCKS_PORT = 7000

# Set socks proxy and wrap the urllib module

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', SOCKS_PORT)
socket.socket = socks.socksocket

# Perform DNS resolution through the socket

def getaddrinfo(*args):
  return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

socket.getaddrinfo = getaddrinfo

def query(url):
  """
  Uses urllib to fetch a site using SocksiPy for Tor over the SOCKS_PORT.
  """

  try:
    return urllib.urlopen(url).read()
  except:
    return "Unable to reach %s" % url
    
def print_bootstrap_lines(line):
  if "Bootstrapped " in line:
    print(term.format(line, term.Color.BLUE))


print(term.format("Starting Tor:\n", term.Attr.BOLD))

tor_process = stem.process.launch_tor_with_config(
  tor_cmd = '/Applications/TorBrowser.app/Contents/MacOS/Tor/tor.real',
  config = {
    'SocksPort': str(SOCKS_PORT),
    'ExitNodes': '{ru}',
    'GeoIPFile': r'/Applications/TorBrowser.app/Contents/Resources/TorBrowser/Tor/geoip',
    'GeoIPv6File' : r'/Applications/TorBrowser.app/Contents/Resources/TorBrowser/Tor/geoip6'
  },
  init_msg_handler = print_bootstrap_lines,
)

print(term.format("\nChecking our endpoint:\n", term.Attr.BOLD))
print(term.format(query("https://www.atagar.com/echo.php"), term.Color.BLUE))

tor_process.kill()  # stops tor
