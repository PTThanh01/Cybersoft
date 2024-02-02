import datetime
import locale
from PIL import Image, ImageTk
import customtkinter as ctk
from customtkinter import CTkScrollableFrame
from customtkinter import CTkComboBox, CTkLabel, CTkButton

# Create window customtkinter
root = ctk.CTk()
root.title("Flight Management")
root.geometry("700x600")

flights = [
   {"id": 1, "destination": "New York", "departure": "2024-01-15 08:00", "airline": "Delta", "price": "$500"},
   {"id": 2, "destination": "Paris", "departure": "2024-02-10 12:30", "airline": "Air France", "price": "$700"},
   {"id": 3, "destination": "Tokyo", "departure": "2024-03-05 18:45", "airline": "Japan Airlines", "price": "$900"},
   {"id": 4, "destination": "London", "departure": "2024-01-20 10:15", "airline": "British Airways", "price": "$650"},
   {"id": 5, "destination": "Sydney", "departure": "2024-02-25 16:00", "airline": "Qantas", "price": "$1200"},
   {"id": 6, "destination": "Los Angeles", "departure": "2024-03-10 21:30", "airline": "United Airlines", "price": "$450"},
   {"id": 7, "destination": "Rome", "departure": "2024-04-01 09:45", "airline": "Alitalia", "price": "$600"},
   {"id": 8, "destination": "Dubai", "departure": "2024-05-15 14:20", "airline": "Emirates", "price": "$850"},
   {"id": 9, "destination": "Singapore", "departure": "2024-06-05 20:15", "airline": "Singapore Airlines", "price": "$1100"},
   {"id": 10, "destination": "Berlin", "departure": "2024-07-10 07:30", "airline": "Lufthansa", "price": "$550"},
   {"id": 11, "destination": "Barcelona", "departure": "2024-02-15 11:00", "airline": "Vueling", "price": "$400"},
   {"id": 12, "destination": "Bangkok", "departure": "2024-03-08 16:30", "airline": "Thai Airways", "price": "$800"},
   {"id": 13, "destination": "Amsterdam", "departure": "2024-04-15 07:45", "airline": "KLM", "price": "$525"},
   {"id": 14, "destination": "Rio de Janeiro", "departure": "2024-05-20 19:15", "airline": "LATAM", "price": "$950"},
   {"id": 15, "destination": "Istanbul", "departure": "2024-06-08 10:30", "airline": "Turkish Airlines", "price": "$675"},
   {"id": 16, "destination": "Phuket", "departure": "2024-07-15 14:45", "airline": "Thai Smile", "price": "$725"},
   {"id": 17, "destination": "Hong Kong", "departure": "2024-08-01 21:00", "airline": "Cathay Pacific", "price": "$975"},
   {"id": 18, "destination": "Cape Town", "departure": "2024-09-15 08:30", "airline": "South African Airways", "price": "$1200"}, 
]

flight_buttons = []

scrollable_frame = CTkScrollableFrame(root, label_text="Flights")
scrollable_frame.configure(height=500)
scrollable_frame.grid(row=0, column=0, padx=5, pady=5, rowspan=18, columnspan=1, sticky="nsew")

for i, flight in enumerate(flights):
    button = ctk.CTkButton(
        scrollable_frame,
        text=f"{flight['destination']} - {flight['airline']}",
        compound="top",
        image=None,  # You can add airline logos here if needed
    )
    button.grid(row=i, column=0, padx=5, pady=5, sticky="ew")
    flight_buttons.append(button)

    # Add flight details to the button text
    extended_text = f"Destination: {flight['destination']}\nDeparture: {flight['departure']}\nAirline: {flight['airline']}\nPrice: {flight['price']}"
    button.configure(text=extended_text)

    # Store the flight details in a separate attribute
    button.flight_details = flight

flight_details_label = ctk.CTkLabel(root, text="", justify="left", anchor="w", padx=10, wraplength=400, font=("Helvetica", 14))
flight_details_label.grid(row=14, column=2, padx=5, pady=5, sticky="w")

# Function to update flight details label
def update_flight_details(selected_button):
    flight_details = selected_button.flight_details
    details_text = f"Flight ID: {flight_details['id']}\nDestination: {flight_details['destination']}\nDeparture: {flight_details['departure']}\nAirline: {flight_details['airline']}\nPrice: {flight_details['price']}"
    flight_details_label.config(text=details_text)

# Bind the button click event to update flight details
for button in flight_buttons:
    button.configure(command=lambda btn=button: update_flight_details(btn))

