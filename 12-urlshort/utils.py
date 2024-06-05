import hashlib
import redis
import json

def create_hash(input_string, hash_length=10):
    # Create a SHA-256 hash object
    hash_object = hashlib.sha256()
    
    # Update the hash object with the input string encoded in UTF-8
    hash_object.update(input_string.encode('utf-8'))
    
    # Get the hexadecimal representation of the hash
    hash_hex = hash_object.hexdigest()
    
    # Return the first 10 characters of the hash for a shorter hash
    # You can adjust the length as needed
    short_hash = hash_hex[:hash_length]
    
    return short_hash

def add_to_cache(host='localhost', port=6379, db=0, key=None, value=None, set_key=None, set_values=None):
    """
    Adds a key-value pair to the Redis cache and/or adds members to a set.

    Parameters:
    host (str): Redis server hostname.
    port (int): Redis server port.
    db (int): Redis database number.
    key (str): The key to add to the cache.
    value (str): The value to associate with the key.
    set_key (str): The key of the set to add members to.
    set_values (list): The values to add to the set.

    Returns:
    bool: True if the operations were successful, False otherwise.
    """
    try:
        # Create a Redis client
        client = redis.Redis(host=host, port=port, db=db)
        
        if key and value:
            # Add the key-value pair to the cache
            client.set(key, value)
            print(f"Successfully added {key}:{value} to the cache.")
        
        if set_key and set_values:
            # Add the values to the set
            client.sadd(set_key, *set_values)
            print(f"Successfully added {set_values} to the set {set_key}.")
        
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def is_in_cache(host='localhost', port=6379, db=0, key=None, set_key=None, set_value=None):
    """
    Checks if a key or set member exists in the Redis cache.

    Parameters:
    host (str): Redis server hostname.
    port (int): Redis server port.
    db (int): Redis database number.
    key (str): The key to check in the cache.
    set_key (str): The key of the set to check in.
    set_value (str): The value to check for in the set.

    Returns:
    bool: True if the key or set member exists, False otherwise.
    """
    try:
        # Create a Redis client
        client = redis.Redis(host=host, port=port, db=db)
        
        if key:
            # Check if the key exists in the cache
            if client.exists(key):
                return True
        
        if set_key and set_value:
            # Check if the value exists in the set
            if client.sismember(set_key, set_value):
                return True
        
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def add_object_to_cache(host='localhost', port=6379, db=0, key=None, value=None):
    """
    Adds an object (Python dictionary or list) to the Redis cache by serializing it as JSON.

    Parameters:
    host (str): Redis server hostname.
    port (int): Redis server port.
    db (int): Redis database number.
    key (str): The key to add to the cache.
    value (object): The Python object (dictionary, list, etc.) to store as JSON.

    Returns:
    bool: True if the operation was successful, False otherwise.
    """
    try:
        # Create a Redis client
        client = redis.Redis(host=host, port=port, db=db)

        # Serialize the object as JSON
        serialized_value = json.dumps(value)

        # Add the key-value pair to the cache
        client.set(key, serialized_value)
        print(f"Successfully added {key}:{serialized_value} to the cache.")

        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
