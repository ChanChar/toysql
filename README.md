Mini project to better understand the inner workings of a NoSQL database.

How to use:

1. Start connection by running `python3 pysql.py`.
2. Open another terminal/command line and run `telnet localhost PORTNUMBER` to interact with the DB and to keep the connection open.
3. Close connection with DB by aborting (Control-C) initial window. (WILL BE CHANGED)

Uses a python dictionary as the main "data store" and uses socket+thread to keep an open connection.

Supports the following standard commands:

PUT, GET, PUTLIST, GETLIST, APPEND, INCREMENT, STATS

An instance of a valid request message is built with FOUR arguments delimited by `;`:

```
COMMAND;[KEY];[VALUE];[TYPE]
```

An instance of a valid response message is built with TWO arguments also delimited by `;`:

```
STATUS(TRUE or FALSE);[COMMAND MESSAGE]
```

TODO:

1. Improve `parse_message` to better handle GET, GETLIST, INCREMENT and DELETE commands.
2. Cover how to force quit the 'Address already in use' problem when using Control-C (SIGINT) to close out of DB.
3. Create some level of persistence of data store. Possibly use a JSON file saved to current directory.
4. Update README.md to better cover usage and syntax.
5. Build functionality to query for multiple results.
6. Build better way to exit connections. Related to item 2.
7. Test, tests, testing, tester. 
