# NikDev IoT Client (Python)

**Python API for accessing the NikDev IoT Server**

This package is serving as an API client for accessing the [NikDev IoT Server](https://iot.nik-dev.se/admin/login),
and simplify uploading data to the server.

## Installation

Using pip:

    pip install nikdev-iot

From source:

    python setup.py install


## Using the API

Before using the API you need to [create an account](https://iot.nik-dev.se/admin/register)
and a device to connect against.

### Finding ID and Keys

In order to connect to the server you need a Device ID and an API Key.
Both the Device ID and API Key are of a UUID structure:
`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`.

The Device ID is found on the first view when you open your device on the
Server GUI, and the API Key can be found under the section API Keys
under the same device. If you don't have an API Key you can create one.

### Importing and initializing
To import the API, use the following:
```python
from nikdev_iot import Api, PushException, GetException
```

The `PushException` and `GetException` can be good to import to catch eventual 
errors when sending or receiving data.

To initialize the API class, there's 2 options. Either you can
pass a dict with configuration values, or you can create it from
entering the credentials. The second option is handy if you want
to use the default configuration.

```python
# Method 1: initialization with a dict.
api = Api({
    'deviceId': '<Device ID>',
    'apiKey': '<API Key>'
})

# Method 2: initialization with credentials.
api = Api.from_credentials('<Device ID>', '<API Key>')
```

### Test connection
> Not implemented yet.

### Storing data
In order to add and store data to the API, you must pass the data as key-value pairs.

```python
api.add_value('<Field ID 1>', '<Value>')
api.add_value('<Field ID 2>', '<Value>')
```

Trying to add 2 values with the same Field ID will overwrite the previous value.

After entering all values you'd like to store you must commit them.
Committing values will lock them, just like a commit in git, and is
prepared to be pushed.

```python
api.add_value(...)
api.commit()
```

> The terminology is on purpose made to mirror git commands as much
> as possible, since it's a simple way to get a quick start on the API
> (assumed you know some of the git commands).


### Uploading data
After you've committed your values it's time to uoload them.
Uploading is done by calling `push()`. This will try to upload
any committed values to the server. If there's unpushed committed
values they will be uploaded as well.

```python
api.add_value(...)
api.commit()
api.push()
```

It's possible to run both commit and push in one function
call by using `commit_and_push()`.
```python
api.add_value(...)
api.commit_and_push()
```

Normally you don't get any response from either `commit()` or `push()`.
However, if there's an error when uploading the values `push()` will throw an
`PushException`. This can be done for a number of reasons, but the important cases are:
 - You entered wrong Device ID or API Key
 - Your API Key doesn't have write access (this can easily be fixed from the Server GUI)
 - The server messed up.
 - The connection timed out.

The last two reasons are categorized as "Bad Luck" and you can try again to upload your data.
However, if there's anything wrong with the Device ID or API Key (entered wrong or doesn't have access)
your committed values will be thrown away.

if you want to catch these exceptions, just wrap the push command with a `try/exception clause` and
catch `PushException`:

```python
try:
    # Try to push the values to the server
    api.push()
except PushException as exception:
    if exception.retained_data:
        pass
        # The data is still intact and can be re-pushed
    else:
        pass
        # The data is no more.
    pass
```

### Full example

```python
# Importing the API
from nikdev_iot import Api, PushException

# Initialize the api from credentials
api = Api.from_credentials('<Device ID>', '<API Key>')

# Add values to be uploaded
api.add_value('<Field ID 1>', '<Value>')
api.add_value('<Field ID 2>', '<Value>')
# Commit the values to "lock" them, meaning you can add
# new values of the same Field ID without overwriting the previous.
api.commit()

# Adding am additional value for Field ID 1
api.add_value('<Field ID 1>', '<Another Value>')
# Commit that value as well
api.commit()

# We'll try to push the data 3 times
for _ in range(0, 3):
    try:
        # Try to push the values to the server
        api.push()
        # If we reach the next line, we can safely exit the loop
        break
    except PushException as exception:
        # Check if the data was retained
        if exception.retained_data:
            # If so, sleep for a while and try to push it again.
            import time; time.sleep(2)
        else:
            # Otherwise we exit the loop as we won't be able to push it again
            break
```

### Fetching data
> Not implemented yet.
