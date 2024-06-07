import argparse

def get_input_args():
    parser = argparse.ArgumentParser(description='Sign in to Tinder, grabs potential match profile pictures, and sends them to flask server')
    parser.add_argument('--remote', type=bool, default=False, help='Open Chrome browser directly on device or start remote server to running chromedriver')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Host runnning API')
    parser.add_argument('--port', type=str, default='5000', help='Port to access API')
    parser.add_argument('--use_api', type=bool, default=False, help='Use API or interact with browser')
    parser.add_argument('--human_login', type=bool, default=False, help='Automated or human interaction with browser')
    parser.add_argument('--pref_race', type=list, default=[], help='Preferred race filter')
    parser.add_argument('--min_rating', type=float, default=2.5, help='Minimum match rating')
    parser.add_argument('--like_limit', type=int, default=10, help='Amount of likes before exiting browser')

    args = parser.parse_args()

    return args