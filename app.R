library(shiny)
library(leaflet)
library(jsonlite)
library(bslib)

# # Sample data - in a real app, you might want to read this from a file
# json_data <- '[
#   {
#     "events": [
#       {
#         "name": "Harry Potter: A Forbidden Forest Experience",
#         "location": {
#           "street_address": "Morven Park",
#           "city": "Leesburg",
#           "state": "VA",
#           "zip_code": "",
#           "latitude": 39.1151,
#           "longitude": -77.6073
#         },
#         "start_date": "",
#         "end_date": "2023/12/08",
#         "start_time": "17:00",
#         "end_time": "23:00",
#         "hashtags": [
#           "feverus",
#           "feverambassador",
#           "4dmvkids",
#           "dmvkids",
#           "dcmom",
#           "HPForbiddenForestExperience",
#           "HarryPotter",
#           "Leesburg",
#           "HPForbiddenForestExperienceLeesburg"
#         ]
#       }
#     ],
#     "shortcode": "DBr8xw4SmZt"
#   }
# ]'
# # Parse JSON data
# data <- fromJSON(json_data)

data <- jsonlite::read_json("posts.json", simplifyVector = TRUE)

library(tidyr)
library(dplyr)
data <-
  data %>%
  unnest(events) %>%
  unnest(location)
print(colnames(data))
tibble::glimpse(data)

data <-
  data %>%
  filter(!is.na(latitude) & !is.na(longitude)) %>%
  mutate(
    start_date = as.Date(start_date),
    end_date = as.Date(end_date),
    popup = paste0(
      "<b>", name, "</b><br>",
      ifelse(
        !is.na(start_date),
        paste0(
          format(start_date, format = "%a %b %e"),
          " - ",
          format(end_date, format = "%a %b %e"),
          "<br>"
        ),
        ""
      ),
      ifelse(!is.na(caption), paste0(caption, "<br>"), ""),
      street_address, ", ", city, ", ", state, "<br>",
      # ifelse(
      #   !is.na(display_url),
      #   paste0("<img src='", display_url, "' width='200px'><br>"),
      #   ""
      # ),
      "<a href='https://www.instagram.com/p/", shortcode, "' target='_blank'>",
      "View <code>", owner_username, "</code>'s ", tolower(node_type),
      "</a>"
    )
  )




ui <- page_sidebar(
  title = "Events Map",
  sidebar = sidebar(
    title = "About",
    "This map shows various events and their locations. Click on markers to see event details."
  ),

  card(
    full_screen = TRUE,
    leafletOutput("map", height = "800px")
  )
)

server <- function(input, output, session) {

  output$map <- renderLeaflet({
    # Create base map
    leaflet() %>%
      addTiles() %>%
      # Centered on first event
      setView(lng = mean(data$longitude), lat = mean(data$latitude), zoom = 9)
  })

  # Add markers for each event
  observe({
    # Add markers to the map
    leafletProxy("map") %>%
      clearMarkers() %>%
      addMarkers(
        lng = data$longitude,
        lat = data$latitude,
        popup = data$popup
      )
  })
}

shinyApp(ui, server)
