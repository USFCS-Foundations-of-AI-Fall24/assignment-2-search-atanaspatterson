from collections import deque



## We will append tuples (state, "action") in the search queue
def breadth_first_search(startState, action_list, goal_test, use_closed_list=True) :
    numStates = 0
    search_queue = deque()
    closed_list = {}

    search_queue.append((startState,""))
    if use_closed_list :
        closed_list[startState] = True
    while len(search_queue) > 0:
        ## this is a (state, "action") tuple
        next_state = search_queue.popleft()
        if goal_test(next_state[0]):
            print("Goal found")
            print(next_state)
            print("Number of states generated = {}".format(numStates))
            print()
            # ptr = next_state[0]
            # while ptr is not None :
            #     ptr = ptr.prev
            #     print(ptr)
            return next_state
        else : 
            successors = next_state[0].successors(action_list)
            numStates += len(successors)
            if use_closed_list :
                successors = [item for item in successors
                                    if item[0] not in closed_list]
                for s in successors :
                    closed_list[s[0]] = True
            search_queue.extend(successors)

### Note the similarity to BFS - the only difference is the search queue

## use the limit parameter to implement depth-limited search
def depth_first_search(startState, action_list, goal_test, use_closed_list=True,limit=-1) :
    search_queue = deque()
    numStates = 0
    closed_list = {}

    search_queue.append((startState, "", 0))
    if use_closed_list :
        closed_list[startState] = True
    while len(search_queue) > 0:
        ## this is a (state, "action") tuple
        next_state = search_queue.pop()
        depth = next_state[2]

        if (limit != -1 and depth > limit):
            continue

        if goal_test(next_state[0]):
            print("Goal found")
            print(next_state)
            print("Number of states generated = {}".format(numStates))
            # ptr = next_state[0]
            # while ptr is not None :
            #     ptr = ptr.prev
            #     print(ptr)
            return next_state
        else :
            successors = next_state[0].successors(action_list)
            numStates += len(successors)
            if use_closed_list :
                successors = [item for item in successors
                                    if item[0] not in closed_list]
                for s in successors :
                    closed_list[s[0]] = True
                
            search_queue.extend((s[0], s[1], depth + 1) for s in successors)




