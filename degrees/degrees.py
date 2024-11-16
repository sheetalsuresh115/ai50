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
    # Load information from people.csv
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

    # Load movie information from movies.csv
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


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    # Fetch the person id for the source name entered.
    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")

    # Fetch the person id for the target name entered.
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    # Finds the connection between both the stars.
    path = shortest_path(source, target)

    if path is None:
        # If the stars have no connection path will be None
        print("Not connected.")
    else:
        # The degrees of separation is found and displayed.
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        if degrees > 0:
            path = [(None, source)] + path
            for i in range(degrees):
                person1 = people[path[i][1]]["name"]
                person2 = people[path[i + 1][1]]["name"]
                movie = movies[path[i + 1][0]]["title"]
                print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    stars_connected = False
    num_explored = 0
    explored_sets = QueueFrontier()

    start = Node(source, None, None)
    queue = QueueFrontier()
    queue.add(start)

    actions, cells = [], []
    # If the source and target stars are the same, the path is empty.
    if source == target:
        return []

    # As long as the connection between stars are not found and
    # We start with the source id to find the connection.
    while not queue.empty() and not stars_connected:
        node = queue.remove()

        if not explored_sets.contains_state(node.state):
            # Explored sets keeps track of all the person's we have explored.
            explored_sets.add(node)

            # Here we explore all the co-stars, movies the person has acted in.
            for movie_id, person_id in neighbors_for_person(node.state):
                child = Node(state=person_id, parent=node, action=movie_id)
                if child.state == target:
                    # If one of the co-stars are the target, we have found the connection.
                    stars_connected = True
                    break
                # If the co-star is not the target, we add them to the queue to check for
                # next degree of connection.
                queue.add(child)

        if stars_connected:
            # If we did find the connection, then we have to return the movie and the person id
            solution = [(child.action, child.state)]
            parent = child.parent

            # Since we traversed into the target connection,
            # The path has to be reversed to show the connection from the source to the target.
            while parent.action:
                solution.insert(0, (parent.action, parent.state))
                parent = parent.parent
            return solution

    return None


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