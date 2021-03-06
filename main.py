# Authors: Joshua Go, Evan Swanson, Mauricio Velazquez
# Course: CPSC 450
# Assignment: Final Project
# Usage: python3 main.py [test file name]
# Description:
#   
# ----------------------------------------------------------------------
#  Killer Feature 1: 
#      Recommended friends.
#      We would go through all of a user's friends'
#      friends and count up how many of them are recurring throughout and 
#      has a relatively high friendship leve. 
#      If the friend that popped up the most is not friends with the user, 
#      it will be a recommended friend. 
# ----------------------------------------------------------------------
#  Killer Feature 2: 
#      We calculate a "top chart", where we take into consideration 
#      both the amount of friends and the "quality" of friends. Meaning that this
#      feature would output the list of all users ranked from top to bottom. We 
#      Calculate their "score" by averiging out their overall level of friendship
#      and muiltiply it their number of friends. 
# ----------------------------------------------------------------------
#  Best Friend Chain Algorithm
#       In  order to solve this we will use Dijkstra’s algorithm
# ----------------------------------------------------------------------

import sys
import copy
import operator

def main(filename):
    try:
        file_stream = open(filename, 'r')
        userDictionary, adjacencyList = read_file(file_stream) 
        file_stream.close()
    except FileNotFoundError:
        sys.exit('invalid filename %s' % filename)
    userChoice = 0
    while(userChoice != "6"):
        print("What do you want to do?")
        print("1) Check if user exists")
        print("2) Check connection between users")
        print("3) Friend chain")
        print("4) Top Chart")
        print("5) Recommend friend")
        print("6) Quit")
        userChoice = input()
        #just test cases, replace with actual params
        doChoice(userChoice, userDictionary, adjacencyList)

# reads file
def read_file(filename):
    adj_list = []   # adjacency list containing friends of the users based on the users index
    user_dict = {}    # dictionary containing the users and their corresponding index
    every_three = 0     # resets counter every 3 iterations
    index = 0   # keeps track of index of the adjacency list
    user = None
    users_friend = None
    for i in filename.read().split(): 
        if every_three == 0:
            user = i
            if not i in user_dict:
                user_dict.update({i : index})     # add user to the user dictionary  
                index += 1  # update index
        elif every_three == 1:
            users_friend = i
        else:
            users_friends_dict = {users_friend : i}  # add the users friend to a dictionary
            user_index = user_dict.get(user)
            if user_index >= len(adj_list):
                adj_list.append(users_friends_dict)     # add new dictionary to the adjacency list
            else:
                adj_list[user_index][users_friend] = i

        every_three += 1
        if every_three == 3:    # reset to 0 every 3 iterations
            every_three = 0
    # loop through adj_list and add users who have no friends to user_dict
    for i, entry in enumerate(adj_list):
        for adj_key in [*adj_list[i]]:
            if adj_key not in user_dict:
                user_dict.update({adj_key: -1})
    print(user_dict)
    return user_dict, adj_list
    
def doChoice(userChoice, userDictionary, graph):
    if userChoice == "1":
        checkName = input("Enter the users name > ")
        if checkName in userDictionary:
            print(checkName + " exists")
        else:
            print(checkName + " does not exist")
    elif userChoice == "2":
        names = input("What users (seperated by spaces) > ")
        names = names.split()
        if names[1] in graph[userDictionary[names[0]]]:
            weight = graph[userDictionary[names[0]]][names[1]]
            print("The connection from " + names[0] + " to " + names[1] + " has weight " + str(weight))
        else:
            print("No connection between names")
    elif userChoice == "3":
        Dijkstra(userDictionary, graph)
    elif userChoice == "4":
        topChart(userDictionary, graph)
    elif userChoice == "5":
        recommendFriend(userDictionary, graph)

def topChart(Dict, graph):
    totalVals = {}
    for users in Dict:
        index = 0
        total = 0
        for edges in graph:
            for vals in edges:
                if users == vals:
                    total = total + (int(edges.get(vals)))
        # print(users)
        # print(total)
        totalVals.update({users:total})

        index = index + 1
    orderedIndex = sorted(totalVals.items(), key=lambda kv: kv[1], reverse = True)
    print(orderedIndex)

    print("\n\n...........Top Chart...........")
    index = 1
    for x in orderedIndex:
        name = x[0]
        number = x[1]
        print (str(index) + ") " + f"{name:<15}{number:>12}")
        index = index + 1

    print("\n\n")

def getKey(val, Dict): 
    for key, value in Dict.items(): 
         if val == value: 
             return key 

def minDistance(dist, sptSet):
    min = float("inf")
    min_index = 0
    for v in range(len(dist)):
        if dist[v] < min and sptSet[v] == False:
            min = dist[v]
            min_index = v
    return min_index

def Dijkstra(userDictionary, graph):
    names = input("What users (seperated by spaces) > ")
    names = names.split()
    numVert = len(graph)
    parent = [-1] * numVert
    #make a copy of the graph to transform
    adjacencyList = copy.deepcopy(graph)

    
    #transform each weight to 10 - itself
    for x in range(len(adjacencyList)):
        for key, val in adjacencyList[x].items():
            adjacencyList[x][key] = 10 - int(val)

    #initialize distances list
    dist = [float("inf")] * numVert
    dist[userDictionary[names[0]]] = 0
    sptSet = [False] * numVert

    for cout in range(numVert):
        u = minDistance(dist, sptSet)
        sptSet[u] = True
        #break if we made it to our destination
        if list(userDictionary.keys())[list(userDictionary.values()).index(u)] == names[1]:
            break

        for name,val in adjacencyList[u].items():
            v = userDictionary[name]
            if sptSet[v] == False and dist[v] > dist[u] + int(val):
                dist[v] = dist[u] + int(val)
                parent[userDictionary[name]] = u

    printPath(parent, userDictionary[names[1]], userDictionary)

def printPath(parent, j, userDictionary):
    #Base Case : If j is source 
    if parent[j] == -1 :  
        print(' -' + list(userDictionary.keys())[list(userDictionary.values()).index(j)])
        return
    printPath(parent , parent[j], userDictionary) 
    print(' -' + list(userDictionary.keys())[list(userDictionary.values()).index(j)])


def recommendFriend(userDictionary, adjacencyList):
    name = input("Enter the user to recommend a friend to: ")
    friendCount = {}
    #go through each of the user's friends
    for friend, value in adjacencyList[userDictionary[name]].items():
        #go through this person's friends and add to count dictionary
        for person in adjacencyList[userDictionary[friend]]:
            if person in friendCount:
                friendCount[person] += int(adjacencyList[userDictionary[friend]][person]) #the weight of the friendship
            else:
                friendCount[person] = int(adjacencyList[userDictionary[friend]][person])
    
   
    #remove the person themselves
    if name in friendCount:
        del friendCount[name]
    print(friendCount)
    delPeople = max(friendCount, key=friendCount.get) in adjacencyList[userDictionary[name]]
    #remove people who are already friends with the person
    while delPeople:
        del friendCount[max(friendCount, key=friendCount.get)]
        if len(friendCount) == 0:
            print("No friends to recommend")
            delPeople = False
        else:
            delPeople = max(friendCount, key=friendCount.get) in adjacencyList[userDictionary[name]]

    #output the top candidate
    if len(friendCount) != 0:
        print(max(friendCount, key=friendCount.get))


# takes in command line arguments to execute program
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Usage: %s file' % sys.argv[0])
    main(sys.argv[1])