from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from util import Stack, Queue

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())

room_dict = {}
for key in room_graph:
    room_dict[key] = room_graph[key][1]

def get_adjacent(room_id):
    return room_dict[room_id]

world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
reverse_path = [] 
visited = {}
opposite_directions = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}

visited[player.current_room.id] = player.current_room.get_exits()
hubs = []

def shortest_path(starting_vertex, destination_vertex):
    

    q = Queue()
    q.enqueue([starting_vertex])
    visited = set()

    while q.size() > 0:
        p = q.dequeue()
        last_vertex = p[-1]
        if last_vertex == destination_vertex:
            return p
        if last_vertex not in visited:
            visited.add(last_vertex)
            for neighbor in get_adjacent(last_vertex).values():
                copy = p.copy()
                copy.append(neighbor)
                q.enqueue(copy) 




while len(visited) < len(room_graph)-1:
    for i in hubs:
        if len(visited[i]) == 0:
            hubs.remove(i)


    if player.current_room.id not in visited:
        visited[player.current_room.id] = player.current_room.get_exits()
        visited[player.current_room.id].remove(reverse_path[-1])

    # if we hit a dead end, do bfs
    if (len(visited[player.current_room.id]) == 0):
        if len(hubs) > 0:
            print(hubs)
            while player.current_room.id == hubs[-1]:
                hubs.pop()
            pathback = shortest_path(player.current_room.id, hubs[-1])
            pathback = pathback[1:]
            i = 0
            count=0
            print(player.current_room.id)
            print(pathback)
            while len(visited[player.current_room.id]) == 0 and player.current_room.id != pathback[-1]:
                currentRoom = player.current_room.id
                count += 1
                for key in room_dict[currentRoom]:
                    try: 
                        if room_dict[currentRoom][key] == pathback[i]:
                            
                            # pathback.remove(room_dict[player.current_room.id][key])
                            traversal_path.append(key)
                            player.travel(key)
                            i+=1
                    except:
                        i+=1
                        continue



        # while len(visited[player.current_room.id]) == 0:
        #     reverse_move = reverse_path.pop()
        #     traversal_path.append(reverse_move)
        #     player.travel(reverse_move)
    # print(player.current_room.id)
    if len(visited[player.current_room.id]) > 1:
        hubs.append(player.current_room.id)
    if len(visited[player.current_room.id]) > 0:
        dir = visited[player.current_room.id].pop(0)
    
    # print(visited[player.current_room.id])
    # print(traversal_path)
    try:
        if getattr(player.current_room, f"{dir}_to").id not in visited:
            reverse_path.append(opposite_directions[dir])
            traversal_path.append(dir)
            player.travel(dir)
    except:
        continue

    # print([i for i in room_dict if i not in visited])
    # else:
    #     traversal_path.append(dir)
    #     player.travel(dir)
    #     print(opposite_directions[dir])
    #     visited[player.current_room.id].remove(opposite_directions[dir])
    #     reverse_path = []
        
    # traversal_path.append(dir)
    # player.travel(dir)



# def dead_ended(r, lastroom):
#     if lastroom != -1:
#         for key in room_dict[r].keys():
#             if room_dict[r][key] == lastroom:
#                 return False
#         return True

# def get_direction(r, lastroom):
#     for key in room_dict[r].keys():
#         if key == "n":
#             if room_dict[r]['n'] == lastroom:
#                 return "s"
#         if key == "s":
#             if room_dict[r]['s'] == lastroom:
#                 return "n"
#         if key == "e":
#             if room_dict[r]['e'] == lastroom:
#                 return "w"
#         if key == "w":
#             if room_dict[r]['w'] == lastroom:
#                 return "e"

# def get_paths():
#     returnstack = Stack()
#     s=Stack()
#     s.push(player.current_room.id)
#     visited = []
#     shortpath = []
#     lastroom = 0
#     returnpoint = 0
#     while s.size() > 0:
#         r = s.pop()
#         if dead_ended(r, lastroom):
#             shortpath = [get_opposite(i) for i in shortpath if i]
#             shortpath.reverse()
#             traversal_path.extend(shortpath)
#             shortpath = []
#             lastroom = returnstack.pop()
#         if r not in visited:
#             visited.append(r)
#             shortpath.append(get_direction(r, lastroom))
#             traversal_path.append(get_direction(r, lastroom))
#             for i in range(len(room_dict[r].keys()) - 2):
#                 returnstack.push(r)
#                 shortpath = []
#             lastroom = r
#             for neighbor in list(get_adjacent(r).values()):
#                 s.push(neighbor)

#     return visited

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)
print(traversal_path)
for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
