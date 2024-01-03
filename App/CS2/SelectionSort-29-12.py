from PIL import Image, ImageTk
import customtkinter as ctk
from customtkinter import CTkScrollableFrame, CTkComboBox, CTkLabel, CTkButton
import locale

# Create window customtkinter
root = ctk.CTk()
root.title("Find Hotel")
root.geometry("650x600")

destinations = ["Sân bay", "Bệnh viện Chợ Rãy", "Đại học Sài Gòn", "BHD Star", "Ktx Đại học Sài Gòn", "McDonald's",
                "KFC", "Thảo cầm viên", "Dinh Độc Lập", "Công viên Tao Đàn", "Nhà thờ", "Bảo tàng", "An Dương Vương", ]
destination_buttons = []

image_paths = {
    "Sân bay": r"Picture\akf.png",
    "Bệnh viện Chợ Rãy": r"Picture\dfkr.png",
    "Đại học Sài Gòn": r"Picture\dhh.png",
    "An Dương Vương": r"Picture\fbf.png",
    "BHD Star": r"Picture\fbh.png",
    "Nhà thờ": r"Picture\fbtur.png",
    "Bảo tàng": r"Picture\gbg.png",
    "Sân bay": r"Picture\OIG.png",
    "Ktx Đại học Sài Gòn": r"Picture\OIG1.png",
    "McDonald's": r"Picture\OIGee.png",
    "Thảo cầm viên": r"Picture\rth.png",
    "Dinh Độc Lập": r"Picture\juu.png",
    "Công viên Tao Đàn": r"Picture\hph.png",
    "KFC": r"Picture\jjj.png",
}

location_info = {
    "An Dương Vương": {"price": "$120", "rooms": 1},
    "BHD Star": {"price": "$210", "rooms": 3},
    "Sân bay": {"price": "$520", "rooms": 2},
    "Bệnh viện Chợ Rãy": {"price": "$300", "rooms": 4},
    "Đại học Sài Gòn": {"price": "$20", "rooms": 2},
    "2 Bis": {"price": "$320", "rooms": 3},
    "Nhà thờ": {"price": "$20", "rooms": 2},
    "Bảo tàng": {"price": "$100", "rooms": 2},
    "Ktx Đại học Sài Gòn": {"price": "$10", "rooms": 6},
    "McDonald's": {"price": "$100", "rooms": 1},
    "Thảo cầm viên": {"price": "$10", "rooms": 1},
    "Dinh Độc Lập": {"price": "$10", "rooms": 1},
    "Công viên Tao Đàn": {"price": "$50", "rooms": 2},
    "KFC": {"price": "$60", "rooms": 3},
}

scrollable_dest_frame = CTkScrollableFrame(root, label_text="Hotel")
scrollable_dest_frame.configure(height=500)
scrollable_dest_frame.grid(row=0, column=0, padx=5, pady=5, rowspan=16, columnspan=1, sticky="nsew")

destination_images = {destination: ImageTk.PhotoImage(Image.open(path).resize((80, 80))) for destination, path in
                      image_paths.items()}

for i, destination in enumerate(destinations):
    button = ctk.CTkButton(
        scrollable_dest_frame,
        text=destination,
        compound="top",  # Display image above the text
        image=destination_images.get(destination),
    )
    button.grid(row=i, column=0, padx=5, pady=5, sticky="ew")
    destination_buttons.append(button)
    # Add room and price information to the button text
    info = location_info.get(destination, {})
    info_text = f"{destination}\nPhòng: {info.get('rooms', 'N/A')}\nGiá: {info.get('price', 'N/A')}"
    button.configure(text=info_text)

result_label = ctk.CTkLabel(root, text="", justify="left", anchor="w", padx=10, wraplength=400, font=("Helvetica", 14))
result_label.grid(row=14, column=2, padx=5, pady=5, sticky="w")

# Filters
filter_frame = ctk.CTkFrame(root)
filter_frame.grid(row=0, column=4, padx=5, pady=5, rowspan=16, sticky="nsew")

# Add filter options for price and rooms
price_filter_label = CTkLabel(filter_frame, text="Filter by Price:")
price_filter_label.grid(row=0, column=4, padx=5, pady=5, sticky="w")

price_options = ["Any", "$10 - $50", "$50 - $100", "$100 - $200", ">$200"]
price_combobox = CTkComboBox(filter_frame, values=price_options)
price_combobox.grid(row=0, column=5, padx=5, pady=5)

price_combobox.bind("<KeyRelease>", lambda event: apply_filters(price_combobox.get(), rooms_combobox.get(),
                                                                search_entry.get()))

rooms_filter_label = CTkLabel(filter_frame, text="Filter by Rooms:")
rooms_filter_label.grid(row=1, column=4, padx=5, pady=5, sticky="w")

rooms_options = ["Any", "1", "2", "3", ">3"]
rooms_combobox = CTkComboBox(filter_frame, values=rooms_options)
rooms_combobox.grid(row=1, column=5, padx=5, pady=5)

rooms_combobox.bind("<KeyRelease>", lambda event: apply_filters(price_combobox.get(), rooms_combobox.get(),
                                                                 search_entry.get()))

