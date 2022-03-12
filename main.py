import difflib
import socket


def display_data(matches):
    result = ""
    with open(f"info/{matches[0]}.site", "r") as file:
        for fact in file.readlines():
            result += fact + "\n"

    return matches[0], result


def search_topic(search_key):
    with open(f"meta/topics.txt", "r") as file:
        topics = file.read().splitlines()

    high_matches = difflib.get_close_matches(search_key, topics, cutoff=0.75)
    low_matches = list(set(difflib.get_close_matches(search_key, topics, cutoff=0.5)) - set(high_matches))

    if len(high_matches) != 0:
        if high_matches[0] == search_key:
            key, result = display_data(low_matches)
            return key, result, "Exact Match"
        else:
            key, result = display_data(low_matches)
            return key, result, "Close Match"

    elif len(low_matches) != 0:
        key, result = display_data(low_matches)
        return key, result, "Low Match"

    else:
        return search_key, "No Matches Were Found.", "No Match"


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 5000

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((HOST, PORT))
    listener.listen(1)
    print(f"The Server Is Listening On https://{HOST}:{PORT}")

    while True:
        client_connection, client_address = listener.accept()
        data = client_connection.recv(1024).splitlines()

        resource = data[0].decode('utf-8')

        if resource.find("GET") == -1:
            continue

        information = resource.split(" ")[1][1:]

        if information.endswith(".ico"):
            continue

        key, result, rtype = search_topic(information)
        to_send = {"Response Type": rtype, key: result}
        response = f"""HTTP/1.1 200 OK\n\n{to_send}"""

        client_connection.sendall(response.encode())
        client_connection.close()
