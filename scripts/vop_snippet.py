import hou, json, os, os.path as ospath
host_value = {'app' : 0, 'ind' : 1, 'com' : 2}


def writeList(hou, file_path = '', node_list=None):
    ''' This function creates the JSON content out of the provided list of nodes'''
    # grabs a collection of selected nodes
    if node_list == None:
        node_list = hou.selectedNodes()
    if node_list == ():
        return
    # creates various dictionaries to populate JSON
    data = {}
    nodes = {}
    connections = {}
    # run through nodes collectiong info
    for node in node_list:
        # dictionary to contain changed parms and values
        parms = {}
        # run through nodes' parms checkign for changed defaults
        for parm in node.parms():
            if parm.isAtDefault() == False:
                parms[parm.name()] = parm.eval()
        # populate nodes part of JSON dictionary
        nodes[node.name()] = dict(zip(['type','parms'], [node.type().name(), parms]))
        # populate connections part of dictionary
        connections[node.name()] = []
        for connection in node.inputConnections():
            connections[node.name()].append(dict({connection.inputNode().name():(connection.inputIndex(), connection.outputIndex())}))
    data['nodes'] = nodes
    data['connections'] = connections
    data['host'] = {'host' : keyGen()}
    # write JSON file to disk
    if file_path == '':
        file_path = hou.expandString(hou.ui.selectFile(pattern='*.json', chooser_mode=hou.fileChooserMode.Write))
    else:
        file_path = hou.expandString(hou.ui.selectFile(start_directory=file_path, pattern='*.json', chooser_mode=hou.fileChooserMode.Write))
    try:
        with open(file_path, 'w') as json_write:
            json_write.write(json.dumps(data, indent=4, separators=(',', ': ')))
    except IOError:
        hou.ui.setStatusMessage("Could not write snippet...")
        return -1
    hou.ui.setStatusMessage("Successfully wrote snippet as: " + file_path)
    return 0

def readList(hou, file_path=''):
    ''' This function parses data from JSON file and returns dictionaries with nodes and connections to be created'''
    # pick file with preset
    if file_path == '':
        file_path = hou.expandString(hou.ui.selectFile(pattern='*.json', chooser_mode=hou.fileChooserMode.Read))
    else:
        file_path = hou.expandString(hou.ui.selectFile(start_directory=file_path, pattern='*.json', chooser_mode=hou.fileChooserMode.Read))
    # container for all the data to be read from JSON file
    data = {}
    try:
        with open(file_path, 'r') as json_data:
            data = json.load(json_data)
    except IOError:
        hou.ui.setStatusMessage("Could not read snippet...")
        return -1
    nodes = dict(zip(data['nodes'].keys(), data['nodes'].values()))
    connections = dict(zip(data['connections'].keys(), data['connections'].values()))
    host = dict(zip(data['host'].keys(), data['host'].values()))
    if keyCheck(host['host']) == False:
        raise Exception('Snippet cannot be executed in this system.\nCheck your license type')
    # determine location to create vop nodes
    net_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    cur_node = net_editor.pwd()
    if not isVopContainer(cur_node):
        node_path = hou.ui.selectNode(relative_to_node=None, initial_node=cur_node, node_type_filter=None)
        if node_path is not None:
            cur_node = hou.node(node_path)
        else:
            raise TypeError
    return cur_node, nodes, connections

def createNodes(hou, cur_node, nodes, connections):
    ''' This function creates nodes and connections from the supplied dictionaries'''
    # a container for the newly created nodes
    created_node = {}
    # node creation part of the process
    for node in nodes.keys():
        created_node[node] = cur_node.createNode(nodes[node]['type'], node_name=node)
        for parm_name in nodes[node]['parms'].keys():
            created_node[node].parm(parm_name).set(nodes[node]['parms'][parm_name])
    # connecting part of the process
    for connection in connections.keys():
        in_node = created_node[connection]
        for out_connection in connections[connection]:
            for item in out_connection.keys():
                out_node = None
                # check if node is among newly created nodes
                if item in created_node.keys():
                    out_node = created_node[item]
                else:
                    # otherwise, assume it already exists within the current network
                    out_node = hou.node(cur_node.path() + '/' + item)
                # if none of the previous steps worked skips the connection step
                if out_node != None:
                    input_index = out_connection[item][0]
                    output_index = out_connection[item][1]
                    in_node.setInput(input_index, out_node, output_index)
    # layout the newly created nodes
    layout_nodes = tuple([created_node[key] for key in created_node.keys()])
    cur_node.layoutChildren(items = layout_nodes)
    return 0

def isVopContainer(node):
    ''' This function checks if a node belongs to any of the select VOP network categories'''
    vopTypes = ['attribvop', 'volumevop', 'popvop', 'gasfieldvop', 'geometryvop', 'vopforce']
    if node.type().name() in vopTypes:
        return True
    return False

def readSnippet(hou, file_path):
    ''' This function creates the nodes and connections from a JSON file. It's menant to be invoked from a shelf script'''
    try:
        cur_node, nodes, connections = readList(hou, file_path)
    except TypeError:
        hou.ui.setStatusMessage("Could recreate nodes from snippet...")
        return -1
    createNodes(hou, cur_node, nodes, connections)
    return 0

def keyGen():
    ''' This function generates a validation key for host app'''
    if hou.isApprentice():
        return 'app'
    else:
        if hou.applicationName() == 'hindie':
            return 'ind'
        else:
            return 'com'

def keyCheck(cur_host):
    ''' This function checks for the validation key to activate script'''
    if host_value[cur_host] >= host_value[keyGen()]:
        return True
    return False