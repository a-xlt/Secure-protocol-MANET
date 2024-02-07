import threading

if __name__ == "__main__":
    sender_node = int(input("Enter Sender node number: "))

    exec(f"from node{sender_node} import route_message as x")
    exec('my_thread =threading.Thread(target=x)')
    exec('my_thread.start()')
