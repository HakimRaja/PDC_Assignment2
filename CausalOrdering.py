import threading
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

class BSSProcess:
    def __init__(self, process_id):
        # Initializing a process with its ID and components
        self.process_id = process_id
        self.clock = defaultdict(int)  # Logical clock tracking message delivery per process
        self.message_queue = []  # Queue for storing messages before delivery
        self.delivered_messages = []  # List of delivered messages
        self.thread_pool = ThreadPoolExecutor(max_workers=5)  # Thread pool to handle incoming messages
    def send_message(self, message, recipients):
        # Increment logical clock before sending a message
        self.clock[self.process_id] += 1
        timestamp = dict(self.clock)
        # Sending message to all recipients using thread pool
        for recipient in recipients:
            self.thread_pool.submit(recipient.receive_message, message, self.process_id, timestamp)

    def receive_message(self, message, sender_id, timestamp):
        # Storing the received message in the message queue
        self.message_queue.append((message, sender_id, timestamp))
        self.process_message_queue()  # Attempt to process messages from the queue

    def process_message_queue(self):
        to_remove = []  # Keep track of messages to be removed after processing
        # Checking all messages in the queue for potential delivery
        for message, sender_id, timestamp in self.message_queue:
            if self.can_deliver(timestamp, sender_id):  # If message can be delivered
                self.deliver_message(message, sender_id, timestamp)
                to_remove.append((message, sender_id, timestamp))

        # Remove delivered messages from the queue
        for item in to_remove:
            self.message_queue.remove(item)

    def can_deliver(self, timestamp, sender_id):
        # Check if the message is ready to be delivered based on causal ordering
        if self.clock[sender_id] + 1 == timestamp[sender_id]:
            for process_id, time_value in timestamp.items():
                if process_id != sender_id and self.clock[process_id] < time_value:
                    return False  # Message cannot be delivered if dependency is not satisfied
            return True  # All dependencies are satisfied, deliver the message
        return False

    def deliver_message(self, message, sender_id, timestamp):
        # Update logical clock and store the delivered message
        self.clock[sender_id] += 1
        self.delivered_messages.append((message, sender_id, timestamp))
        print(f"Process {self.process_id} delivered message from {sender_id}: '{message}' at {self.clock}")


def simulate():
    # Create three processes A, B, and C
    process_A = BSSProcess(0)
    process_B = BSSProcess(1)
    process_C = BSSProcess(2)
    # Simulate message exchanges between processes
    process_A.send_message("Hello from A", [process_B, process_C])
    time.sleep(0.1)
    process_B.send_message("Reply from B", [process_A, process_C])
    time.sleep(0.1)
    process_C.send_message("Message from C", [process_A, process_B])

# Calling the funtion for execution
simulate()
