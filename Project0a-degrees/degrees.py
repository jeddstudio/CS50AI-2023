import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


##############################  📝 Notes  ##############################
########## Change to the `load_data(directory)` to `load_data("small")` for switch to the small dataset ########## 
def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    ########## HERE change directory or "small" ##########
    load_data(directory)
    ########## HERE change directory or "small" ##########
    print("Data loaded.")


    source = person_id_for_name(input("Name: "))
    # source = person_id_for_name("tom hanks") # for testing
    # source = person_id_for_name("cary elwes") # for testing
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    # target = person_id_for_name("tom cruise") # for testing
    # target = person_id_for_name("chris sarandon") # for testing
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)
    print(f"path: {path}")

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")



##############################  Edit this part  ##############################
##############################  Edit this part  ##############################
##############################  Edit this part  ##############################

def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    ### Name for testing in small folder csv file###  
    # source_Name: cary elwes (144)
    # target_Name: chris sarandon (1697)
    # related_movie: "The Princess Bride",1987 (93779)


    # source = 144 
    start_state = Node(state=source, parent=None, action=None)

    # Change `frontier = StackFrontier()` to use DFS
        # It take so long...
    frontier = QueueFrontier() # Use "queue" aka the BFS algorithm
    # Put the node into frontier
    frontier.add(start_state) # this `.add()` come from `class StackFrontier()`

    # Initialize an empty explored set
    # This is the Explored Set contain what we are explored
    explored = set()


    # Keep looping until solution found
        # Or frontier is empty
    while not frontier.empty():
        # If nothing left in frontier, then NO RELATION
        if frontier.empty():
            return None # Give the None to def main(), it will print("Not connected.")
        
        # Remove a node from frontier and become a new state
        node = frontier.remove()
        # print(f"node.state == target: {node.state} == {target}")


        # Check if the actor in the node is the target actor
        # The first round `node.state == target` is: 144 == 1697
            # which is False
        # So keep going to next node
        if node.state == target:
            # Contain that what we will return 
            path = []

            # If no parent node, we are in the starting node
            while node.parent is not None:
                path.append((node.action, node.state))
                # print(f"append {node.action}, {node.state}")
                # print(f"path: {path}")
                node = node.parent
            path.reverse() # Python built-in method to make: [Target, C, B, Source] >>>> [Source, B, C, Target]
            return path # This is what we are finally return to `def main()`
        
        # Because if is False, it will go to next line
            # So no "else" here

        # Because the first node(`node.state`, 144) isn't 1697
        # So add it to `explored`
        explored.add(node.state)
        # print(explored)
        # print(f"node.state: {neighbors_for_person(node.state)}")


        # if node.state == target is (False)
        # Find the friend of friend
        # list all the movies and friends of current `node`
        current_node_data = neighbors_for_person(node.state) # {('93779', '1597'), ('93779', '144'), ('93779', '1697'), ('93779', '705')}}
    
        # Check if movies and friends not in `explored` and `frontier`
            # add them to `explored`
        for movie_id, person_id in current_node_data:
            # if `frontier.contains_state(person_id)`= False, it is not in the `frontier`
            if not frontier.contains_state(person_id) and person_id not in explored: 
                # if the id in frontier(True), it means it will be a node in coming round, so don't need to add it into `explored`
                # if the id already in `explored`, it means it was exlpored

                # Create a child node
                # By adding `movie_id` to the action here, 
                    # it can add "friends of friends" from the movies that your friends have acted in.
                        # and iterate to add  "friends of friends os friends"
                child = Node(state=person_id, parent=node, action=movie_id)
                frontier.add(child)

    # If loop through all data and haven't found the target, return None      
    return None


##############################  Edit this part  ##############################
##############################  Edit this part  ##############################
##############################  Edit this part  ##########################



def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()