import subprocess
import sys


def simulate_communication(sender, receiver, filename):
    """
    Simulates the communication between nodes for sending a file.
    This function assumes that node scripts are named node1.py, node2.py, etc.
    """
    node_script = f'node{sender}.py'

    try:
        # Simulating the process by calling the respective node script
        subprocess.run([sys.executable, node_script, str(receiver), filename], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while communicating between nodes: {e}")


if __name__ == "__main__":
    # Example usage
    sender_node = int(input("Enter the sender node number: "))
    receiver_node = int(input("Enter the receiver node number: "))
    filename = input("Enter the filename to send: ")

    simulate_communication(sender_node, receiver_node, filename)
