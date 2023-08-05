#!/usr/bin/env python3

from webcubers import WebCubers
import argparse
import sys
import appdirs
import os
import sys
import cutie
import requests
import pyotp
from prettytable import PrettyTable

def banner():
    print(f'''
 __    __     _       ___      _                   
/ / /\ \ \___| |__   / __\   _| |__   ___ _ __ ___ 
\ \/  \/ / _ \ '_ \ / / | | | | '_ \ / _ \ '__/ __|
 \  /\  /  __/ |_) / /__| |_| | |_) |  __/ |  \__ \\
  \/  \/ \___|_.__/\____/\__,_|_.__/ \___|_|  |___/
              < WebCubers-CLI v{WebCubers.module_version} >
''')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def login(username=None, api_key=None):
    if username:
        webcubers = WebCubers(username, api_key)
        if webcubers.is_authenticated:
            with open(session_path, 'w+') as session_file:
                session_file.write(f'{username},{api_key}')
            return True
        else:
            return webcubers.error
    else:
        if not os.path.exists(session_path):
            print('[-] Session not found please login again.')
            sys.exit()
        else:
            with open(session_path, 'r') as session_file:
                username, api_key = str(session_file.read()).split(',')
            webcubers = WebCubers(username, api_key)
            if webcubers.is_authenticated:
                return webcubers
            else:
                print(f'[-] {webcubers.error["message"]}')
                if webcubers.error['code'] == 403:
                    try:
                        os.remove(session_path)
                    except:
                        pass
                sys.exit()

def logout():
    try:
        os.remove(session_path)
        return True
    except:
        return False

def download_snippet(snippet_id):
    webcubers = login()
    snippet = webcubers.snippet(snippet_id)
    try:
        snippet_filename = snippet['data']['filename']
        if snippet['status']:
            with open(snippet_filename, 'wb') as snippet_file:
                snippet_file.write(str(snippet['data']['code']).encode())
            print(f'\n[+] Snippet {bcolors.HEADER}{snippet_filename}{bcolors.ENDC} downloaded successfully.\n')
        else:
            print(f'[-] {snippet["message"]}')
    except :
        print(f'[-] {snippet["message"]}')

def download_repo_file(file_id):
    webcubers = login()
    repo_file_info = webcubers.repository_get(file_id)
    try:
        repo_filename = repo_file_info['data']['filename']
        if repo_file_info['status']:
            with open(repo_filename, 'wb') as local_repo_file:
                local_repo_file.write(str(repo_file_info['data']['code']).encode())
            print(f'\n[+] Repository file {bcolors.HEADER}{repo_filename}{bcolors.ENDC} downloaded successfully.\n')
        else:
            print(f'[-] {repo_file_info["message"]}')
    except :
        print(f'[-] {repo_file_info["message"]}')

def arg_logout(args):
    try_logout = logout()
    if try_logout == True:
        print('[+] You have successfully signed out.')
    else:
        print(f'[-] Problem occurred in removing session, please try login again.')

def arg_profile(args):
    webcubers = login()
    profile = webcubers.profile()
    if profile['status'] == True:
        print(f'{bcolors.BOLD}[+] Profile information :\n{bcolors.ENDC}')
        for profile_key, profile_value in profile['data'].items():
            print(f'\t{bcolors.WARNING}[+] {profile_key.capitalize()} :{bcolors.ENDC} {bcolors.HEADER}{profile_value}{bcolors.ENDC}')
    else:
        print(f'[-] Problem occurred with removing session, please try login again.')

def arg_login(args):
    try_login = login(args.username, args.api_key)
    if try_login == True:
        print('[+] You have successfully signed in webcubers.')
    else:
        print(f'[-] {try_login}')

def arg_snippets(args):
    webcubers = login()
    snippets = webcubers.snippets()

    snippets_ids = []
    snippets_info = []
    for snippet in snippets['data']:

        snippet_type = snippet["type"].capitalize()
        if snippet["type"] == 'private':
            snippet_type = f'{bcolors.FAIL}{snippet_type}{bcolors.ENDC}'
        else:
            snippet_type = f'{bcolors.WARNING}{snippet_type}{bcolors.ENDC}'

        snippets_info.append(f'{bcolors.HEADER}{snippet["filename"]}{bcolors.ENDC} - {snippet["title"]} [ {snippet_type} ]')
        snippets_ids.append(f'{snippet["id"]}')
    
    print(f'{bcolors.BOLD}[~] Select snippet to download :{bcolors.ENDC}\n')
    target_snippet_id = cutie.select(
        snippets_info,
        deselected_prefix='\t',
        selected_prefix='\t => ')
    
    download_snippet(snippets_ids[target_snippet_id])

