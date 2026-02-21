import requests
import random
from time import sleep
from colorama import Fore, init

from util.plugins.commun import setTitle, getheaders, proxy, clear

# Initialize colorama for Windows compatibility
init()

# Define color variables
y = Fore.YELLOW
w = Fore.WHITE
b = Fore.BLUE

def groupspamtitle():
    """Display group spam title"""
    clear()
    print(f"""\n{y}[{w}+{y}]{w} GroupChat Spammer\n""")

def selector(token, users):
    """Create groupchats with selected users"""
    clear()
    setTitle("Creating groupchats")
    print(f"{y}[{w}+{y}]{w} Starting groupchat creation with selected users...")
    
    while True:
        try:
            response = requests.post(
                'https://discord.com/api/v9/users/@me/channels', 
                proxies=proxy(), 
                headers=getheaders(token), 
                json={"recipients": users}
            )

            if response.status_code == 200:
                print(f"{y}[{Fore.LIGHTGREEN_EX}!{y}]{w} Created groupchat with {len(users)} users")
            elif response.status_code == 204:
                print(f"{y}[{Fore.LIGHTGREEN_EX}!{y}]{w} Created groupchat")
            elif response.status_code == 429:
                retry_after = response.json().get('retry_after', 'unknown')
                print(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} Rate limited ({retry_after}ms)")
                sleep(retry_after / 1000)  # Convert ms to seconds
            else:
                print(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} Error: {response.status_code}")
                # Add a small delay to avoid rapid failed requests
                sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n{y}[{Fore.LIGHTYELLOW_EX}!{y}]{w} Stopped by user")
            break
        except Exception as e:
            print(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} Exception: {e}")
            sleep(1)

def randomizer(token, ID):
    """Create groupchats with random users"""
    setTitle("Creating random groupchats")
    print(f"{y}[{w}+{y}]{w} Starting random groupchat creation...")
    
    if len(ID) < 2:
        print(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} Need at least 2 friends to create groupchats")
        return

    while True:
        try:
            # Ensure we have at least 2 users for groupchat
            if len(ID) >= 2:
                users = random.sample(ID, 2)
            else:
                print(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} Not enough users available")
                break

            response = requests.post(
                'https://discord.com/api/v9/users/@me/channels', 
                proxies=proxy(), 
                headers=getheaders(token), 
                json={"recipients": users}
            )

            if response.status_code == 200:
                print(f"{y}[{Fore.LIGHTGREEN_EX}!{y}]{w} Created random groupchat")
            elif response.status_code == 204:
                print(f"{y}[{Fore.LIGHTGREEN_EX}!{y}]{w} Created groupchat")
            elif response.status_code == 429:
                retry_after = response.json().get('retry_after', 'unknown')
                print(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} Rate limited ({retry_after}ms)")
                sleep(retry_after / 1000)  # Convert ms to seconds
            else:
                print(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} Error: {response.status_code}")
                sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n{y}[{Fore.LIGHTYELLOW_EX}!{y}]{w} Stopped by user")
            break
        except Exception as e:
            print(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} Exception: {e}")
            sleep(1)

def main_program():
    """Main program execution"""
    groupspamtitle()
    
    print(f"{y}[{w}+{y}]{w} Enter the token of the account you want to Spam")
    token = input(f"{y}[{b}#{y}]{w} Token: ").strip()
    
    if not token:
        print(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} Token cannot be empty")
        return

    # Validate token
    try:
        validity_test = requests.get(
            'https://discord.com/api/v9/users/@me', 
            headers=getheaders(token),
            proxies=proxy()
        )
        if validity_test.status_code != 200:
            print(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} Invalid token")
            return
    except Exception as e:
        print(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} Error validating token: {e}")
        return

    print(f'\n{y}[{w}+{y}]{w} Do you want to choose user(s) yourself to groupchat spam or do you want to select randoms?')
    print(f'''
{y}[{w}01{y}]{w} choose user(s) yourself
{y}[{w}02{y}]{w} randomize the users
                    ''')
    
    try:
        secondchoice = int(input(f'{y}[{b}#{y}]{w} Choice: '))
    except ValueError:
        print(f'{y}[{Fore.LIGHTRED_EX}!{y}]{w} Invalid input. Please enter 1 or 2.')
        return

    if secondchoice not in [1, 2]:
        print(f'{y}[{Fore.LIGHTRED_EX}!{y}]{w} Invalid Choice')
        return

    # If they choose to import the users manually
    if secondchoice == 1:
        print(f'\n{y}[{w}+{y}]{w} Input the users you want to create a groupchat with (separate by , id,id2,id3)')
        recipients = input(f'{y}[{b}#{y}]{w} Users ID: ').strip()
        
        if "," not in recipients:
            print(f"\n{y}[{Fore.LIGHTRED_EX}!{y}]{w} You didn't use commas (,) - format should be: id,id2,id3")
            return
            
        users = [user_id.strip() for user_id in recipients.split(',') if user_id.strip()]
        
        if len(users) < 2:
            print(f"\n{y}[{Fore.LIGHTRED_EX}!{y}]{w} You need at least 2 users to create a groupchat")
            return
            
        print(f"\n{y}[{w}+{y}]{w} Will create groupchats with {len(users)} users")
        input(f"\n\n{y}[{b}#{y}]{w} Press enter to continue (\"ctrl + c\" at anytime to stop)")
        selector(token, users)

    # If they choose to randomize the selection
    elif secondchoice == 2:
        try:
            # Get all users to spam groupchats with
            friend_response = requests.get(
                "https://discord.com/api/v9/users/@me/relationships", 
                proxies=proxy(), 
                headers=getheaders(token)
            )
            
            if friend_response.status_code != 200:
                print(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} Failed to fetch friends list: {friend_response.status_code}")
                return
                
            friendIds = friend_response.json()
            IDs = []
            
            for friend in friendIds:
                IDs.append(friend['id'])
            
            if len(IDs) < 2:
                print(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} You need at least 2 friends to create random groupchats")
                return
                
            print(f"{y}[{w}+{y}]{w} Found {len(IDs)} friends")
            input(f"\n{y}[{b}#{y}]{w} Press enter to continue (\"ctrl + c\" at anytime to stop)")
            randomizer(token, IDs)
            
        except Exception as e:
            print(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} Error fetching friends: {e}")

if __name__ == "__main__":
    try:
        main_program()
    except KeyboardInterrupt:
        print(f"\n\n{y}[{Fore.LIGHTYELLOW_EX}!{y}]{w} Program interrupted by user")
    except Exception as e:
        print(f"\n{y}[{Fore.LIGHTRED_EX}!{y}]{w} Unexpected error: {e}")
    
    input(f"\n{y}[{b}#{y}]{w} Press enter to exit")