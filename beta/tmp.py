"""This script contains a Queue that signals orders
"""

import queue

order_queue = queue.Queue()
order = (
    'demo_session',
    {
        'symbol': 'VET/USDT',
        'side': 'buy',
        'amount': 1000
    }
)
order_queue.put(order)
