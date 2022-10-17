# Tinder AI Auto Swiper
### Two part system that implements facial recognition, attractiveness ratings and Tinder API and UI interaction to automate Tinder swipe process.

# API

## Endpoints
POST /rating?race=[<ins>race</ins>]&rating=[<ins>rating</ins>]

## Parameters
| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `race` | `array of strings` | Query, Optional | Racial Options: ["asian", "white", "middle eastern", "indian", "latino", "black"] |
| `rating` | `float` | Query, Optional | 0.0 - 5.0 |

## Response
```json
{
    "match": true, 
    "race": "white", 
    "rating": 2.5576894283294678
}
```

# Bot

### Signs in to Tinder, grabs potential match profile pictures, and sends them to flask server

## Required Environment Variables
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
