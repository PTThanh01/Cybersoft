from collections import deque
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

    def dfs_shortest_path(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path

        shortest_path = None
        for neighbor in self.graph[start]:
            if neighbor not in path:
                new_path = self.dfs_shortest_path(neighbor, end, path)
                if new_path:
                    if not shortest_path or len(new_path) < len(shortest_path):
                        shortest_path = new_path

        return shortest_path

# Hàm để cập nhật hình ảnh trên label
def update_image(new_image):
    label.config(image=new_image)
    label.image = new_image


def calculate_shortest_path_and_draw(shortest_only=True):
    start_node = start_node_entry.get()
    end_node = end_node_entry.get()

    shortest_path = graph_obj.dfs_shortest_path(start_node, end_node)
    if shortest_only:
        result_label.config(text=f"Đường đi ngắn nhất từ {start_node} đến {end_node}: {' -> '.join(shortest_path)}")
        result_label.update()  # Cập nhật giao diện người dùng

        total_distance = 0
        distances_text = "Với khoảng cách "
        for i in range(len(shortest_path) - 1):
            start_node, end_node = shortest_path[i], shortest_path[i + 1]
            distance = graph_obj.graph[start_node][end_node]
            total_distance += distance
        distances_text += f"{total_distance}"
        result_label.config(text=result_label.cget("text") + "\n" + distances_text)

    # Đọc hình ảnh gốc
    img = mpimg.imread("default1.png")
    img_width = img.shape[1]
    img_height = img.shape[0]

    # Tính toán extent dựa trên kích thước hình ảnh gốc
    extent = [-img_width / 2, img_width / 2, -img_height / 2, img_height / 2]

    # Vẽ đồ thị trên hình ảnh gốc
    plt.imshow(img, extent=extent)
    pos = nx.spring_layout(G, pos=node_positions, fixed=node_positions.keys(), weight='weight')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_nodes(G, pos, node_color='blue')
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    nx.draw_networkx_labels(G, pos)
    pos = nx.spring_layout(G, pos=node_positions, fixed=node_positions.keys(), weight='weight')

    # Adjust the label positions
    label_pos = {node: (pos[node][0], pos[node][1] + 20) for node in node_labels}  # Adjust the '20' value as needed

    # Add labels to nodes with adjusted positions
    nx.draw_networkx_labels(G, labels=node_labels, pos=label_pos, font_size=10, font_color="black")

    if shortest_only:
        # Vẽ đường đi ngắn nhất
        path_edges = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=1.5)

    plt.axis('off')  # Tắt các trục
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

start_label = tk.Label(root, text="Từ:")
start_node_entry = tk.Entry(root)
end_label = tk.Label(root, text="Đến:")
end_node_entry = tk.Entry(root)
start_node_entry.insert(0, "0")  # Giá trị mặc định cho điểm bắt đầu
end_node_entry.insert(0, "13")  # Giá trị mặc định cho điểm kết thúc
start_label.pack()
start_node_entry.pack()
end_label.pack()
end_node_entry.pack()

# Tạo các nút để chuyển đổi hình ảnh và giải bài toán
button2 = tk.Button(root, text="Hiển thị Tất cả Đường", command=lambda: calculate_shortest_path_and_draw(shortest_only=False))
button1 = tk.Button(root, text="Đường đi ngắn nhất (DFS)", command=calculate_shortest_path_and_draw)
result_label = tk.Label(root, text="")
result_label.pack()

button2.pack()
button1.pack()

# Tạo đối tượng Graph và thêm cạnh
graph_obj = Graph()
edges = [
    ("0", "1", 0.83), ("0", "2", 1.6), ("0", "4", 0.5),
    ("1", "0", 0.83), ("1", "5", 0.75), ("1", "12", 1.05),
    ("2", "12", 0.25), ("2", "11", 0.12), ("2", "10", 0.38),
    ("3", "0", 1.2), ("3", "11", 0.54), ("3", "4", 1.07),
    ("4", "0", 0.5),
    ("5", "6", 0.94), ("5", "12", 0.88),
    ("6", "7", 1.06), ("6", "5", 0.94),("6", "9", 0.97),
    ("7", "13", 1.1), ("7", "8", 0.63), ("7", "6", 1.07),
    ("8", "9", 1.3), ("8", "7", 0.63), ("8", "13", 0.89),
    ("9", "6", 0.97), ("9", "10", 0.43), ("9", "8", 1.3),
    ("10", "9", 0.43), ("10", "11", 0.37), ("10", "12", 0.51),
    ("11", "3", 0.54), ("11", "2", 0.12),
    ("12", "10", 0.51), ("12", "5", 0.88), ("12", "2", 0.25), ("12", "1", 1.05),
    ("13", "7", 1.1),("13", "8", 0.89)
]

node_labels = {
    "0": "2 Bis",
    "1": "An Dương Vương",
    "2": "Nguyễn Văn Linh",
    "3": "Võ Văn Kiệt",
    "4": "Điện Biên Phủ",
    "5": "Ngô Gia Tự",
    "6": "Trần Phú",
    "7": "Ktx Đại học Sài Gòn",
    "8": "McDonald's",
    "9": "KFC",
    "10": "Thảo cầm viên",
    "11": "Dinh Độc Lập",
    "12": "Công viên Tao Đàn",
    "13": "Đại học Sài Gòn",
}

# Tạo một từ điển với tọa độ tùy chỉnh cho các nút    
node_positions = {
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


for start, end, weight in edges:
    graph_obj.add_edge(start, end, weight)

# Create a NetworkX graph for visualization
G = nx.DiGraph()
for edge in edges:
    start, end, distance = edge
    G.add_edge(start, end, weight=distance)

# Khởi chạy giao diện người dùng
root.mainloop()