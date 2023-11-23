from PIL import Image, ImageTk
import networkx as nx
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from customtkinter import CTkScrollableFrame

# Create window customtkinter
root = ctk.CTk()
root.title("Find Hotel")

# Convert the image to an ImageTk object
def load_image(image_path, width, height):
    image = Image.open(image_path)
    resized_image = image.resize((width, height))
    return ImageTk.PhotoImage(resized_image)

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, start, end, weight):
        if start not in self.graph:
            self.graph[start] = {}
        self.graph[start][end] = weight

    def dijkstra(self, start, end):
        distances = {vertex: float("infinity") for vertex in self.graph}
        previous_vertices = {}
        distances[start] = 0

        vertices = self.graph.copy()

        while vertices:
            current_vertex = min(vertices, key=lambda vertex: distances[vertex])
            vertices.pop(current_vertex)

            for neighbor, weight in self.graph[current_vertex].items():
                potential_route = distances[current_vertex] + weight

                if potential_route < distances[neighbor]:
                    distances[neighbor] = potential_route
                    previous_vertices[neighbor] = current_vertex

        path, current_vertex = [], end
        while current_vertex != start:
            path.insert(0, current_vertex)
            current_vertex = previous_vertices[current_vertex]
        path.insert(0, start)
        return path

def calculate_shortest_path_and_draw(destination=None, shortest_only=True):
    start_node = "2 Bis"
    end_node = destination
    if shortest_only:
        shortest_path, total_distance = calculate_shortest_path(
            graph_obj, start_node, end_node
        )
        result_label.configure(text=f"Với khoảng cách {total_distance:.2f} km")
        result_label.update()
    draw_graph(G, node_positions, shortest_path if shortest_only else None)

def calculate_shortest_path(graph_obj, start_node, end_node, method="dijkstra"):
    if method == "dijkstra":
        shortest_path = graph_obj.dijkstra(start_node, end_node)

    total_distance = 0
    for i in range(len(shortest_path) - 1):
        start_node, end_node = shortest_path[i], shortest_path[i + 1]
        distance = graph_obj.graph[start_node][end_node]
        total_distance += distance

    return shortest_path, total_distance

def on_window_resize(event):
    if hasattr(on_window_resize, "_after_id"):
        root.after_cancel(on_window_resize._after_id)
    on_window_resize._after_id = root.after(200, lambda: draw_graph(G, node_positions))
    
# Function to load and resize images
def load_and_resize_image(image_path, width, height):
    image = Image.open(image_path)
    resized_image = image.resize((width, height))
    return ImageTk.PhotoImage(resized_image)
        
def draw_graph(G, node_positions, shortest_path=None, label_pos_offset=20):
    ax.clear()
    img = mpimg.imread("default1.png")
    img_width = img.shape[1]
    img_height = img.shape[0]
    
    # Get the current window size
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    
    # Calculate the scaling factor for the map
    scale_x = window_width / img_width
    scale_y = window_height / img_height
    
    # Update node positions based on the scaling factor
    scaled_node_positions = {node: (x * scale_x, y * scale_y) for node, (x, y) in node_positions.items()}
    
    extent = [-window_width / 2, window_width / 2, -window_height / 2, window_height / 2]

    plt.subplots_adjust(left=0, bottom=0, right=1, top=1)
    ax.imshow(img, extent=extent)

    pos = nx.spring_layout(
        G, pos=scaled_node_positions, fixed=scaled_node_positions.keys(), weight="weight"
    )
    
    if shortest_path:
        # Extract the subgraph containing only the nodes and edges of the shortest path
        path_edges = [
            (shortest_path[i], shortest_path[i + 1])
            for i in range(len(shortest_path) - 1)
        ]
        path_nodes = set(shortest_path)
        subgraph = G.subgraph(path_nodes)
        
        # Draw only nodes and edges that are part of the shortest path
        nx.draw_networkx_nodes(subgraph, pos, node_color="blue", ax=ax)
        
        # Draw directed edges for the shortest path
        nx.draw_networkx_edges(subgraph, pos, edgelist=path_edges, edge_color="red",ax=ax)
        
        # Draw edge labels for the shortest path
        labels = {(edge[0], edge[1]): G[edge[0]][edge[1]]['weight'] for edge in path_edges}
        nx.draw_networkx_edge_labels(subgraph, pos, edge_labels=labels, ax=ax)
    else:
        # Draw all nodes and edges
        nx.draw_networkx_nodes(G, pos, node_color="blue", ax=ax)
        nx.draw_networkx_edges(G, pos, ax=ax)
        
        # Draw all edge labels
        labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)

    label_pos = {
        node: (pos[node][0], pos[node][1] + label_pos_offset) for node in node_positions
    }

    nx.draw_networkx_labels(G, pos=label_pos, font_size=10, font_color="black", ax=ax)

    ax.axis("off")
    canvas.draw()

initial_width = 800
initial_height = 600
plot_frame = ctk.CTkFrame(root)
plot_frame.grid(row=0, column=2, rowspan=13, padx=10, pady=10)
fig, ax = plt.subplots(figsize=(initial_width / 100, initial_height / 100), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=ctk.TOP, fill=ctk.BOTH, expand=1)

destinations = ["Sân bay","Bệnh viện Chợ Rãy","Đại học Sài Gòn","BHD Star","Ktx Đại học Sài Gòn","McDonald's","KFC","Thảo cầm viên","Dinh Độc Lập","Công viên Tao Đàn","Nhà thờ","Bảo tàng","An Dương Vương",]
destination_buttons = []

