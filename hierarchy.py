"""Hierarchy service"""

import json
from node import Node

# API
allowedCommands = ['add_node', 'delete_node', 'move_node', 'query']

def add_node(nodeObject):
    try:
        Node(nodeObject['id'], nodeObject['name'], nodeObject.get('parent_id', False))
        result = json.dumps({'ok': True})
    except:
        result = json.dumps({'ok': False})
    
    return result

def query(nodeObject):
    minDepth = nodeObject.get('min_depth', 0)
    maxDepth = nodeObject.get('max_depth', 0)
    names = nodeObject.get('names', [])
    ids = nodeObject.get('ids', []) 
    rootIds = nodeObject.get('root_ids', [])

    response = Node.getTree(None, minDepth, maxDepth, names, ids, rootIds)

    return json.dumps({'nodes': response})

def delete_node(nodeObject):
    nodeId = nodeObject.get('id', '')

    try:
        Node.deleteNode(nodeId)
        result = json.dumps({'ok': True})
    except:
        result = json.dumps({'ok': False})
    
    return result

def move_node(nodeObject):
    nodeId = nodeObject.get('id', '')
    parent = nodeObject.get('new_parent_id', '')
    
    try:
        Node.moveNode(nodeId, parent)
        result = json.dumps({'ok': True})
    except:
        result = json.dumps({'ok': False})

    return result


methods = globals().copy()

# Main cycle
while True:
    try:
        testInput = input()
    except EOFError:
        break

    command = json.loads(testInput) 

    filteredCommands = filter(lambda key: key in allowedCommands, command.keys())

    for func in filteredCommands:
        response = methods.get(func)(command[func])
        print(response)