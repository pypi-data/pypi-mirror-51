
Oathkeeper
---
**Created for internal ```Greendeck``` use only. Can be used for non-commercial purposes.**

![Greendeck][gd]  ![oathkeeper][oathkeeper]

[gd]: https://greendeck-cdn.s3.ap-south-1.amazonaws.com/dumps/gd_transparent_blue_bg.png "Logo Title Text 2"
[oathkeeper]: https://greendeck-cdn.s3.ap-south-1.amazonaws.com/dumps/oathkeeper.png "Logo Title Text 2"

A simple library to keeps and maintains all your secret keys, API keys, connection strings and environment variables in a safe place for you to use. Just like Ser Jamie kept his oaths.

You don't need to worry about deployment or maintenance. All you need:
1. Install the Library
2. Signup on oathkeeper.greendeck.co or contact developers@greendeck.co

### About Oathkeeper
*Oathkeeper* is your omnipresent dictionary of key value pairs. Think of *Oathkeeper* as remote JSON object.
It is compatible with all JSON serializable data-types.

### Install from pip
https://pypi.org/project/oathkeeper/

```pip install oathkeeper```

### How to use ?
##### import ```Oathkeeper``` class
```python
from oathkeeper import Oathkeeper
```

##### initialize ```Oathkeeper``` client connection as per your requirements
```python
# declare variables
oathkeeper_EMAIL = <YOUR_oathkeeper_EMAIL> # signup here: oathkeeper.greendeck.co
oathkeeper_PASSWORD = <YOUR_oathkeeper_EMAIL> # signup here: oathkeeper.greendeck.co
oathkeeper_ENV = <YOUR_oathkeeper_ENV> # This can be a string; for example, "production", "testing", "staging" etc.
# The default values are oathkeeper_ENV='default'

# Now initialize the Oathkeeper Object
oathkeeper = Oathkeeper(oathkeeper_EMAIL, oathkeeper_PASSWORD, oathkeeper_ENV)
```

##### using ```Oathkeeper```
Once, you have the Oathkeeper object for a particular environment. You can **set**  or save key value pairs and **get** values for any key in that particular environment.
```python
oathkeeper.get(key) # will return the value for the key in your Oathkeeper object. The key needs to be present.
oathkeeper.set(key, value) # will set the key to the provided value in your Oathkeeper object.
```

---
How to build your pip package

* open an account here https://pypi.org/

In the parent directory
* ```python setup.py sdist bdist_wheel```
* ```twine upload dist/*```

references
* https://medium.com/small-things-about-python/lets-talk-about-python-packaging-6d84b81f1bb5

# Thank You
