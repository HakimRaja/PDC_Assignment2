## Causal Ordering Algorithms 

This repository contains the implementation of Causal Ordering Algorithms using Python, focusing on the following algorithms:

BSS Algorithm: Maintains message order by using vector clocks and message queues.

SES Algorithm: Uses vector clocks for ordering and matrix clocks for tracking dependencies.

Matrix Clock: Tracks dependencies by maintaining a matrix for all processes' clocks.

# The code implementation includes:

BSS-based Causal Ordering Algorithm

SES and Matrix Clock Mechanisms

The implementation simulates message passing between processes and ensures messages are delivered in the correct causal order.

## How to Run the Code

Clone the repository.

Run the files using Python:
    python CausalOrdering.py
    python CausalOrdering2.py

## Output Explanation

The output shows messages being delivered in the correct causal order with their vector clocks. The vector clocks ensure that each process updates its state only when all dependencies are satisfied.

## Author

Hakim Mahfooz Raja
