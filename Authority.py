import sqlite3


def get_public_key(node_number):
    conn = sqlite3.connect('node_keys.db')
    cursor = conn.cursor()

    cursor.execute("SELECT public_key FROM keys WHERE node_number = ?", (node_number,))
    public_key = cursor.fetchone()

    conn.close()

    return public_key[0] if public_key else None


