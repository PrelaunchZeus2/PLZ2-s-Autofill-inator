import cassiopeia as cass
import datetime

api_key = "RGAPI-f4c02da6-2e8e-4c94-9b25-e62f82ec5fca"
print("Your API key is: ", api_key)
summoner_name = input("\nPlease Enter The Starting Summoners Name: ")
region = "NA"
cass.set_riot_api_key(api_key)  # Use the API key provided by the user

starting_summoner = cass.get_summoner(name=summoner_name, region=region)  # Specify the region directly

match_history = starting_summoner.match_history
match_count = 0
auto_filled_count = 0
auto_filled_list = []
how_many_games = int(input("How many of the stated players games would you like to examine? (Please type a Number): "))
non_rift_games = 0
player_names = []

current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # Generate current timestamp
filename = f"auto_filled_data_{current_time}.txt"  # Include timestamp in the filename

"""
This function goes uses the API key and the current participants name to go 
through their how_many_games most recent games it counts what roles they played 
and returns the role with the most played games.
"""

def get_most_played_role(api_key, summoner_name):
    summoner = cass.get_summoner(name=summoner_name, region="NA")
    match_history = summoner.match_history
    match_count2 = 0
    role_counts = {}
    while match_count2 <= 25:
        match = match_history[match_count2]
        if match.queue.id == 420:  # Is game a ranked summoner's rift game?
            print(summoner)
            participant = match.participants[summoner]
            try:
                role = participant.lane
                if role not in role_counts:
                    role_counts[role.value] = 1
                else:
                    role_counts[role.value] += 1
            except KeyError:
                pass
            match_count2 += 1
        else:
            print(summoner, "'s game", match_count2, "is not a Ranked Summoner's Rift Game")
            match_count2 += 1
    if len(role_counts) == 0:
        raise Exception("No Main Role Could be Determined")
    else:
        most_played_role = max(role_counts, key=role_counts.get)
        formatted_role = f"Lane.{most_played_role.lower()}"
        return formatted_role

"""
actual counting of what players are autofilled based on their currently played 
role and the main role determined by get_most_played_role
"""
while match_count <= how_many_games and match_count <= len(match_history):
    game = match_history[match_count]  # Retrieve each game one by one
    if game.queue.id == 420:  # is for ranked Summoner's Rift?
        for participant in game.participants:
            most_played_role = get_most_played_role(api_key, participant.summoner.name)
            current_played_lane = str(participant.lane)
            if most_played_role != current_played_lane:
                auto_filled_count += 1
                auto_filled_list.append(participant.summoner.name)
                match_count += 1
            else:
                print(participant.summoner.name, " Is Not AutoFilled")
                player_names.append(participant.summoner.name)
                match_count += 1
    else:
        print(" Match ", match_count, "is not a Ranked Summoner's Rift Game")
        non_rift_games += 1
        match_count += 1


"""
Output Statements
"""
with open(filename, "w") as file:
    print("Auto-filled Count:", auto_filled_count)
    print("Auto-filled List:", auto_filled_list)
    #print("There were ", non_rift_games, "non-ranked non-summoners rift games")
    #print(player_names)
    file.write(f"Auto-filled Count: {auto_filled_count}\n")
    file.write(f"Auto-filled List: {auto_filled_list}\n")
    file.write(f"Not Auto-filled List: {player_names}")
    file.write(f"There were {non_rift_games} games not played on Summoner's Rift\n")

