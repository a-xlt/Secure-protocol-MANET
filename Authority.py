import sqlite3


def get_public_key(node_number):
    """
    Retrieves the public key for a given node number from the database.
    :param node_number: The node number whose public key is needed.
    :return: The public key if found, None otherwise.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect('node_keys.db')
    cursor = conn.cursor()

    # Retrieve the public key for the given node number
    cursor.execute("SELECT public_key FROM keys WHERE node_number = ?", (node_number,))
    public_key = cursor.fetchone()

    conn.close()

    return public_key[0] if public_key else None


# The script can still be run standalone for testing purposes
if __name__ == "__main__":
    node_number = int(input("Enter the node number to retrieve the public key: "))
    public_key = get_public_key(node_number)
    if public_key:
        print("Public Key:", public_key)
    else:
        print("No public key found for node", node_number)
