"""This script contains a Queue that signals orders
"""

import queue

order_queue = queue.Queue()
order = {
    'session_id': 'demo_session',
    'order_info': {
        'symbol': 'VET/USDT',
        'side': 'sell',
        'amount': 1000
    }
}
order_queue.put(order)
