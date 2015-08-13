Mini project to understand the inner workings of a NoSQL database.

Uses a python dictionary as the main data store.

Supports the following standard commands:

PUT, GET, PUTLIST, GETLIST, APPEND, INCREMENT, STATS

An instance of a valid request message is built with three arguments delimited by `;`:

COMMAND;[KEY];[VALUE];[TYPE]

An instance of a valid response message is built with two arguments also delimited by ';':

STATUS (TRUE or FALSE); [COMMAND MESSAGE]
