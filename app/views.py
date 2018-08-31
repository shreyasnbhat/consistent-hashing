from flask import render_template, request, session, g
from app import *
import json


@app.route('/', methods=['GET', 'POST'])
def getHomePage():
    if request.method == 'GET':
        figure = hc.plot_all(PLOT_RADIUS)
        session['count'] = DEFAULT_NODE_COUNT
        x_history, y_history = slice(hc.remap_history)
        return render_template('homepage.html', figure=json.dumps(figure), x_history=x_history, y_history=y_history)


@app.route('/addNode', methods=['POST'])
def addNode():
    session['count'] += 1
    new_node_name = NODE_PREFIX + '-' + str(session['count'] - 1)
    hc.add_weighted_node(new_node_name, DEFAULT_NODE_WEIGHT, True)
    figure = hc.plot_all(PLOT_RADIUS)
    print("Added", new_node_name)
    x_history, y_history = slice(hc.remap_history)
    return render_template('homepage.html', figure=json.dumps(figure), x_history=x_history, y_history=y_history)


@app.route('/removeNode', methods=['POST'])
def removeNode():
    new_node_name = NODE_PREFIX + '-' + str(session['count'] - 1)
    session['count'] -= 1
    hc.remove_weighted_node(new_node_name, DEFAULT_NODE_WEIGHT, True)
    figure = hc.plot_all(PLOT_RADIUS)
    print("Removed", new_node_name)
    x_history, y_history = slice(hc.remap_history)
    return render_template('homepage.html', figure=json.dumps(figure), x_history=x_history, y_history=y_history)