def arg_repo(args):
    webcubers = login()

    if args.download:
        download_repo_file(args.download[0])    
    elif args.upload:
        filepath = os.path.normpath(args.upload[0])
        filename = filepath.split(os.sep)[-1]
        with open(filepath, 'rb') as local_repo_file:
            code = local_repo_file.read()

        force = False
        if args.force:
            force = True

        response = webcubers.repository_post(filename, code, force=force)
        if response['status']:
            print(f"[+] {response['data']['message']}")
        else:
            print(f"[-] {response['message']}")

    else:
        repository_files = webcubers.repository()

        snippets_info = []
        for repository_file in repository_files['data']:

            snippets_info.append(f'{bcolors.HEADER}{repository_file["filename"]}{bcolors.ENDC}')
        
        print(f'{bcolors.BOLD}[~] Select file to download :{bcolors.ENDC}\n')
        target_repo_file_id = cutie.select(
            snippets_info,
            deselected_prefix='\t',
            selected_prefix='\t => ')
        
        download_repo_file(repository_files['data'][target_repo_file_id]["filename"])    
    
def arg_connection(args):
    try:
        connection_info = requests.get('http://ifconfig.io/all.json').json()
    except:
        print('[-] Connection error, please check your internet connection.')
        sys.exit()
    
    print(f'{bcolors.BOLD}[~] Connection info :{bcolors.ENDC}\n')
    print(f'\t[+] IP : {connection_info["ip"]}')
    
    if connection_info['host']:
        print(f'\t[+] Host : {connection_info["host"][:-1]}')
    
    print(f'\t[+] Country : {connection_info["country_code"]}')

    test_connection = WebCubers.ping().status_code
    if test_connection == 481 or test_connection == 403:
        access_status = f'{bcolors.FAIL}Blocked{bcolors.ENDC}'
    else:
        access_status = f'{bcolors.HEADER}Allowed{bcolors.ENDC}'

    print(f'\t[+] Access : {access_status}')

def arg_leaders(args):
    webcubers = login()

    if args.classname:
        print(f'{bcolors.BOLD}{args.classname[0].upper()} Leaderboard :{bcolors.ENDC}\n')
        leaderboard_request = webcubers.leaderboard(args.classname[0])
        if not leaderboard_request['status']:
            print(f'[-] {leaderboard_request["message"]}')
            sys.exit()

        leaderboard_data = leaderboard_request['data']
    else:
        print(f'{bcolors.BOLD}Webcubers Leaderboard :{bcolors.ENDC}\n')
        leaderboard_data = webcubers.leaderboard()['data']
    
    leaderboard = PrettyTable()
    leaderboard.padding_width = 5

    leaderboard.field_names = ["ID", "Name", "Score"]
    leaderboard.align["Name"] = "l"

    leader_position = 1
    for leader in leaderboard_data:
        leaderboard.add_row([leader_position, leader['username'], leader['score']])
        leader_position += 1
    print(leaderboard)

def arg_otp(args):
    otp_path = os.path.join(app_path, 'otp')

    if args.setkey:
        with open(otp_path, 'w+') as otp_file:
            otp_file.write(f'{args.setkey[0]}')

        print(f'{bcolors.BOLD}[+] OTP-Key saved successfully.{bcolors.ENDC}')
    else:
        if not os.path.exists(otp_path):
            print('[-] OTP-Key not found please set it again.')
            sys.exit()
        else:
            with open(otp_path, 'r') as otp_file:
                otp_key = otp_file.read()
            totp = pyotp.TOTP(otp_key)
            new_key = totp.now()
            print(f'[+] Your new login token is : {bcolors.BOLD}{new_key}{bcolors.ENDC}')

def main():
    global session_path, app_path
    try:
        banner()

        app_path = appdirs.user_data_dir('Cubers','WebCubers')
        session_path = os.path.join(app_path, 'session')

        if not os.path.exists(app_path):
            os.makedirs(app_path)
        
        # parser
        cli_parser = argparse.ArgumentParser(prog='cubers', description='WebCubers CLI Connector.')
        cli_subparsers = cli_parser.add_subparsers()

        login_command = cli_subparsers.add_parser('login')
        login_command.add_argument('username')
        login_command.add_argument('api_key')
        login_command.set_defaults(func=arg_login)

        leaders_command = cli_subparsers.add_parser('leaders')
        leaders_command.add_argument('--classname', nargs=1, metavar=('class_id'))
        leaders_command.set_defaults(func=arg_leaders)

        otp_command = cli_subparsers.add_parser('otp')
        otp_command.add_argument('--setkey', nargs=1, metavar=('key'))
        otp_command.set_defaults(func=arg_otp)

        snippets_command = cli_subparsers.add_parser('snippets')
        snippets_command.set_defaults(func=arg_snippets)

        repo_command = cli_subparsers.add_parser('repo')
        repo_command.add_argument('--upload', nargs=1, metavar=('filepath'))
        repo_command.add_argument('--force', action='store_true')
        repo_command.add_argument('--download', nargs=1, metavar=('filename'))
        repo_command.set_defaults(func=arg_repo)

        connection_command = cli_subparsers.add_parser('connection')
        connection_command.set_defaults(func=arg_connection)

        logout_command = cli_subparsers.add_parser('logout')
        logout_command.set_defaults(func=arg_logout)

        profile_command = cli_subparsers.add_parser('profile')
        profile_command.set_defaults(func=arg_profile)

        if len(sys.argv) <= 1:
            sys.argv.append('--help')

        # Execute parse_args()
        args = cli_parser.parse_args()
        args.func(args)
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    main()