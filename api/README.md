# API

The API accepts image URLs or Base64 encoded images, runs facial recognition on the images, picks the most frequently occurring face, if a racial preference has been set it determines the race of the face, if a minimum rating threshold has been set it rates their attractiveness, lastly returning the match information and decision.

## Endpoints
POST /rating?race=[<ins>race</ins>]&rating=[<ins>rating</ins>]

```json
{
    "images": [
        "https://images-ssl.gotinder.com/u/ei2H13vR1cV46M3Nt56Czd/r4bQcxoqzuan2pwcPwbJ1z.jpeg?Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6IiovdS9laTJIMTN2UjFjVjQ2TTNOdDU2Q3pkLyoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE2NjE1NTg2NDB9fX1df"
    ]
}
```

## Parameters
| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `race` | `array of strings` | Query, Optional | Racial Options: ["asian", "white", "middle eastern", "indian", "latino", "black"] |
| `rating` | `float` | Query, Optional | 0.0 - 5.0 |
| `images` | `array of strings` | Body, Requred | String can be the image URL or Base64 encoded image. Limit of up to 10 images per request. |

## Response
```json
{
    "match": true, 
    "race": "white", 
    "rating": 2.5576894283294678
}
```

## Example Usage
```
flask run
```
