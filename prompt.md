# Prompt

I am wanting to extract location information about different events near washington dc.

Collect the location, date, and time of the event. Please include other information included in the sample data. If you are unsure of the answer, do not include it.

Please return the results in a JSON format. Process all events within the request.


----------------------------

# Examples

## Input

```
Washington DC’s top-rated hot dog stand has over SEVEN HUNDRED 5 star reviews, and is the only food cart or truck option on the National Mall to consider

📍 Sami’s Hot Dog Cart
801 C Street SW
Washington, DC
🚊 L’Enfant Plaza

From 11am-3pm, November 1st-3rd

#dcfoodie #thingstododc #washingtondc #dmveats #hotdogs #exploredc #walkwithlocals
```

## Output

```json
{
    "events": [
        {
            "name": "Sami's Hot Dog Cart",
            "location": {
                "street_address": "801 C Street SW",
                "city": "Washington",
                "state": "DC",
                "zip_code": "",
                "latitude": 38.884,
                "longitude": -77.017
            },
            "start_date": "2024/11/01",
            "end_date": "2024/11/03",
            "start_time": "11:00",
            "end_time": "15:00",
            "hashtags": ["dcfoodie", "thingstododc", "washingtondc", "dmveats", "hotdogs", "exploredc", "walkwithlocals"]
        }
    ]
}