##Filters
filter_frame = ctk.CTkFrame(root)
filter_frame.grid(row=0, column=4, padx=5, pady=5, rowspan=14, sticky="nsew")

# Add filter options for price and departure
price_filter_label = CTkLabel(filter_frame, text="Filter by Price:")
price_filter_label.grid(row=0, column=4, padx=5, pady=5, sticky="w")

price_options = ["Any", "$500 - $700", "$700 - $900", ">$900"]
price_combobox = CTkComboBox(filter_frame, values=price_options)
price_combobox.grid(row=0, column=5, padx=5, pady=5)

price_combobox.bind("<KeyRelease>", lambda event: apply_filters(price_combobox.get(), departure_combobox.get()))

departure_filter_label = CTkLabel(filter_frame, text="Filter by Departure:")
departure_filter_label.grid(row=1, column=4, padx=5, pady=5, sticky="w")

departure_options = ["Any", "Before 2024-02-01", "2024-02-01 and later", "Exact date"]
departure_combobox = CTkComboBox(filter_frame, values=departure_options)
departure_combobox.grid(row=1, column=5, padx=5, pady=5)

departure_combobox.bind("<KeyRelease>", lambda event: apply_filters(price_combobox.get(), departure_combobox.get(), search_entry.get(), sort_combobox.get()))



# Add search
search_label = CTkLabel(filter_frame, text="Search:")
search_label.grid(row=2, column=4, padx=5, pady=5, sticky="w")

search_entry = ctk.CTkEntry(filter_frame)
search_entry.grid(row=2, column=5, padx=5, pady=5, sticky="w")

# Bind the key release event to the apply_filters function
search_entry.bind("<KeyRelease>", lambda event: apply_filters(price_combobox.get(), departure_combobox.get(), search_entry.get()))

# Sorting function
def apply_sort_filter(sort_option):
    if "Destination (A-Z)" in sort_option:
        bubble_sort_flights_by_destination(flight_buttons, "asc")
    elif "Destination (Z-A)" in sort_option:
        bubble_sort_flights_by_destination(flight_buttons, "desc")
    elif "Departure (Earliest First)" in sort_option:
        bubble_sort_flights_by_departure(flight_buttons, "asc")
    elif "Departure (Latest First)" in sort_option:
        bubble_sort_flights_by_departure(flight_buttons, "desc")
    elif "Price (Low to High)" in sort_option:
        bubble_sort_flights_by_price(flight_buttons, "asc")
    elif "Price (High to Low)" in sort_option:
        bubble_sort_flights_by_price(flight_buttons, "desc")

    update_button_positions()

# Create a Combobox for sorting
sort_filter_label = CTkLabel(filter_frame, text="Sort:")
sort_filter_label.grid(row=4, column=4, padx=5, pady=5, sticky="w")
sort_combobox = CTkComboBox(filter_frame, values=["Sort by Destination (A-Z)", "Sort by Destination (Z-A)", "Sort by Departure (Earliest First)", "Sort by Departure (Latest First)", "Sort by Price (Low to High)", "Sort by Price (High to Low)"])
sort_combobox.grid(row=4, column=5, padx=5, pady=5, sticky="ew")

# Bind the function to Combobox selection changes
sort_combobox.bind("<<ComboboxSelected>>", lambda event: apply_sort_filter(sort_combobox.get()))

# Bind the key release event to the apply_filters function
apply_filter_button = CTkButton(
    filter_frame,
    text="Apply Filters",
    command=lambda: apply_filters(price_combobox.get(), departure_combobox.get(), search_entry.get(), sort_combobox.get())
)
apply_filter_button.grid(row=3, column=4, columnspan=2, pady=5)

global departure_filter
def apply_filters(price_filter, departure_filter, keyword_filter="", sort_option=None):
    # Logic to filter flights based on price, departure, keyword, and sort_option
    global filtered_flights

    # Cập nhật departure_filter với giá trị mới
    departure_filter = departure_filter

    if departure_filter == "Any":
        filtered_flights = filter_flights(price_filter, None, keyword_filter)
    else:
        filtered_flights = filter_flights(price_filter, departure_filter, keyword_filter)

    if sort_option:
        apply_sort_filter(sort_option)

    # Update flight buttons with filtered flights
    update_flight_buttons(filtered_flights, price_filter, departure_filter)

    
