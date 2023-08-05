# SideGears desktop app runtime

https://gitlab.com/john.tourtellott/sidegears

SideGears is a set of lightweight tools for creating desktop
applications that consist of an html/css/javascript UI with a
python backend. The toolset has two parts

* Python kernel for backend processing and platform access. The python
  kernel is available from pypi ("pip install sidegears").
* Javascript client for browser-based user interface. The javascript
  client is available from npmjs ("npm install sidegears").

The two halves connect through a standard websocket and
communicate via json-rpc messages. In the typical use case, the
user interface -- running in a browser -- calls methods in the kernel via
the sidegears API. See examples in the npm package, including one that uses the
python webruntime library to launch a browser instance from python.

SideGears supports 3 of the 4 RPC transport cases:

* RPC request from the javascript client to the python kernel.
* RPC notification from client to kernel.
* RPC notification from kernel to client.

SideGears does *not* support RPC requests from the kernel to the
client. This can be added, but is not considered needed for the
envisioned desktop applications.

## Python Kernel
The sidegears kernel uses the standard websockets module that runs in
the asyncio event loop. The kernel has two public objects:

```
from sidegears.kernel import RPCKernel, rpc_method
```

Kernel methods are:

* `start(self, host='localhost', port='5678', close_on_disconnect=False)`
  Start the kernel, listening for client connections on the specified
  host and port. When the `close_on_disconnect` flag is set, the kernel
  will run until the client connection closes. (This call is not
  blocking.)
* `stop(self)` Stop the kernel, terminating any websocket connections.
* `wait_until_closed(self)` Returns a future that resolves when the
   kernel has stopped. This method is used when the close_on_connection
   flag is set when the kernel is started.
* `send_notification(self, method, params=None)` Send a notification
  message to the client.
* `set_basic_logging(self, enabled)` Enable logging of the RPC messages
  sent and received.
* `set_debug(self, enabled)` Enabled debug options in the json RPC
  server.
* `set_trim_log_values(self, enabled)` When basic logging is enabled,
  shorten the messages logged to the console.

Application RPC methods are designated by using the `rpc_method`
decorator, for example:

```
@rpc_method
async def multiply(x, y):
    return x*y
```

Note that RPC methods must be defined with the async keyword.

Source code for several examples applications that run the kernel
and launch a browser/UI are included in the package distribution files.
You can find these in the python site-packages/sidegears folder.

## Javascript Client Packages

The javascript libraries are used in conjunction with the
corresponding python sidegears package. When the python
sidegears kernel is running, the sidegears js library can connect
to the kernel and make functions calls (which are transported as
json-rpc messages over websockets.)

There are four packages in the dist folder:

* sidegears.js : UMD format, for running in browser or bundled with
  common js applications. This is the default package entry point.
* sidegears.esm.js : ES6 package for bundling into large applications
* sidegears-plugin.js : UMD format for Vue applications in browser or
  commonjs
* sidegears-plugin.esm.js : ES6 format for Vue applications, for
  bunding into applications

### Javascript UI/Client

For starndard html pages, use `sidegears.js` or `sidegears.esm.js`,
depending on your bundling format. The API is very small, and used
in the examples/client/client.html file. The API methods are:

* `sidegears.connect(host='localhost', port=5678)` opens the connection
  to the kernel. The method returns a promise object, which must
  resolve before calling methods on the kernel.

* `sidegears.disconnect()` closes the connection to the kernel. For
  desktop apps, this can be called in response to the window
  `beforeunload` event, although there is no guarantee it will be
  executed before the window closes.

* `sidegears.requester` returns a proxy object that can be used to make
  make RPC request calls directly. In brief, calling
  `sidegears.requester.method(params)` is equivalent to calling
  `sidegears.sendRequest(method, params)`.

* `sidegears.notifier` returns a proxy object for making RPC
  notification calls directly. Calling
  `sidegears.notifier.method(params)` is equivalent to calling
  `sidegears.sendNotification(method, params)`.

* `sidegears.sendRequest(method, parameters)` makes an rpc call to the
  kernel, returning a promise object that resolves with the reply or
  error. The "method" argument is a string, and the "parameters" are
  passed to the method when it is executed in the kernel. Only
  parameters that can be json serialized can be used.

* `sidegears.sendNotification(method, parameters)` makes an rpc call to
  the kernel, but unlike reqest calls, there is no return from rpc
  notification calls. The "method" argument is a string, and the
  "parameters" are passed to the method when it is executed in the
  kernel. Only parameters that can be json serialized can be used.

* `sidegears.onNotify` is used to set a function to be called when
  notification messages are received from the python kernel.

### Vue API

For Vue.js applications, you can use the `sidegears-plugin.js` and
`sidegears-plugin.esm.js` files, which implement a Vue.js plugin.
When installed, the plugin injects a global Vue.$\_sidegears object.
The plugin object has the same basic methods as described above for the
standard API. From Vue components:

* `this.$\_sidegears.connect(host='localhost', port=5678)`
* `this.$\_sidegears.disconnect()`
* `this.$\_sidegears.sendRequest(method, params)`
* `this.$\_sidegears.sendNotification(method, params)`

Other methods are:

* `$_sidegears.isOpen()` returns a boolean indication whether the
  client is connected to the kernel or not.

* `$_sidegears.getRequestProxy()` returns a proxy object that can make
  RPC request calls directly (same as the javascript requester).

* `$_sidegears.getNotifyProxy()` returns a proxy object that can make
  RPC notification calls directly (same as the javascript notifier).

In addition, a custom `notification` event is emitted when a notification message is
received from the kernel. The event arguments are the accompanying
method and parameters.

## Background

In some ways, SideGears is analogous to application frameworks such
as Electron and NW.js, which also provide an html/js/css user
interface.

* The main difference is that SideGears uses a python backend,
  whereas Electron and NW.js use nodejs.
* Also, in Electron and NW.js, the UI and nodejs logic are tightly
  coupled through a single event loop; whereas the SideGears UI and
  backend run in separate event loops, and
  can be run in separate processes. (Theoretically, SideGears
  frontend and backend can run on different machines, although this is
  not officially supported.)
* SideGears can be used with an existing browser for the UI,
  or in an application an embedded browser.

Finally, if anyone is curious where the term SideGears comes from:

* "Side" refers to PySide, which is the original name of the Qt for
  Python [1] project. Our initial implementations use the PySide
  QWebEngine library for the UI rendering engine (although we have
  moved on to webruntime). SideGears is also a "side" project for the
  author.
* "Gears" refers to TurboGears [2], a well-established web framework
  that takes a "best of breed" approach, combining existing tools into
  a cohesive system. We like their approach and try to emulate it. We
  also want to portray our project as a small set of software tools,
  not a full-scale "platform" or "framework".

[1] Qt for Python is at https://www.qt.io/qt-for-python

[2] TurboGears is at http://www.turbogears.org/
