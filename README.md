# Mitten

Mitten is an easy packet-level modding platform for Cube World which allows for control over a server using plugins.

## Setting up a server using Mitten

Mitten operates as a "man in the middle" between the server and the clients:

![Mitten](https://i.imgur.com/q5ZAEQo.png)

This means that the internal Cube World server must run on a different port, so that Mitten service requests on the default port of 12345. There is a script included for modifying a Server.exe to operate on a different port. Mitten, by default, expects the internal server to run on port 12344.

## Plugins

Any .py file placed into the Plugins folder will be loaded as a plugin for Mitten, and may be enabled or disabled via the global configuration. Plugins may also place anything they wish to be configurable into their section of the global configuration. 
