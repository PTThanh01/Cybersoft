import locale
from PIL import Image, ImageTk
import customtkinter as ctk
from customtkinter import CTkScrollableFrame
from customtkinter import CTkComboBox, CTkLabel, CTkButton


# Create window customtkinter
root = ctk.CTk()
root.title("Find Hotel")
root.geometry("500x600")


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

def bubble_sort_destinations_by_name(dest_buttons, sort_order):
    n = len(dest_buttons)
    locale.setlocale(locale.LC_COLLATE, 'vi_VN.utf8')

    for i in range(n):
        for j in range(0, n-i-1):
            dest_button1 = dest_buttons[j]
            dest_button2 = dest_buttons[j+1]
            dest1_text = dest_button1.original_text
            dest2_text = dest_button2.original_text

            if (sort_order == "asc" and locale.strcoll(dest1_text, dest2_text) > 0) or \
               (sort_order == "desc" and locale.strcoll(dest1_text, dest2_text) < 0):
                dest_buttons[j], dest_buttons[j+1] = dest_buttons[j+1], dest_buttons[j]


def bubble_sort_destinations_by_price(dest_buttons, sort_order):
    n = len(dest_buttons)

    for i in range(n):
        for j in range(0, n-i-1):
            dest_button1 = dest_buttons[j]
            dest_button2 = dest_buttons[j+1]
            dest1_text = dest_button1.original_text
            dest2_text = dest_button2.original_text

            price1_str = location_info.get(dest1_text, {}).get("price", "0")
            price2_str = location_info.get(dest2_text, {}).get("price", "0")

            # Remove the dollar sign and convert to integers
            price1 = int(price1_str.replace('$', ''))
            price2 = int(price2_str.replace('$', ''))

            if (sort_order == "asc" and price1 > price2) or \
               (sort_order == "desc" and price1 < price2):
                dest_buttons[j], dest_buttons[j+1] = dest_buttons[j+1], dest_buttons[j]     
             
# Create a sort function for each sorting option
def sort_by_name_az():
    bubble_sort_destinations_by_name(destination_buttons, "asc")
    update_button_positions()

def sort_by_name_za():
    bubble_sort_destinations_by_name(destination_buttons, "desc")
    update_button_positions()

def sort_by_price_low_high():
    bubble_sort_destinations_by_price(destination_buttons, "asc")
    update_button_positions()

def sort_by_price_high_low():
    bubble_sort_destinations_by_price(destination_buttons, "desc")
    update_button_positions()

# Helper function to update button positions after sorting
def update_button_positions():
    for i, button in enumerate(destination_buttons):
        button.grid(row=i, column=0, padx=5, pady=5, sticky="ew")


sort_frame = ctk.CTkFrame(root)
sort_frame.grid(row=0, column=3, padx=5, pady=5, rowspan=6, sticky="nsew")

sort_name_az_button = ctk.CTkButton(sort_frame, text="Sort by Name (A-Z)", command=sort_by_name_az)
sort_name_az_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

sort_name_za_button = ctk.CTkButton(sort_frame, text="Sort by Name (Z-A)", command=sort_by_name_za)
sort_name_za_button.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

sort_price_low_high_button = ctk.CTkButton(sort_frame, text="Sort by Price (Low to High)", command=sort_by_price_low_high)
sort_price_low_high_button.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

sort_price_high_low_button = ctk.CTkButton(sort_frame, text="Sort by Price (High to Low)", command=sort_by_price_high_low)
sort_price_high_low_button.grid(row=3, column=2, padx=5, pady=5, sticky="ew")
    
# Start the user interface
root.mainloop()