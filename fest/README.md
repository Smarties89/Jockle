fest
====

Flask Essential(fest) python library

This library contains basic functionality that most web servers need, and was started as a need-to-have library for the many projects I am involved in. This library is in *alpha* release and may break backward compability. This library is specialized in making Flask easier to use, but it can also be used with other server libraries. The goal for this library is to provide easy to use functinonality to Flask, so cherry-pick what you like, and leave the rest out. All feedback/constructive critic are welcomed.

Functionality
-------------
* Logging routes(Python Flask Request)
* RoleAuthenticator to restrict access to functions(or Flask API's)
* Validate user input(with `fest.decorators.validate`)
* CollectiveLogging(needs examples)
* Check if the server is in debug mode (with `fest.util.debug`). This is implemented by the principle of "better safe than sorry". All machines are assumed to be production servers unless a file named /notproducserver exists. Call "makenotprodserver.bash" to make a debug server.


Plan
----

* Create examples.
* Create more documentation.
* Create unit tests


The Example
-----------

Here is an example of the transformation of lot of boilerplate code in Python/Flask using fest. This is from some of my code.

```python
...
@app.route("/translator/translate", methods=["POST"])
def readLog():
    delimeter = request.form['delimeter']
    q = request.form['q']
    slang = request.form['slang']
    tlang = request.form['tlang']
    osep  = request.form['osep']
    sound = request.form['sound'] # What do we want sound from
    log.info("slang:{0}. tlang:{1}. delimeter:{2}. Withsound:{3}. osep:{4}.words:{2}".format(
        slang,
        tlang,
        delimeter,
        sound,
        osep,
        q))
    if len(q) > 1000: # Maximum length of words is 1000 characters
        return "", 500
    ...
    
...
```
With fest this could easily be reduced to the following:

```python
...
from fest.decorators import requireformdata
...
@app.route("/translator/translate", methods=["POST"])
@requireformdata(["delimeter", "q", "slang", "tlang", "osep", "sound"])
def readLog(delimeter, q, slang, tlang, osep, sound):
    log.info("slang:{0}. tlang:{1}. delimeter:{2}. Withsound:{3}. osep:{4}.words:{2}".format(
        slang,
        tlang,
        delimeter,
        sound,
        osep,
        q))
    if len(q) > 1000: # Maximum length of words is 1000 characters
        return "", 500
    ...
    
...
```

The logging boilerplate can easily be replaced by `routelog`

```python
...
from fest.decorators import routelog
...
@app.route("/translator/translate", methods=["POST"])
@routelog
@requireformdata(["delimeter", "q", "slang", "tlang", "osep", "sound"])
def readLog(delimeter, q, slang, tlang, osep, sound):
    if len(q) > 1000: # Maximum length of words is 1000 characters
        return "", 500
    ...
    
...
```

Now we want to validate the length of words, for this we can use `validate` to this. It takes the keyword you want to validate, a lambda which validates, and a possible error message.

```python
...
from fest.decorators import validate
...
@app.route("/translator/translate", methods=["POST"])
@routelog
@requireformdata(["delimeter", "q", "slang", "tlang", "osep", "sound"])
@validate(q, lambda o: len(o) > 1000, "The word have to be lo
def readLog(delimeter, q, slang, tlang, osep, sound):
    ...
    
...
```

This way we transformed lot of typical boilerplate code to similiar very low level lines code. This increases readability, and reduces code. It also has a nice feature that example requireformdata returns to the client what it needs of form data, in case something is not sent with. Example if delimeter is not send in a request the service will reply with "Invalid request, missing form data element delimeter".
