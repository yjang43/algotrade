"""This script contains a Queue that signals orders
"""

import queue

order_queue = queue.Queue()
order0 = {
    'session_id': 'demo_session',
    'order_info': {
        'symbol': 'VET/USDT',
        'side': 'sell',
        'amount': 1000
    }
}
order1 = {
    'session_id': 'demo_session',
    'order_info': {
        'symbol': 'NULS/USDT',
        'side': 'sell',
        'amount': 1000
    }
}
order_queue.put(order0)
order_queue.put(order1)


"""structure
{string: Session}"""
session_container = {}
