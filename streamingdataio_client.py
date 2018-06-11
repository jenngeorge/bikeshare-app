https://github.com/streamdataio/streamdataio-python/blob/master/client.py

"""Streamdata.io demo."""

import sys
import collections
import json
import time
import random

import jsonpatch
import requests
import sseclient
from terminaltables import AsciiTable

SD_TOKEN = "[YOUR_STREAMDATAIO_APP_TOKEN]"
DEMO_API = "http://stockmarket.streamdata.io/v2/prices"
URL = (
    "https://streamdata.motwin.net/{}?X-Sd-Token={}".format(DEMO_API, SD_TOKEN)
)

def print_table(data):
    """Print data as a table."""
    table_data = []
    for item in data:
        item = collections.OrderedDict(
            sorted(item.items(), key=lambda t: t[0]))
        if len(table_data) == 0:
            table_data.append(item.keys())
        table_data.append(item.values())
    table = AsciiTable(table_data)
    print(table.table)


def run(data, headers, retryCount):
    """Launch client."""
    """with requests.get(URL, stream=True) as response:"""

    print(headers)
    try:
            with requests.get(URL, stream=True, headers=headers) as response:
                client = sseclient.SSEClient(response)
                for event in client.events():
                    if event.event == "data":
                        print("Data event received")
                        last_event_id = event.id
                        data = json.loads(event.data)
                        print_table(data)

                    elif event.event == "patch":
                        print("Patch event received")
                        last_event_id = event.id
                        patch = jsonpatch.JsonPatch.from_string(event.data)
                        patch.apply(data, in_place=True)
                        print_table(data)

                    elif event.event == "error":
                        """Print the error by default.
                           You can perform some error analysis according to
                           the message sent"""
                        print("Error: {}".format(event.data))
                        """By default, close the connnection and re-initiate a
                           new one with the Last-Event-ID of the latest message
                        """
                        client.close()

                        """Depending on the analysis of the error, you may want to
                           reconnect. That's the purpose of the code below.
                           BEWARE to perform an error analysis first. IN SOME CASE,
                           YOU DON'T WANT TO RECONNECT blindingly: bad API url,
                           authentication errors, etc. In such a case, you just
                           close the connection and deal with the error.
                           In the below example, we reconnect according to the status
                           code returned by the server.
                           NOTE that in addition, we count the number of attempts.
                           If a threshold of unsuccessful attempts has been reached,
                           we don't reconnect again: the issue is probably permanent.
                           NOTE that you can analyze the err['message'] to provide
                           a finer error message to your end users.
                           """
                        err = json.loads(event.data)
                        status = err['status']

                        """ status 2001 -> the API had an error, retry can be worthwhile
                            status 2004 -> there was a connection issue with the targeted API server, retry can be worthwhile
                            status 2008 -> there was an issue while sending the event message from the server, retry can be worthwhile
                        """
                        if retryCount < 5 and (status == 2001 or status == 2004 or status == 2008):
                            retryCount = retryCount + 1
                            """The server can set a retry in ms if not, we set a default
                                one to give to the 'Requests' lib
                                the time to close properly the connection"""
                            retry = 15
                            if event.retry is not None:
                                retry = event.retry / 1000.0

                            """If there are several parallel connections, we introduce
                               a random in order to avoid re-connnections at
                               the same time
                            """
                            time.sleep(retry + random.randint(0, 15))

                            """Re-initiate a new connection with the Last-Event-ID and
                               the latest data received (to be able to apply the next
                               patch)
                            """
                            run(data, { 'Last-Event-ID': last_event_id }, retryCount)

                    else:
                        print("Unhandled event received.")
                        client.close()
    except:
        print("Unexpected error:",  sys.exc_info()[0])

if __name__ == "__main__":
    run([], {}, 0)