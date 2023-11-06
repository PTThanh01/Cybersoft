import tkinter as tk
from PIL import Image, ImageTk
import networkx as nx
import matplotlib.image as mpimg
import matplotlib.pyplot as plt


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


# Hàm để cập nhật hình ảnh trên label
def update_image(new_image):
    label.config(image=new_image)
    label.image = new_image


shortest_path = []
def calculate_shortest_path_and_draw(shortest_only=True):
    global shortest_path  # Declare shortest_path as a global variable

    new_start = start_entry.get()
    new_destination = destination_entry.get()

    # Kiểm tra xem điểm đến có tồn tại trong đồ thị không
    if new_destination in G.nodes() and new_start in G.nodes():
        shortest_path = nx.shortest_path(
            G, source=new_start, target=new_destination, weight="weight"
        )
        result_label.config(
            text=f"Đường đi ngắn nhất từ {new_start} đến {new_destination}: {' -> '.join(shortest_path)}"
        )
        result_label.update()

        total_distance = nx.shortest_path_length(
            G, source=new_start, target=new_destination, weight="weight"
            
        )
        rounded_distance = round(total_distance, 2)
        
        distances_text = f"Với khoảng cách: {rounded_distance}"
        result_label.config(text=result_label.cget("text") + "\n" + distances_text)
    else:
        result_label.config(text=f"Không tồn tại điểm đến {new_destination} hoặc điểm bắt đầu {new_start}")
        result_label.update()

    # Tạo một từ điển với tọa độ tùy chỉnh cho các nút
    fixed_positions = {
        "0": (500,122),
        "1": (290,190),
        "2": (144,-103),
        "3": (283,-109),
        "4": (545,0.3),
        "5": (85,202),
        "6": (-131,77),
        "7": (-380,-62),
        "8": (-400,-233),
        "9": (-62,-174),
        "10": (52,-152),
        "11": (150,-134),
        "12": (128,-42),
        "13": (-630,-206),
    }

    # Đọc hình ảnh gốc
    img = mpimg.imread("default1.png")
    img_width = img.shape[1]
    img_height = img.shape[0]

    # Tính toán extent dựa trên kích thước hình ảnh gốc
    extent = [-img_width / 2, img_width / 2, -img_height / 2, img_height / 2]

    # Vẽ đồ thị trên hình ảnh gốc
    plt.imshow(img, extent=extent)
    pos = nx.spring_layout(
        G, pos=fixed_positions, fixed=fixed_positions.keys(), weight="weight"
    )
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_nodes(G, pos, node_color="blue")
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    nx.draw_networkx_labels(G, pos)

    if shortest_only:
        # Vẽ đường đi ngắn nhất
        path_edges = [
            (shortest_path[i], shortest_path[i + 1])
            for i in range(len(shortest_path) - 1)
        ]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=1)

    plt.axis("off")  # Tắt các trục
    plt.show()
        

# Tạo cửa sổ tkinter
root = tk.Tk()
root.title("Chuyển đổi hình ảnh và Giải bài toán")

# Tải hình ảnh ban đầu và các hình ảnh khác

new_image_width = 600
new_image_height = 280
image1 = load_image("default1.png", new_image_width, new_image_height)

# Tạo label để hiển thị hình ảnh ban đầu
label = tk.Label(root, image=image1)
label.pack()

# Tạo label và khung nhập chữ cho điểm bắt đầu mới
start_label = tk.Label(root, text="Từ:")
start_entry = tk.Entry(root)
start_label.pack()
start_entry.pack()

# Tạo label và khung nhập chữ cho điểm đến mới
destination_label = tk.Label(root, text="Đến:")
destination_entry = tk.Entry(root)
destination_label.pack()
destination_entry.pack()

# Tạo nút để tìm đường đi với điểm đến mới
calculate_button = tk.Button(
    root,
    text="Tìm đường đi ngắn nhất",
    command=lambda: calculate_shortest_path_and_draw(),
)
calculate_button.pack()

# Tạo các nút để chuyển đổi hình ảnh và giải bài toán
button1 = tk.Button(
    root,
    text="Hiển thị Đường đi",
    command=lambda: calculate_shortest_path_and_draw(shortest_only=False),
)

result_label = tk.Label(root, text="")
result_label.pack()
button1.pack()

def clear_shortest_path():
    global shortest_path, shortest_path_drawn
    shortest_path = []
    if shortest_path_drawn:
        plt.clf()
        shortest_path_drawn = False
    result_label.config(text="")

# Tạo đối tượng Graph và thêm cạnh
G = nx.DiGraph()
edges = [
    # ("0", "1", 0.83), ("0", "2", 1.6), ("0", "4", 0.5),
    # ("1", "0", 0.83), ("1", "5", 0.75), ("1", "12", 1.05),
    # ("2", "12", 0.25), ("2", "11", 0.12), ("2", "10", 0.38),
    # ("3", "0", 1.2), ("3", "11", 0.54), ("3", "4", 1.07),
    # ("4", "0", 0.5),
    # ("5", "6", 0.94), ("5", "12", 0.88),
    # ("6", "7", 1.06), ("6", "5", 0.94),("6", "9", 0.97),
    # ("7", "13", 1.1), ("7", "8", 0.63), ("7", "6", 1.07),
    # ("8", "9", 1.3), ("8", "7", 0.63), ("8", "13", 0.89),
    # ("9", "6", 0.97), ("9", "10", 0.43), ("9", "8", 1.3),
    # ("10", "9", 0.43), ("10", "11", 0.37), ("10", "12", 0.51),
    # ("11", "3", 0.54), ("11", "2", 0.12),
    # ("12", "10", 0.51), ("12", "5", 0.88), ("12", "2", 0.25), ("12", "1", 1.05),
]

for start, end, weight in edges:
    G.add_edge(start, end, weight=weight)

# Khởi chạy giao diện người dùng
root.mainloop()