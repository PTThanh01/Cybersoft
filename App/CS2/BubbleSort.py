import locale
from PIL import Image, ImageTk
import customtkinter as ctk
from customtkinter import CTkScrollableFrame
from customtkinter import CTkComboBox, CTkLabel, CTkButton


# Create window customtkinter
root = ctk.CTk()
root.title("Find Hotel")
root.geometry("700x600")


destinations = ["Sân bay","Bệnh viện Chợ Rãy","Đại học Sài Gòn","BHD Star","Ktx Đại học Sài Gòn","McDonald's",
                "KFC","Thảo cầm viên","Dinh Độc Lập","Công viên Tao Đàn","Nhà thờ","Bảo tàng","An Dương Vương",]
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
scrollable_dest_frame.grid(row=0, column=0, padx=5, pady=5, rowspan=18, columnspan=1, sticky="nsew")
destination_images = {destination: ImageTk.PhotoImage(Image.open(path).resize((80, 80))) for destination, path in
                      image_paths.items()}

for i, destination in enumerate(destinations):
    button = ctk.CTkButton(
        scrollable_dest_frame,
        text="",  # Empty text for now
        compound="top",  # Display image above the text
        image=destination_images.get(destination),
    )
    button.grid(row=i, column=0, padx=5, pady=5, sticky="ew")
    destination_buttons.append(button)

    # Add room and price information to the button text
    info = location_info.get(destination, {})
    original_text = destination  # Store the original text
    extended_text = f"{destination}\nPhòng: {info.get('rooms', 'N/A')}\nGiá: {info.get('price', 'N/A')}"
    button.configure(text=extended_text)
    
    # Store the original text in a separate attribute
    button.original_text = original_text

result_label = ctk.CTkLabel(root, text="", justify="left", anchor="w", padx=10, wraplength=400, font=("Helvetica", 14))
result_label.grid(row=14, column=2, padx=5, pady=5,sticky="w")

##Filters
filter_frame = ctk.CTkFrame(root)
filter_frame.grid(row=0, column=4, padx=5, pady=5, rowspan=14, sticky="nsew")

# Add filter options for price and rooms
price_filter_label = CTkLabel(filter_frame, text="Filter by Price:")
price_filter_label.grid(row=0, column=4, padx=5, pady=5, sticky="w")

price_options = ["Any", "$10 - $50", "$50 - $100", "$100 - $200", ">$200"]
price_combobox = CTkComboBox(filter_frame, values=price_options)
price_combobox.grid(row=0, column=5, padx=5, pady=5)

price_combobox.bind("<KeyRelease>", lambda event: apply_filters(price_combobox.get(), rooms_combobox.get(), search_entry.get()))

rooms_filter_label = CTkLabel(filter_frame, text="Filter by Rooms:")
rooms_filter_label.grid(row=1, column=4, padx=5, pady=5, sticky="w")

rooms_options = ["Any", "1", "2", "3", ">3"]
rooms_combobox = CTkComboBox(filter_frame, values=rooms_options)
rooms_combobox.grid(row=1, column=5, padx=5, pady=5)

rooms_combobox.bind("<KeyRelease>", lambda event: apply_filters(price_combobox.get(), rooms_combobox.get(), search_entry.get()))

# Add search
search_label = CTkLabel(filter_frame, text="Search:")
search_label.grid(row=2, column=4, padx=5, pady=5, sticky="w")

search_entry = ctk.CTkEntry(filter_frame)
search_entry.grid(row=2, column=5, padx=5, pady=5, sticky="w")

# Bind the key release event to the apply_filters function
search_entry.bind("<KeyRelease>", lambda event: apply_filters(price_combobox.get(), rooms_combobox.get(), search_entry.get()))

def apply_sort_filter(sort_option):
    if "Name (A-Z)" in sort_option:
        bubble_sort_destinations_by_name(destination_buttons, "asc")
    elif "Name (Z-A)" in sort_option:
        bubble_sort_destinations_by_name(destination_buttons, "desc")
    elif "Price (Low to High)" in sort_option:
        bubble_sort_destinations_by_price(destination_buttons, "asc")
    elif "Price (High to Low)" in sort_option:
        bubble_sort_destinations_by_price(destination_buttons, "desc")

    update_button_positions()

# Create a Combobox for sorting
sort_filter_label = CTkLabel(filter_frame, text="Sort:")
sort_filter_label.grid(row=4, column=4, padx=5, pady=5, sticky="w")
sort_combobox = CTkComboBox(filter_frame, values=["Sort by Name (A-Z)", "Sort by Name (Z-A)", "Sort by Price (Low to High)", "Sort by Price (High to Low)"])
sort_combobox.grid(row=4, column=5,  padx=5, pady=5, sticky="ew")

