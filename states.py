from enum import Enum

# states for tutorial text
class TutorialState(Enum):
    START = 'Add a router or a host to start!'
    HOST_ADDED = 'All elements can be dragged around! Add a router to continue.'
    ROUTER_ADDED = 'All elements can be dragged around! Add a host to continue.'
    NODES_ADDED = 'Awesome! Now select a router and a host using shift+click'\
                  ' and add a connection. You can type in the desired cost and'\
                  ' click "Add Connection"'
    CON_ADDED = 'Look at you! One last thing: to calculate the shortest path, '\
                'select two elements on your network graph and click "Shortest Path"'
    SP_SHOWN =  'Gread job! As you can see, the shortest path is highlighted in green.'\
                ' Click "clear" to finish the tutorial.'
    FINISH = ''
class ErrorState(Enum):
    OK = ''
    SELECT_1 = 'You need to select an element first!'
    SELECT_2 = 'You need to select exactly two elements! (use shift+click)'
    INV_COST = 'Entered cost is invalid!'
    HOST_HOST_CON = ''
    HOST_SECOND_CON = ''

# function that decides the final message
def msg(tut, err):
    if err == ErrorState.OK: return tut.value
    else:                    return err.value