class Node(object):
    rootNode = None
    nodeList = {}
    nameList = {}

    # constructor
    def __init__(self, nodeId, name, parent):
        if nodeId == '' or name == '':
            raise Exception('id and name must be specified and not empty strings')

        if parent != '':
            try:
                self.createNode(nodeId, name, parent)
            except:
                raise

        else:
            self.createRoot(nodeId, name)


    # creating Root
    def createRoot(self, nodeId, name):
        try:
            if Node.rootNode:
                raise Exception('root node already exists')
            
            self.fillValues(nodeId, '', name)

            Node.rootNode = nodeId 
            Node.nodeList[nodeId] = self
        
        except:
            raise

    # creating node
    def createNode(self, nodeId, name, parent):
        try:
            parentNode = self.getNode(parent)
        except KeyError:
            raise Exception('parent node does node exist')
          
        for childId in parentNode.children:
            childNode = self.getNode(childId)
            if childNode.name == name:
                raise Exception('parent node already has child with the same name')
        
        try:
            self.getNode(nodeId) # raises a keyError if node does not exists
            raise Exception('node with this id already exists')
        except KeyError:
            parentNode.children.append(nodeId)
            parentNode.childrenNames.append(name)

            self.fillValues(nodeId, parent, name)

            try:
                Node.nameList[parent][name] = self
            except KeyError:
                Node.nameList[parent] = {}
                Node.nameList[parent][name] = self

    def fillValues(self, nodeId, parentId, name):
        self.id = nodeId
        self.parent = parentId
        self.name = name
        self.children = []
        self.childrenNames = []
        Node.nodeList[nodeId] = self

    # delete node
    def deleteNode(nodeId):
        if not nodeId or nodeId == '':
            raise Exception('ID must be specified and not an empty string.')

        try:
            node = Node.getNode(None, nodeId)
        except KeyError:
            raise Exception('Node not exist')

        if len(node.children):
            raise Exception('Node must not have children')

        #removing id from parent lists
        parent = node.getNode(node.parent)
        parent.children.remove(node.id)
        parent.childrenNames.remove(node.name)

        #removing id and name from class
        del Node.nodeList[node.id]
        del Node.nameList[node.parent][node.name]


    # moving node
    def moveNode(nodeId, parentId):
        if not nodeId or nodeId == '' or not parentId or parentId == '':
            raise Exception('ID and parent ID must be specified and not an empty strings.')
        
        try:
            node = Node.getNode(None, nodeId)
            parent = Node.getNode(None, parentId)
        except KeyError:
            raise
        
        if node.parent == '':
          raise Exception('cannot move root node')


        if node.name in parent.childrenNames:
          raise Exception('parent already has child with the same name')

        newParent = parent

        # check if we can reach the root
        while True:
            if parent.parent == '':
                break

            if parent.id == node.id:
                raise Exception('Move must not create a cycle in the tree')

            parent = parent.getNode(parent.parent)

        oldParent = node.getNode(node.parent)
        node.parent = parentId

        oldParent.children.remove(node.id)
        oldParent.childrenNames.remove(node.name)

        del Node.nameList[oldParent.id][node.name]
        Node.nameList[newParent.id][node.name] = node

        newParent.children.append(node.id)
        newParent.childrenNames.append(node.name)


    def getNode(self, nodeId):
        try:
            node = Node.nodeList[nodeId]
            return node
        except KeyError:
            raise


    def getNodeByName(self, name, parent):
        try:
            node = Node.nameList[parent][name]
            return node
        except KeyError:
            raise


    def getSiblings(self, depth, nodes, minDepth, maxDepth):
        if maxDepth > 0 and depth > maxDepth:
            return 

        if minDepth > 0 and depth >= minDepth: 
            nodes.append({'id': self.id, 'name': self.name, 'parent_id': self.parent})

        if minDepth == 0:
            nodes.append({'id': self.id, 'name': self.name, 'parent_id': self.parent})

        for childName in sorted(self.childrenNames):
            self.getNodeByName(childName, self.id).getSiblings(depth + 1, nodes, minDepth, maxDepth)


    def getTree(self, minDepth, maxDepth, names, ids, rootIds):
        nodes = []
        
        if len(rootIds):
            for rootId in rootIds:
                try:
                    Node.getNode(None, rootId).getSiblings(0, nodes, minDepth, maxDepth)
                except KeyError:
                    continue

        else:
            root = Node.getNode(None, Node.rootNode)
            root.getSiblings(0, nodes, minDepth, maxDepth)

        #filter by name
        if len(names):
            for node in nodes.copy():
                if node['name'] not in names:
                    nodes.remove(node)

        # filter by id
        if len(ids):
            for node in nodes.copy():
                if node['id'] not in ids:
                    nodes.remove(node)

        return nodes


    # print helper for debugging
    def __str__(self):
        try:
            return self.id + ':' + self.name + ':parent - ' + self.parent
        except AttributeError:
            return self.id + ':' + self.name + ':root'
