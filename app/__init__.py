from flask import Flask
import datetime
from hashring import *
import string

# Flask App initialization
app = Flask(__name__)
app.secret_key = 'secret_key'

DEFAULT_NODE_COUNT = 3
DEFAULT_NODE_WEIGHT = 10
DEFAULT_KEY_COUNT = 500
NODE_PREFIX_LENGTH = 5
PLOT_RADIUS = 2
NODE_PREFIX = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(NODE_PREFIX_LENGTH))
NODES = [NODE_PREFIX + '-' + str(i) for i in range(DEFAULT_NODE_COUNT)]
KEYS = generate_random(DEFAULT_KEY_COUNT, 100000)
hc = HashCircle(KEYS, [], NODE_PREFIX_LENGTH, DEFAULT_NODE_WEIGHT)

for i in NODES:
    hc.add_weighted_node(i, DEFAULT_NODE_WEIGHT, True)

from app import views
