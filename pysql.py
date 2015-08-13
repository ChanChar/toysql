import socket

# Set up stats, command handlers and data store.
HOST = 'localhost'
PORT = 8000
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
STATS = {
    'PUT': {'success': 0, 'error': 0},
    'GET': {'success': 0, 'error': 0},
    'GETLIST': {'success': 0, 'error': 0},
    'PUTLIST': {'success': 0, 'error': 0},
    'INCREMENT': {'success': 0, 'error': 0},
    'APPEND': {'success': 0, 'error': 0},
    'DELETE': {'success': 0, 'error': 0},
    'STATS': {'success': 0, 'error': 0},
}

# Look up table
COMMAND_HANDLERS = {
    'PUT': handle_put,
    'GET': handle_get,
    'GETLIST': handle_getlist,
    'PUTLIST': handle_putlist,
    'INCREMENT': handle_increment,
    'APPEND': handle_append,
    'DELETE': handle_delete,
    'STATS': handle_stats,
}

DATA_STORE = {}

def main():
    SOCKET.bind((HOST, PORT))
    SOCKET.listen(1)

    while True:
        connection, address = SOCKET.accept()
        print("New connection from [{}]".format(address))
        data = connection.recv(4096).decode()
        command, key, value = parse_message(data)

        if command == 'STATS':
            response = handle_stats()
        elif command in ('GET', 'GETLIST', 'INCREMENT', 'DELETE'):
            response = COMMAND_HANDLERS[command](key)
        elif command in ('PUT', 'PUTLIST', 'APPEND'):
            response = COMMAND_HANDLERS[command](key, value)
        else:
            response = (False, 'Unknown command type [{}]'.format(command))

        update_stats(command, response[0])
        connection.sendall('{};{}'.format(response[0], response[1]))
        connection.close()

# Parse and convert values into given type.
def parse_message(data):
    command, key, value, value_type = data.strip().split(';')
    if value_type:
        if value_type == 'LIST':
            value = value.split(',')
        elif value_type == 'INT':
            value = int(value)
        else:
            value = str(value)
    else:
        value = None
    return command, key, value

# Common Handlers

def update_stats(command, success):
    if success:
        STATS[command]['success'] += 1
    else:
        STATS[command]['error'] += 1

def handle_put(key, value):
    DATA_STORE[key] = value
    return (True, 'Key [{}] set to [{}]'.format(key, value))

def handle_get(key):
    if key in DATA_STORE:
        return (True, DATA_STORE[key])
    else:
        return (False, 'KeyError: Key [{}] not found'.format(key))

def handle_putlist(key, value):
    return handle_put(key, value)

def handle_getlist(key):
    return_value = exists, value = handle_get(key)

    if not exists:
        return return_value
    elif not isinstance(value, list):
        return (False, "TypeError: Key [{}] contains non-list values ([{}])".format(key, value))
    else:
        return return_value

def handle_increment(key):
    return_value = exists, value = handle_get(key)

    if not exists:
        return return_value
    elif not isinstance(value, int):
        return (False, "TypeError: Key [{}] contains not-integer values ([{}])".format(key, value))
    else:
        DATA_STORE[key] = value + 1
        return (True, 'Key [{}] incremented'.format(key))

def handle_append(key, value):
    return_value = exists, list_value = handle_get(key)
    if not exists:
        return return_value
    elif not isinstance(list_value, list):
        return (False, "TypeError: Key [{}] contains not-list value ([{}])".format(key, value))
    else:
        DATA[key].append(value)
        return (True, 'Key [{}] had value [{}] appended'.format(key, value))

def handle_delete(key):
    if key in DATA_STORE:
        del DATA_STORE[key]
    else:
        return (False, 'KeyError: Key [{}] not found and could not be deleted'.format(key))

def handle_stats():
    return (True, str(STATS))

if __name__ == '__main__':
    main()
