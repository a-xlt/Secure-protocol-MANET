import sqlite3


def get_public_key_by_nodeNumber(nodeNumber):
    conn = sqlite3.connect('keys.db')
    cursor = conn.cursor()

    # Retrieve the public key name based on the provided ID
    cursor.execute('SELECT public_key_name FROM key_pairs WHERE nodeNumber = ?', (nodeNumber,))
    result = cursor.fetchone()

    if result:
        public_key_name = result[0]

        # Read and return the public key
        with open('public_keys\\' + public_key_name, 'rb') as f:
            public_key = f.read()

        return public_key

    # If ID not found, return None
    else:
        return 'No key Found!'