# Helper function for bubble sort by destination
def bubble_sort_flights_by_destination(flight_buttons, sort_order):
    n = len(flight_buttons)
    locale.setlocale(locale.LC_COLLATE, 'vi_VN.utf8')

    for i in range(n):
        for j in range(0, n-i-1):
            flight_button1 = flight_buttons[j]
            flight_button2 = flight_buttons[j+1]

            flight1_text = flight_button1.cget("text")
            flight2_text = flight_button2.cget("text")

            if (sort_order == "asc" and locale.strcoll(flight1_text, flight2_text) > 0) or \
               (sort_order == "desc" and locale.strcoll(flight1_text, flight2_text) < 0):
                flight_buttons[j], flight_buttons[j+1] = flight_buttons[j+1], flight_buttons[j]

# Helper function for bubble sort by departure
def bubble_sort_flights_by_departure(flight_buttons, sort_order):
    n = len(flight_buttons)

    for i in range(n):
        for j in range(0, n-i-1):
            flight_button1 = flight_buttons[j]
            flight_button2 = flight_buttons[j+1]

            departure1_str = flight_button1.flight_details["departure"]
            departure2_str = flight_button2.flight_details["departure"]

            departure1 = departure1_str
            departure2 = departure2_str

            if (sort_order == "asc" and departure1 > departure2) or \
               (sort_order == "desc" and departure1 < departure2):
                flight_buttons[j], flight_buttons[j+1] = flight_buttons[j+1], flight_buttons[j]

# Helper function for bubble sort by price
def bubble_sort_flights_by_price(flight_buttons, sort_order):
    n = len(flight_buttons)

    for i in range(n):
        for j in range(0, n-i-1):
            flight_button1 = flight_buttons[j]
            flight_button2 = flight_buttons[j+1]

            price1_str = flight_button1.flight_details["price"]
            price2_str = flight_button2.flight_details["price"]

            price1 = int(''.join(char for char in price1_str if char.isdigit()))
            price2 = int(''.join(char for char in price2_str if char.isdigit()))

            if (sort_order == "asc" and price1 > price2) or \
               (sort_order == "desc" and price1 < price2):
                flight_buttons[j], flight_buttons[j+1] = flight_buttons[j+1], flight_buttons[j]


def filter_flights(price_filter, departure_filter, keyword_filter):
    filtered_flights = []
    for flight in flights:
        price = flight["price"].replace("$", "").strip()
        departure = flight["departure"]
        keyword = f"{flight['destination']} {flight['airline']}"

        # Check if the flight meets the selected filters and keyword
        if (
            (price_filter == "Any" or check_price_filter(price, price_filter)) and
            ((departure_filter is None) or (departure_filter == "Any") or check_departure_filter(departure, departure_filter)) and
            (keyword_filter.lower() in keyword.lower())
        ):
            filtered_flights.append(flight)

    return filtered_flights

# Linear search function
def linear_search(query, text):
    query_length = len(query)
    text_length = len(text)

    for i in range(text_length - query_length + 1):
        match = True
        for j in range(query_length):
            if text[i + j] != query[j]:
                match = False
                break
        if match:
            return True

    return False

# Bind the key release event to the apply_filters function
search_entry.bind("<KeyRelease>", lambda event: apply_filters(price_combobox.get(), departure_combobox.get(), search_entry.get()))

# Check price
def check_price_filter(flight_price, filter_option):
    if filter_option == "Any":
        return True

    # Remove "$" sign and extra spaces if present
    flight_price = flight_price.replace("$", "").strip()

    # Remove any non-numeric characters from the filter option
    filter_option = ''.join(char for char in filter_option if char.isdigit() or char in ['-', '>'])

    if "-" in filter_option:
        min_price, max_price = map(int, filter_option.split("-"))
        return min_price <= int(flight_price) <= max_price
    elif filter_option.startswith(">"):
        min_price = int(filter_option[1:])
        return int(flight_price) > min_price
    else:
        return False


def check_departure_filter(flight_departure, filter_option):
    if filter_option == "Any":
        return True

    if filter_option == "Before 2024-02-01":
        return flight_departure < "2024-02-01"
    elif filter_option == "2024-02-01 and later":
        return flight_departure >= "2024-02-01"
    else:
        return flight_departure.startswith(filter_option)
    
# Helper function to update flight buttons after sorting
def update_flight_buttons(filtered_flights, price_filter, departure_filter):
    for button in flight_buttons:
        # Use the original_text attribute for comparison
        flight = button.flight_details

        # Check if the flight is in the filtered list
        if flight in filtered_flights:
            button.grid()  # Show the button
        else:
            button.grid_remove()
            
# Helper function to update button positions after sorting
def update_button_positions():
    for i, button in enumerate(flight_buttons):
        button.grid(row=i, column=0, padx=5, pady=5, sticky="ew")

# Start the user interface
root.mainloop()
