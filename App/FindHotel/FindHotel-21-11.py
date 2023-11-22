from collections import deque
import tkinter as tk
from PIL import Image, ImageTk
import networkx as nx
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Tạo cửa sổ tkinter
root = tk.Tk()
root.title("Find Hotel")


# Hàm để chuyển đổi hình ảnh thành đối tượng ImageTk
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
    # Tìm đường đi ngắn nhất bằng thuật toán Dijkstra
    if shortest_only:
        shortest_path, total_distance = calculate_shortest_path(
            graph_obj, start_node, end_node
        )
        result_label.config(text=f"Với khoảng cách {total_distance:.2f} km")
        result_label.update()  # Cập nhật giao diện người dùng
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


def draw_graph(G, node_positions, shortest_path=None, label_pos_offset=20):
    ax.clear()
    # Load the original image
    img = mpimg.imread("default1.png")
    img_width = img.shape[1]
    img_height = img.shape[0]

    # Calculate the extent based on the original image size
    extent = [-img_width / 2, img_width / 2, -img_height / 2, img_height / 2]

    plt.subplots_adjust(left=0, bottom=0, right=1, top=1)
    # Draw the background image
    ax.imshow(img, extent=extent)

    # Draw the graph on the Matplotlib figure
    pos = nx.spring_layout(
        G, pos=node_positions, fixed=node_positions.keys(), weight="weight"
    )
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_nodes(G, pos, node_color="blue", ax=ax)
    nx.draw_networkx_edges(G, pos, ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)

    # Adjust the label positions
    label_pos = {
        node: (pos[node][0], pos[node][1] + label_pos_offset) for node in node_positions
    }

    # Add labels to nodes with adjusted positions
    nx.draw_networkx_labels(G, pos=label_pos, font_size=10, font_color="black", ax=ax)

    if shortest_path:
        # Draw the shortest path
        path_edges = [
            (shortest_path[i], shortest_path[i + 1])
            for i in range(len(shortest_path) - 1)
        ]
        nx.draw_networkx_edges(
            G, pos, edgelist=path_edges, edge_color="red", width=1.1, ax=ax
        )

    ax.axis("off")

    # Update the Matplotlib plot on the Tkinter canvas
    canvas.draw()


plot_frame = tk.Frame(root)
plot_frame.grid(row=0, column=2, rowspan=13, padx=10, pady=10)
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

destinations = ["Sân bay","Bệnh viện Chợ Rãy","Đại học Sài Gòn","BHD Star","Ktx Đại học Sài Gòn","McDonald's","KFC","Thảo cầm viên","Dinh Độc Lập","Công viên Tao Đàn","Nhà thờ","Bảo tàng","An Dương Vương",]
destination_buttons = []


def create_destination_button(destination):
    button = tk.Button(
        root,
        text=destination,
        command=lambda d=destination: calculate_shortest_path_and_draw(destination=d),
    )
    return button


for i, destination in enumerate(destinations):
    button = create_destination_button(destination)
    button.grid(row=2 + i, column=0, columnspan=2, padx=5, pady=5)
    destination_buttons.append(button)


result_label = tk.Label(root, text="")
result_label.grid(row=14, column=2, padx=5, pady=5)


graph_obj = Graph()
edges = [
    ("2 Bis", "An Dương Vương", 0.83), ("2 Bis", "BHD Star", 1.6), ("2 Bis", "Bảo tàng", 0.5),
    ("An Dương Vương", "2 Bis", 0.83), ("An Dương Vương", "Sân bay", 0.75), ("An Dương Vương", "Công viên Tao Đàn", 1.05),
    ("BHD Star", "Công viên Tao Đàn", 0.25), ("BHD Star", "Dinh Độc Lập", 0.12), ("BHD Star", "Thảo cầm viên", 0.38),
    ("Nhà thờ", "2 Bis", 1.2), ("Nhà thờ", "Dinh Độc Lập", 0.54), ("Nhà thờ", "Bảo tàng", 1.07),
    ("Bảo tàng", "2 Bis", 0.5),
    ("Sân bay", "Bệnh viện Chợ Rãy", 0.94), ("Sân bay", "Công viên Tao Đàn", 0.88),
    ("Bệnh viện Chợ Rãy", "Ktx Đại học Sài Gòn", 1.06), ("Bệnh viện Chợ Rãy", "Sân bay", 0.94),("Bệnh viện Chợ Rãy", "KFC", 0.97),
    ("Ktx Đại học Sài Gòn", "Đại học Sài Gòn", 1.1), ("Ktx Đại học Sài Gòn", "McDonald's", 0.63), ("Ktx Đại học Sài Gòn", "Bệnh viện Chợ Rãy", 1.07),
    ("McDonald's", "KFC", 1.3), ("McDonald's", "Ktx Đại học Sài Gòn", 0.63), ("McDonald's", "Đại học Sài Gòn", 0.89),
    ("KFC", "Bệnh viện Chợ Rãy", 0.97), ("KFC", "Thảo cầm viên", 0.43), ("KFC", "McDonald's", 1.3),
    ("Thảo cầm viên", "KFC", 0.43), ("Thảo cầm viên", "Dinh Độc Lập", 0.37), ("Thảo cầm viên", "Công viên Tao Đàn", 0.51),
    ("Dinh Độc Lập", "Nhà thờ", 0.54), ("Dinh Độc Lập", "BHD Star", 0.12),
    ("Công viên Tao Đàn", "Thảo cầm viên", 0.51), ("Công viên Tao Đàn", "Sân bay", 0.88), ("Công viên Tao Đàn", "BHD Star", 0.25), ("Công viên Tao Đàn", "An Dương Vương", 1.05),
    ("Đại học Sài Gòn", "Ktx Đại học Sài Gòn", 1.1),("Đại học Sài Gòn", "McDonald's", 0.89)
]

# Tạo một từ điển với tọa độ tùy chỉnh cho các nút
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
    "KFC": (-62, -174),
    "Thảo cầm viên": (52, -152),
    "Dinh Độc Lập": (150, -134),
    "Công viên Tao Đàn": (128, -42),
    "Đại học Sài Gòn": (-630, -206),
}
for start, end, weight in edges:
    graph_obj.add_edge(start, end, weight)

# Create a NetworkX graph for visualization
G = nx.DiGraph()
for edge in edges:
    start, end, distance = edge
    G.add_edge(start, end, weight=distance)

# Khởi chạy giao diện người dùng
root.mainloop()
