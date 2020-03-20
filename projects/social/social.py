import random
from util import Stack, Queue  # These may come in handy

class User:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def get_neighbors(self, user_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.friendships[user_id]    

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments
        Creates that number of users and a randomly distributed friendships
        between those users.
        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
        for i in range(num_users):
            self.add_user(f"User {i+1}")

        # Create friendships
        # create a list with all possible friendships
        possible_friendships = []
        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))


        # Shuffle the list
        random.shuffle(possible_friendships)
        # print("----")
        # print(possible_friendships)
        # print("----")
        # Grab the first N pairs from the list and create those friendships
        for i in range(num_users * avg_friendships // 2):
            friendship = possible_friendships[i]
            self.add_friendship(friendship[0], friendship[1])

        # avg_friendships = total_friendships / num_users
        # total_friendships = avg_friendships * num_users
        # N = avg_friendships * num_users // 2

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # Create an empty queue
        q = Queue()
        # Add A PATH TO the starting vertex_id to the queue
        q.enqueue([starting_vertex])
        # Create an empty set to store visited nodes
        visited = set()
        # While the queue is not empty...
        while q.size() > 0:
            # Dequeue, the first PATH
            p = q.dequeue()
            # GRAB THE LAST VERTEX FROM THE PATH
            last_vertex = p[-1]
            # CHECK IF IT'S THE TARGET
            if last_vertex == destination_vertex:
                return p
                # IF SO, RETURN THE PATH    
            # Check if it's been visited
            if last_vertex not in visited:
            # If it has not been visited...
                # Mark it as visited
                visited.add(last_vertex)
                # Then add A PATH TO all neighbors to the back of the queue
                    # (Make a copy of the path before adding)
                for neighbor in self.get_neighbors(last_vertex):
                    copy = p.copy()
                    copy.append(neighbor)
                    q.enqueue(copy)     


    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument
        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.
        The key is the friend's ID and the value is the path.
        """
        # visited = {}  # Note that this is a dictionary, not a set
        # # !!!! IMPLEMENT ME
        # return visited
        # Create an empty stack
        s = Stack()
        # Push the starting vertex_id to the stack
        s.push(user_id)
        # Create an empty set to store visited nodes
        visited = {}
        # While the stack is not empty...
        while s.size() > 0:
            # Pop the first vertex
            v = s.pop()
            # Check if it's been visited
            # If it has not been visited...
            if v not in visited:
                # Mark it as visited
                #print(v)
                path = self.bfs(user_id, v)
                visited[v] = path
                # Then push all neighbors to the top of the stack
                for neighbor in self.get_neighbors(v):
                    s.push(neighbor)
        return visited

if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.users)
    print(sg.friendships)
    print(sg.get_neighbors(6))
    print(sg.get_neighbors(4))
    connections = sg.get_all_social_paths(1)
    print((connections))