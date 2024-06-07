# Bot

Signs in to Tinder, grabs potential match profile pictures, sends them to flask server, and once the server responds the bot will either swipe left or right.

## Environment Variables
* FB_USERNAME
* FB_PASSWORD

## Command-Line Flags
| Flags | Type | Description |
|  --- | --- | --- |
| `remote` | `bool` | Open Chrome browser directly on device or start remote server to running chromedriver |
| `host` | `string` | Host runnning API |
| `port` | `string` | Port to access API |
| `use_api` | `bool` | Use API or interact with browser |
| `human_login` | `bool` | Automated or human interaction with browser |
| `pref_race` | `array` | Preferred race filter |
| `min_rating` | `float` | Minimum match rating |
| `like_count` | `int` | Amount of likes before exiting browser |

## Example Usage
```
python3 tinder_bot.py --min_rating 2.55
```