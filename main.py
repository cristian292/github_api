import requests,json,re,sys,urllib3

def get_activity(username):
    url = f"https://api.github.com/users/{username}/events/public"
    response = None
    try:
        response = requests.get(url)
    except (requests.exceptions.ConnectionError,urllib3.exceptions.NameResolutionError):
        print("Failed to connect!")
        return 
    
    if response.status_code == 200:   
        with open("info.json", mode="w") as file:
            json.dump(response.json(), file, indent=4)
        with open("info.json", mode="r") as file:
            data = json.load(file)

        current = {}

        for event in data:
            tip = event.get("type")
            name = event.get("repo", {}).get("name")
            action = event.get("payload", {}).get("action")

            if action:
                key = (tip,name,action)
            else:
                key = (tip,name,None)
            current[key] = current.get(key, 0) +1

        for (tip,name,action),value in current.items():
            x = tip
            match x:
                case "PushEvent":
                    print(f"Pushed {value} commit/commits in {name}")
                case "WatchEvent":
                    print(f"Starred {name}")
                case "IssuesEvent":
                    if action == "opened":
                        print(f"Opened {value} new issue/issues in {name}")
                    if action == "closed":
                        print(f"Closed {value} issue/issues in {name}") 
                case "IssueCommentEvent" | "PullRequestReviewEvent" | "PullRequestReviewCommentEvent" | "PullRequestEvent" | "ReleaseEvent" :
                    x = action.capitalize()
                    parts = re.findall(r'[A-Z][a-z]*', tip)
                    try:
                        y = f"{parts[0]} {parts[1]} {parts[2]}"
                    except IndexError:
                        y = f"{parts[0]} {parts[1]}"
                    print(f"{x} a {y} in {name}")
                case "CreateEvent": 
                    print(f"Created an event in {name}")
    else:
        print("Error fetching events for {username}: {response.status_code} ")
    
if __name__ == "__main__":
    if (len(sys.argv))>1:
        get_activity(sys.argv[1])
    

        



