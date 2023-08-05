# Jsmsgr

An easy way to publish transactional messages (SMS, EMAIL, etc.) to Semaphore for their publication!

# Requirements

This app requires two other apps to work properly:

* jsm-user-services;
* django-stomp.

Both apps must have been configured properly. Their configs are as follows, including `jsmsgr` lib:

```python
########################
# Django settings file #
########################
import os

INSTALLED_APPS = [
    "...",
    "django_stomp",
    "jsm_user_services",
    "jsmsgr",  # add this lib to the INSTALLED_APPS
]

# django-stomp config
STOMP_SERVER_HOST = os.getenv("STOMP_SERVER_HOST")
STOMP_SERVER_PORT = os.getenv("STOMP_SERVER_PORT")
STOMP_SERVER_USER = os.getenv("STOMP_SERVER_USER")
STOMP_SERVER_PASSWORD = os.getenv("STOMP_SERVER_PASSWORD")
STOMP_USE_SSL = os.getenv("STOMP_USE_SSL", "True")
LISTENER_CLIENT_ID = os.getenv("STOMP_CONSUMPTION_QUEUE")

# jsm-user-services config
USER_API_HOST = os.environ.get("USER_API_HOST")
```

# Installing

```
pip install jsmsgr   
```

# Setup

In order to use the lib, add the following env variable which sets the final semaphore destination name:

```python
import os

JSMSGR_DESTINATION=os.getenv("JSMSGR_DESTINATION")
```

# Using the lib

## Publishing a single message


```python
from jsmsgr.api import send_msg_to_user
    
msg_dict = {
    "msg": "Hello, there, ###_USER_NAME_###",
    "type": "sms",
    "external_id": "external123",
    "callback_mo_destination": "/queue/mo",
    "to_user_id": "a58c4853-2fa5-4891-80c7-f48287dbf403",  # user_id to send the msg to
}

send_msg_to_user(msg_dict)  # creates a publisher internally
send_msg_to_user(msg_dict, semaphore_publisher=your_publisher)  # user your publisher
```


## Publishing a list of messages

```python
from jsmsgr.api import send_msgs_to_user
    
msgs_dict = {
    "msgs": [
        {
            "msg": "Hello, there, ###_USER_NAME_###",
            "type": "sms",
            "external_id": "external123",
            "callback_mo_destination": "/queue/mo",
            "to_user_id": "a58c4853-2fa5-4891-80c7-f48287dbf403",  # user_id to send the msg to
        },
        {
            "msg": "<strong>Hello world there, ###_USER_NAME_###</strong>",
            "subject": "sub1",
            "type": "email",
            "to_user_id": "a58c4853-2fa5-4891-80c7-f48287dbf403",
        },
        {
            "msg": "<strong>Hello world there once again, ###_USER_NAME_###</strong>",
            "subject": "sub1",
            "type": "email",
            "to_user_id": "a58c4853-2fa5-4891-80c7-f48287dbf403",
        }            
    ]
}

send_msgs_to_user(msgs_dict)  # creates a publisher internally
send_msgs_to_user(msgs_dict, semaphore_publisher=your_publisher) # user your publisher
```

## Replacing tags in the original message

Some tags are used to perform string replacements, such as the user name, in the original message. Some tags
are the following:


`###_USER_NAME_###`: Replaced by user name (name of the user with the given `to_user_id` parameter value).

Example:

```
"Hello there, ###_USER_NAME### !"
```

Is sent as:

```
"Hello there, Igor !"
```