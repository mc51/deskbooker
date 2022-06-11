# Deskbooker

Small tool for booking a desk for multiple days on Deskbird

## Installation

Resolve dependencies via [poetry](https://python-poetry.org/):

```console
poetry install
```

Create a .env file in the root folder similar to this:

```
TOKEN_KEY = "AIzaSyCdsf2vthfqCzIEfb234MABk46DAuvncRQ"
REFRESH_TOKEN = "AIwUaOmk334xPq5nQS[...]"
RESOURCE_ID = "ckya3sdjtu001q01s66m1w97i0"
WORKSPACE_ID = "ckasd234xoy002s01s6eu2w428t"
ZONE_ITEM_ID = 68910
```
ZONE_ITEM_ID can be empty. Then, you need to specify desk id and zone on command run.  

\* check the network traffic on web.deskbird.app to find the correct values for your user and the desk you want to book.

TOKEN_KEY can be fetched from the request when you login with SSO:
```
https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key=[TOKEN_KEY]
```

And REFRESH_TOKEN is in the response.

WORKSPACE_ID and RESOURCE_ID is fetched from the request that is made when you book a table.

## Usage

Make sure the virtual enviroment is activated

Book multiple days
```console
python book.py book --from 2022.01.01 --to 2022.01.10 --zone "Marketing Advertising" --desk "3.99"
```

or if you have ZONE_ITEM_ID in your .env file

```console
python book.py book --from 2022.01.01 --to 2022.01.10
```

Check in today
```console
python book.py checkin
```

See all current bookings
```console
python book.py bookings
```

Set your status for a period:
```console
python book.py set_status --from 2022.01.01 --to 2022.01.10 -s "Mobile office"
```

## Credits 
Forked from [Deskbooker](https://github.com/tobiasknudsen/deskbooker)