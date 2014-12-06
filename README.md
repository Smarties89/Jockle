Jockle
======

Fake or proxy HTTP API's for fast prototyping of frontends or other services.

Current state of project
------------------------

This is very useful in increasing frontend(and other API' users) productivity. However the project is still *beta mode*. It is built as a *need-to-have* tool, and is not *finished, polished or looking good*. Remark also that this is meant to be run in developer environments(not ever in production!), and therefore lot of good security practices have been avoided to decrease limitation of the developer.

How you could benefit from it
-----------------------------

Whenever you are building a web service from scratch or working with a existing project, Jockle will help you out. With a new project you can specify API's and worry about implementing them later(or delegate that to a backend developer, who of course can use your Jockle as specification). When the project moves forward, and you want to use the implemented API when developing, you can use Jockle as a proxy to your implemented server, but still make use of new API's made with Jockle. In other words, Jockle tries to find an API first in the Jockle API list, and if that fails it will proxy the other server.

An Overview of the process can be seen here:
![alt tag](https://raw.githubusercontent.com/Smarties89/Jockle/master/docs/Jockle_overview.png)

Highlights
----------

* Easy prototype webservices, for other webservices or home pages.
* Proxy to another service(so you can use all the existing service, but add new ones)
* Full list HTTP Codes
* Export API to server stub, that you can continue working on.


Plan to implement
-----------------

* Handling for Flask regular expressions(Right now you can't have API's with example <id> )
* Make it possible to insert input variables.
* Make a client-stub-maker for Python-Requests.
