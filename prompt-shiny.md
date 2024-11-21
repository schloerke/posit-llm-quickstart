I'd like to make an leaflet application that displays many activities across a map.

I have access to structured post data with an example of

```json
[
  {
    "events": [
      {
        "name": "Harry Potter: A Forbidden Forest Experience",
        "location": {
          "street_address": "Morven Park",
          "city": "Leesburg",
          "state": "VA",
          "zip_code": "",
          "latitude": 39.1151,
          "longitude": -77.6073
        },
        "start_date": "",
        "end_date": "2023/12/08",
        "start_time": "17:00",
        "end_time": "23:00",
        "hashtags": [
          "feverus",
          "feverambassador",
          "4dmvkids",
          "dmvkids",
          "dcmom",
          "HPForbiddenForestExperience",
          "HarryPotter",
          "Leesburg",
          "HPForbiddenForestExperienceLeesburg"
        ]
      }
    ],
    "node_type": "Post",
    "shortcode": "DBr8xw4SmZt",
    "id": "3489149638857614957",
    "__typename": "GraphVideo",
    "is_video": true,
    "date": null,
    "caption": null,
    "title": "",
    "viewer_has_liked": false,
    "edge_media_preview_like": {
      "count": -1,
      "edges": [
        {
          "node": {
            "id": "41127694367",
            "is_verified": false,
            "profile_pic_url": "https://scontent-iad3-1.cdninstagram.com/v/t51.2885-19/433991939_933635164741316_3555757849013978829_n.jpg?stp=dst-jpg_s150x150&_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=108&_nc_ohc=OMIAMrRrm4EQ7kNvgH95dCw&_nc_gid=756aac8a8536432eb6b52c149eb240a0&edm=ANTKIIoBAAAA&ccb=7-5&oh=00_AYDLsDTynG4rgJFp4cBmpDrREjwFhqDuzTkS73z22SaxFQ&oe=6742E6FB&_nc_sid=d885a2",
            "username": "locdnlashdout"
          }
        }
      ]
    },
    "accessibility_caption": null,
    "comments": null,
    "display_url": "https://scontent-iad3-1.cdninstagram.com/v/t51.29350-15/464928701_1127630062119961_4177079216477651977_n.jpg?stp=dst-jpg_e15_fr_p1080x1080&_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=101&_nc_ohc=DYD5SIQnvJ4Q7kNvgFMfgbt&_nc_gid=756aac8a8536432eb6b52c149eb240a0&edm=ANTKIIoBAAAA&ccb=7-5&oh=00_AYA0qSGazdZJToEnko7jIGFuvYsQGxVe_2xjkqT51g6L-w&oe=6742ED29&_nc_sid=d885a2",
    "owner_id": "47943581355",
    "owner_username": "4dmvkids",
    "owner_is_private": false,
    "owner_full_name": "Sarah | DC MD VA Kids Activities"
  }
]
```

Please make markers for each even on the map. When the user clicks on the marker, display the name of the event and the location. It should also contain a link to the original post of the event in the same of `https://www.instagram.com/p/{shortcode}`