image_paths = {
    "Sân bay": "z4.png",
    "Bệnh viện Chợ Rãy": "z4.png",
    "Đại học Sài Gòn": "z4.png",
    "2 Bis": "z4.png",
    "An Dương Vương": "z4.png",
    "BHD Star": "z4.png",
    "Nhà thờ": "z4.png",
    "Bảo tàng": "z4.png",
    "Sân bay": "z4.png",
    "Ktx Đại học Sài Gòn": "z4.png",
    "McDonald's": "z4.png",
    "Thảo cầm viên": "z4.png",
    "Dinh Độc Lập": "z4.png",
    "Công viên Tao Đàn": "z4.png",
    "KFC": "z4.png", 
}

scrollable_dest_frame = CTkScrollableFrame(root, label_text="Hotel")
scrollable_dest_frame.grid(row=0, column=0, padx=5, pady=5, rowspan=13, columnspan=2, sticky="nsew")
destination_images = {destination: load_and_resize_image(path, 80, 80) for destination, path in image_paths.items()}

for i, destination in enumerate(destinations):
    button = ctk.CTkButton(
        scrollable_dest_frame,
        text=destination,
        compound="top",  # Display image above the text
        image=destination_images.get(destination),
        command=lambda d=destination: calculate_shortest_path_and_draw(destination=d),
    )
    button.grid(row=i, column=0, padx=5, pady=5, sticky="ew")
    destination_buttons.append(button)

result_label = ctk.CTkLabel(root, text="")
result_label.grid(row=14, column=2, padx=5, pady=5)
 
graph_obj = Graph()
# Create a list of edges
edges = [
    ("2 Bis", "An Dương Vương", 0.83), ("2 Bis", "BHD Star", 1.6), ("2 Bis", "Bảo tàng", 0.5),
    ("An Dương Vương", "2 Bis", 0.83), ("An Dương Vương", "Sân bay", 0.75), ("An Dương Vương", "Công viên Tao Đàn", 1.05),
    ("BHD Star", "Công viên Tao Đàn", 0.25), ("BHD Star", "Dinh Độc Lập", 0.12), ("BHD Star", "Thảo cầm viên", 0.38),
    ("Nhà thờ", "2 Bis", 1.2), ("Nhà thờ", "Dinh Độc Lập", 0.54), ("Nhà thờ", "Bảo tàng", 1.07),
    ("Bảo tàng", "2 Bis", 0.5),
    ("Sân bay", "Bệnh viện Chợ Rãy", 0.94), ("Sân bay", "Công viên Tao Đàn", 0.88),
    ("Bệnh viện Chợ Rãy", "Ktx Đại học Sài Gòn", 1.06), ("Bệnh viện Chợ Rãy", "Sân bay", 0.94),("Bệnh viện Chợ Rãy", "Đại học Sài Gòn", 0.97),
    ("Ktx Đại học Sài Gòn", "KFC", 1.1), ("Ktx Đại học Sài Gòn", "McDonald's", 0.63), ("Ktx Đại học Sài Gòn", "Bệnh viện Chợ Rãy", 1.07),
    ("McDonald's", "Đại học Sài Gòn", 1.3), ("McDonald's", "Ktx Đại học Sài Gòn", 0.63), ("McDonald's", "KFC", 0.89),
    ("Đại học Sài Gòn", "Bệnh viện Chợ Rãy", 0.97), ("Đại học Sài Gòn", "Thảo cầm viên", 0.43), ("Đại học Sài Gòn", "McDonald's", 1.3),
    ("Thảo cầm viên", "Đại học Sài Gòn", 0.43), ("Thảo cầm viên", "Dinh Độc Lập", 0.37), ("Thảo cầm viên", "Công viên Tao Đàn", 0.51),
    ("Dinh Độc Lập", "Nhà thờ", 0.54), ("Dinh Độc Lập", "BHD Star", 0.12),
    ("Công viên Tao Đàn", "Thảo cầm viên", 0.51), ("Công viên Tao Đàn", "Sân bay", 0.88), ("Công viên Tao Đàn", "BHD Star", 0.25), ("Công viên Tao Đàn", "An Dương Vương", 1.05),
    ("KFC", "Ktx Đại học Sài Gòn", 1.1),("KFC", "McDonald's", 0.89)
]

# Create a list of coordinates for nodes
node_positions = {
    "2 Bis": (500, 122),
    "An Dương Vương": (290, 190),
    "BHD Star": (144, -103),
    "Nhà thờ": (283, -109),
    "Bảo tàng": (545, 0.3),
    "Sân bay": (85, 202),
    "Bệnh viện Chợ Rãy": (-131, 77),
    "Ktx Đại học Sài Gòn": (-380, -62),
    "McDonald's": (-400, -233),
    "Đại học Sài Gòn": (-62, -174),
    "Thảo cầm viên": (52, -152),
    "Dinh Độc Lập": (150, -134),
    "Công viên Tao Đàn": (128, -42),
    "KFC": (-630, -206),
}
for start, end, weight in edges:
    graph_obj.add_edge(start, end, weight)

# Create a NetworkX graph for visualization
G = nx.DiGraph()
for edge in edges:
    start, end, distance = edge
    G.add_edge(start, end, weight=distance)

# Start the user interface
root.mainloop()