import threading
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

class BSSProcess:
    def __init__(self, process_id, num_processes):
        self.process_id = process_id
        self.num_processes = num_processes
        self.vector_clock = [0] * num_processes  # Vector Clock to track messages sent and received by this process
        self.matrix_clock = [[0] * num_processes for _ in range(num_processes)]  # Matrix Clock to track dependencies between all processes
        self.message_queue = []  # Queue to temporarily hold messages until they can be delivered
        self.delivered_messages = []  # List of all messages that have been successfully delivered
        self.thread_pool = ThreadPoolExecutor(max_workers=5)  # Thread pool to manage concurrent message processing
    def send_message(self, message, recipients):
        self.vector_clock[self.process_id] += 1  # Updatig vector clock before sending a message
        # Updating matrix clock to reflect the current state of this process
        for i in range(self.num_processes):
            self.matrix_clock[self.process_id][i] = self.vector_clock[i]
        # Sending message to each recipient using separate threads to mimic network communication
        for recipient in recipients:
            self.thread_pool.submit(recipient.receive_message, message, self.process_id, list(self.vector_clock), [row[:] for row in self.matrix_clock])

    def receive_message(self, message, sender_id, vector_timestamp, matrix_timestamp):
        # Storing received message in the queue
        self.message_queue.append((message, sender_id, vector_timestamp, matrix_timestamp))
        self.process_message_queue()  # Attempting to process messages immediately upon receiving

    def process_message_queue(self):
        to_remove = []
        for message, sender_id, vector_timestamp, matrix_timestamp in self.message_queue:
            if self.can_deliver(vector_timestamp, matrix_timestamp, sender_id):
                self.deliver_message(message, sender_id, vector_timestamp)  # Deliver the message
                to_remove.append((message, sender_id, vector_timestamp, matrix_timestamp))

        for item in to_remove:
            self.message_queue.remove(item)  # Remove delivered messages from the queue

    def can_deliver(self, vector_timestamp, matrix_timestamp, sender_id):
        # Check if the vector clock condition for SES mechanism is satisfied
        if vector_timestamp[sender_id] != self.vector_clock[sender_id] + 1:
            return False

        # Check if the matrix clock condition is satisfied (all dependencies are met)
        for i in range(self.num_processes):
            if i != sender_id and vector_timestamp[i] > self.vector_clock[i]:
                return False

        return True  # The message can be safely delivered

    def deliver_message(self, message, sender_id, vector_timestamp):
        # Update vector clock and matrix clock upon message delivery
        self.vector_clock[sender_id] += 1
        self.delivered_messages.append((message, sender_id, vector_timestamp))  # Log the delivered message

        # Update matrix clock to reflect knowledge of other processes
        for i in range(self.num_processes):
            self.matrix_clock[self.process_id][i] = max(self.matrix_clock[self.process_id][i], vector_timestamp[i])
        print(f"Process {self.process_id} delivered message from {sender_id}: '{message}' at Vector Clock: {self.vector_clock}")


def simulate():
    num_processes = 3
    process_A = BSSProcess(0, num_processes)
    process_B = BSSProcess(1, num_processes)
    process_C = BSSProcess(2, num_processes)
    # Simulate message exchanges between processes
    process_A.send_message("Hello from A", [process_B, process_C])
    time.sleep(0.1)
    process_B.send_message("Reply from B", [process_A, process_C])
    time.sleep(0.1)
    process_C.send_message("Message from C", [process_A, process_B])


simulate()