# Add search
search_label = CTkLabel(filter_frame, text="Search:")
search_label.grid(row=2, column=4, padx=5, pady=5, sticky="w")

search_entry = ctk.CTkEntry(filter_frame)
search_entry.grid(row=2, column=5, padx=5, pady=5, sticky="w")

sort_name_asc_button = CTkButton(filter_frame, text="Sort by Name (A-Z)", command=lambda: selection_sort_destinations_by_name(False))
sort_name_asc_button.grid(row=4, column=4, padx=5, pady=5)

sort_name_desc_button = CTkButton(filter_frame, text="Sort by Name (Z-A)", command=lambda: selection_sort_destinations_by_name(True))
sort_name_desc_button.grid(row=4, column=5, padx=5, pady=5)

sort_price_asc_button = CTkButton(filter_frame, text="Sort by Price (Low to High)",
                                  command=lambda: selection_sort_destinations_by_price(False))
sort_price_asc_button.grid(row=5, column=4, padx=5, pady=5)

sort_price_desc_button = CTkButton(filter_frame, text="Sort by Price (High to Low)",
                                   command=lambda: selection_sort_destinations_by_price(True))
sort_price_desc_button.grid(row=5, column=5, padx=5, pady=5)

# Bind the key release event to the apply_filters function
search_entry.bind("<KeyRelease>", lambda event: apply_filters(price_combobox.get(), rooms_combobox.get(),
                                                              search_entry.get()))

# Update the apply_filter_button command to remove the lambda function
apply_filter_button = CTkButton(
    filter_frame,
    text="Apply Filters",
    command=lambda: apply_filters(price_combobox.get(), rooms_combobox.get(), search_entry.get())
)
apply_filter_button.grid(row=3, column=4, columnspan=2, pady=5)


def apply_filters(price_filter, rooms_filter, keyword_filter):
    # Logic to filter locations based on price and rooms
    filtered_destinations = filter_locations(price_filter, rooms_filter, keyword_filter)
    # Update destination buttons with filtered destinations
    update_destination_buttons(filtered_destinations, price_filter, rooms_filter)


def filter_locations(price_filter, rooms_filter, keyword_filter):
    filtered_destinations = []
    for destination, info in location_info.items():
        price = info.get("price", "").replace("$", "").strip()
        rooms = str(info.get("rooms", ""))
        keyword = destination.lower()

        # Check if the location meets the selected filters and keyword
        if (
                (price_filter == "Any" or check_price_filter(price, price_filter)) and
                (rooms_filter == "Any" or check_rooms_filter(rooms, rooms_filter)) and
                (keyword_filter.lower() in keyword)
        ):
            filtered_destinations.append(destination)

    return filtered_destinations


# Check price
def check_price_filter(location_price, filter_option):
    if filter_option == "Any":
        return True

    # Remove "$" sign and extra spaces if present
    location_price = location_price.replace("$", "").strip()

    # Remove any non-numeric characters from the filter option
    filter_option = ''.join(char for char in filter_option if char.isdigit() or char in ['-', '>'])

    if "-" in filter_option:
        min_price, max_price = map(int, filter_option.split("-"))
        return min_price <= int(location_price) <= max_price
    elif filter_option.startswith(">"):
        min_price = int(filter_option[1:])
        return int(location_price) > min_price
    else:
        return False


# Check room
def check_rooms_filter(location_rooms, filter_option):
    if filter_option == "Any":
        return True

    if filter_option.startswith(">"):
        min_rooms = int(filter_option[1:])
        return int(location_rooms) > min_rooms
    else:
        return location_rooms == filter_option


def selection_sort_destinations_by_name(reverse_order=False):
    n = len(destination_buttons)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            text_j = destination_buttons[j].cget("text")
            text_min = destination_buttons[min_index].cget("text")

            # Use strcoll for locale-aware string comparison
            comparison = locale.strcoll(text_j, text_min)

            if (not reverse_order and comparison < 0) or (reverse_order and comparison > 0):
                min_index = j

        destination_buttons[i], destination_buttons[min_index] = destination_buttons[min_index], destination_buttons[i]

    update_destination_buttons([], price_combobox.get(), rooms_combobox.get())

locale.setlocale(locale.LC_COLLATE, 'vi_VN.UTF-8')


def selection_sort_destinations_by_price(reverse_order=False):
    n = len(destination_buttons)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            # Extract the prices from the button text
            price_j = int(destination_buttons[j].cget("text").split('\n')[-1].replace("Giá: $", ""))
            price_min = int(destination_buttons[min_index].cget("text").split('\n')[-1].replace("Giá: $", ""))

            if (not reverse_order and price_j < price_min) or (reverse_order and price_j > price_min):
                min_index = j

        destination_buttons[i], destination_buttons[min_index] = destination_buttons[min_index], destination_buttons[i]

    update_destination_buttons([], price_combobox.get(), rooms_combobox.get())


def update_destination_buttons(filtered_destinations, price_filter, rooms_filter):
    for i, button in enumerate(destination_buttons):
        destination = button.cget("text")

        if not filtered_destinations or destination in filtered_destinations:
            button.grid(row=i, column=0, padx=5, pady=5, sticky="ew")  # Show the button
        else:
            button.grid_remove()  # Hide the button

# Start the user interface
root.mainloop()