# Bind the function to Combobox selection changes
sort_combobox.bind("<<ComboboxSelected>>", lambda event: apply_sort_filter(sort_combobox.get()))



# Bind the key release event to the apply_filters function
apply_filter_button = CTkButton(
    filter_frame,
    text="Apply Filters",
    command=lambda: apply_filters(price_combobox.get(), rooms_combobox.get(), search_entry.get(), sort_combobox.get())
)
apply_filter_button.grid(row=3, column=4, columnspan=2, pady=5)


def apply_filters(price_filter, rooms_filter, keyword_filter, sort_option=None):
    # Logic to filter locations based on price, rooms, keyword, and sort_option
    global filtered_destinations
    filtered_destinations = filter_locations(price_filter, rooms_filter, keyword_filter)

    if sort_option:
        apply_sort_filter(sort_option)

    # Update destination buttons with filtered destinations
    update_destination_buttons(filtered_destinations, price_filter, rooms_filter)


# Function to filter locations based on price and rooms
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

def update_destination_buttons(filtered_destinations, price_filter, rooms_filter):
    for button in destination_buttons:
        # Use the original_text attribute for comparison
        destination = button.original_text

        # Check if the destination is in the filtered list
        if destination in filtered_destinations:
            button.grid()  # Show the button
        else:
            button.grid_remove()  
def bubble_sort_destinations_by_name(dest_buttons, sort_order):
    n = len(dest_buttons)
    locale.setlocale(locale.LC_COLLATE, 'vi_VN.utf8')

    for i in range(n):
        for j in range(0, n-i-1):
            dest_button1 = dest_buttons[j]
            dest_button2 = dest_buttons[j+1]

            dest1_text = dest_button1.cget("text")
            dest2_text = dest_button2.cget("text")

            if (sort_order == "asc" and locale.strcoll(dest1_text, dest2_text) > 0) or \
               (sort_order == "desc" and locale.strcoll(dest1_text, dest2_text) < 0):
                dest_buttons[j], dest_buttons[j+1] = dest_buttons[j+1], dest_buttons[j]

# Cập nhật hàm sắp xếp theo giá tương tự
def bubble_sort_destinations_by_price(dest_buttons, sort_order):
    n = len(dest_buttons)

    for i in range(n):
        for j in range(0, n-i-1):
            dest_button1 = dest_buttons[j]
            dest_button2 = dest_buttons[j+1]

            dest1_text = dest_button1.cget("text")
            dest2_text = dest_button2.cget("text")

            price1_str = extract_price_from_text(dest1_text)
            price2_str = extract_price_from_text(dest2_text)

            # Extract the numeric part of the price (remove "$" sign)
            price1 = int(''.join(char for char in price1_str if char.isdigit()))
            price2 = int(''.join(char for char in price2_str if char.isdigit()))

            if (sort_order == "asc" and price1 > price2) or \
               (sort_order == "desc" and price1 < price2):
                dest_buttons[j], dest_buttons[j+1] = dest_buttons[j+1], dest_buttons[j]

# Hàm trích xuất giá từ văn bản của nút
def extract_price_from_text(text):
    lines = text.split('\n')
    for line in lines:
        if line.startswith("Giá:"):
            return line.split(":")[1].strip()
    return "$0"

# Create a sort function for each sorting option
def sort_by_name_az():
    apply_filters(price_combobox.get(), rooms_combobox.get(), search_entry.get())  # Áp dụng bộ lọc
    bubble_sort_destinations_by_name(destination_buttons, "asc")
    update_button_positions()

def sort_by_name_za():
    apply_filters(price_combobox.get(), rooms_combobox.get(), search_entry.get())  # Áp dụng bộ lọc
    bubble_sort_destinations_by_name(destination_buttons, "desc")
    update_button_positions()

def sort_by_price_low_high():
    apply_filters(price_combobox.get(), rooms_combobox.get(), search_entry.get())  # Áp dụng bộ lọc
    bubble_sort_destinations_by_price(destination_buttons, "asc")
    update_button_positions()

def sort_by_price_high_low():
    apply_filters(price_combobox.get(), rooms_combobox.get(), search_entry.get())  # Áp dụng bộ lọc
    bubble_sort_destinations_by_price(destination_buttons, "desc")
    update_button_positions()

# Helper function to update button positions after sorting
def update_button_positions():
    for i, button in enumerate(destination_buttons):
        button.grid(row=i, column=0, padx=5, pady=5, sticky="ew")

# Start the user interface
root.mainloop()