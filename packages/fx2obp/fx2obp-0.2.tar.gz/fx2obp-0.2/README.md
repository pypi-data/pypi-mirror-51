
## What

- Convert a http://www.floatrates.com/json-feeds.html daily rates json src file 
to valid Open Bank Project payload.
- HTTP PUT them to an Open Bank Project endpoint to populate the database via the `fx` api call

- Uses python3 

## Setup 

- You must have a valid Direct Login token
- You must have the `CanCreateFxRateAtAnyBank` permission

```
export ENDPOINT=<api.example.com>
export AUTH_TOKEN=<direct-login-token>
```
#### Options

- WRITE_TO_FILE - Write output to disk
- POST_TO_OBP - Post to Open Bank Project api endpoint

**Note:** By default this wont post to the enpoint. This is to allow testing
to post to an endpoint, set the environment up:

```
export WRITE_TO_FILE=False
export POST_TO_OBP=True
```
The above allows you to test before blasting an endpint with invalid data.


## Run
    pip install -r requirements.txt
    python3 convert.py

