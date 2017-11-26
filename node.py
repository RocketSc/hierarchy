class Node(object):
    rootNode = None
    nodeList = {}
    nameList = {}


    def __init__(self, nodeId, name, parentId):
        if nodeId == '' or name == '':
            raise Exception('id and name must be specified and not empty strings')

        if parentId != '':
            try:
                self.createNode(nodeId, name, parentId)
            except:
                raise

        else:
            self.createRoot(nodeId, name)


    def createRoot(self, nodeId, name):
        try:
            if Node.rootNode:
                raise Exception('root node already exists')
            
            self.fillValues(nodeId, '', name)

            Node.rootNode = nodeId 
            Node.nodeList[nodeId] = self
        
        except:
            raise


    def createNode(self, nodeId, name, parentId):
        try:
            parentNode = self.getNode(parentId)
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
            self.fillValues(nodeId, parentId, name)
            parentNode.registerChild(self)

            try:
                Node.nameList[parentId][name] = self
            except KeyError:
                Node.nameList[parentId] = {}
                Node.nameList[parentId][name] = self
    

    def registerChild(self, child):
        self.children.append(child.id)
        self.childrenNames.append(child.name)


    def unregisterChild(self, child):
        self.children.remove(child.id)
        self.childrenNames.remove(child.name)


    def fillValues(self, nodeId, parentId, name):
        self.id = nodeId
        self.parentId = parentId
        self.name = name
        self.children = []
        self.childrenNames = []
        Node.nodeList[nodeId] = self


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
        parent = node.getNode(node.parentId)
        parent.unregisterChild(node)

        #removing id and name from class
        del Node.nodeList[node.id]
        del Node.nameList[node.parentId][node.name]


    def moveNode(nodeId, parentId):
        """
        Throws KeyError if nodes were not found
        """
        if not nodeId or nodeId == '' or not parentId or parentId == '':
            raise Exception('ID and parent ID must be specified and not an empty strings.')
        
        node = Node.getNode(None, nodeId)
        parent = Node.getNode(None, parentId)
        
        if node.parentId == '':
          raise Exception('cannot move root node')


        if node.name in parent.childrenNames:
          raise Exception('parent already has child with the same name')

        newParent = parent

        # check if we can reach the root
        while True:
            if parent.parentId == '':
                break

            if parent.id == node.id:
                raise Exception('Move must not create a cycle in the tree')

            parent = parent.getNode(parent.parentId)

        oldParent = node.getNode(node.parentId)
        node.parentId = newParent.id

        oldParent.unregisterChild(node)
        newParent.registerChild(node)

        del Node.nameList[oldParent.id][node.name]
        Node.nameList[newParent.id][node.name] = node


    def getNode(self, nodeId):
        """
        Throws KeyError if there is no node with provided id
        """
        node = Node.nodeList[nodeId]
        return node


    def getNodeByName(self, name, parentId):
        """
        Throws KeyError if parent doesn't have node with provided name
        """
        node = Node.nameList[parentId][name]
        return node


    def getSiblings(self, depth, nodes, minDepth, maxDepth):
        if maxDepth > 0 and depth > maxDepth:
            return 

        if minDepth > 0 and depth >= minDepth: 
            nodes.append({'id': self.id, 'name': self.name, 'parent_id': self.parentId})

        if minDepth == 0:
            nodes.append({'id': self.id, 'name': self.name, 'parent_id': self.parentId})

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
            return self.id + ':' + self.name + ':parent - ' + self.parentId
        except AttributeError:
            return self.id + ':' + self.name + ':root'
