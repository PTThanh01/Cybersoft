from collections import deque
import tkinter as tk
from PIL import Image, ImageTk
import networkx as nx
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

# Hàm để chuyển đổi hình ảnh thành đối tượng ImageTk
def load_image(image_path):
    image = Image.open(image_path)
    return ImageTk.PhotoImage(image)

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, start, end, weight):
        if start not in self.graph:
            self.graph[start] = {}
        self.graph[start][end] = weight

        # Add edges in both directions for an undirected graph
        if end not in self.graph:
            self.graph[end] = {}
        self.graph[end][start] = weight

    def bfs_shortest_path(self, start, end):
        if start not in self.graph or end not in self.graph:
            return None  # Handle the case where start or end nodes are not in the graph.

        # Create a queue for BFS and initialize it with the start node.
        queue = deque()
        queue.append((start, [start]))  # Each element in the queue is a tuple (current_node, path_so_far).

        # Mark the start node as visited.
        visited = set()
        visited.add(start)

        while queue:
            current_node, path = queue.popleft()

            # Check if we've reached the end node.
            if current_node == end:
                return path  # Return the path from start to end.

            # Explore neighbors of the current node.
            for neighbor in self.graph[current_node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]  # Extend the path with the neighbor.
                    queue.append((neighbor, new_path))

        # If no path is found, return None or a message indicating that there's no path.
        return None

# Hàm để cập nhật hình ảnh trên label
def update_image(new_image):
    label.config(image=new_image)
    label.image = new_image

def calculate_shortest_path_and_draw(shortest_only=True):
    shortest_path = graph_obj.bfs_shortest_path('A', 'C')
    if shortest_only:
        result_label.config(text=f"Đường đi ngắn nhất: {' -> '.join(shortest_path)}")
        result_label.update()  # Cập nhật giao diện người dùng
        
        total_distance = 0
        distances_text = "Với khoảng cách "
        for i in range(len(shortest_path) - 1):
            start_node, end_node = shortest_path[i], shortest_path[i + 1]
            distance = graph_obj.graph[start_node][end_node]
            total_distance += distance
        distances_text += f" {total_distance}"
        result_label.config(text=result_label.cget("text") + "\n" + distances_text)
        
    # Tạo một từ điển với tọa độ tùy chỉnh cho các nút
    fixed_positions = {'A': (52, 155), 'B': (-65, 152), 'C': (-64, 23), 'D': (55, 25), 'E': (61, -137), 'F': (-60, -170), 'G': (63, -175)}

    # Đọc hình ảnh gốc
    img = mpimg.imread("image1.png")
    img_width = img.shape[1]
    img_height = img.shape[0]

    # Tính toán extent dựa trên kích thước hình ảnh gốc
    extent = [-img_width / 2, img_width / 2, -img_height / 2, img_height / 2]

    # Vẽ đồ thị trên hình ảnh gốc
    plt.imshow(img, extent=extent)
    pos = nx.spring_layout(G, pos=fixed_positions, fixed=fixed_positions.keys(), weight='weight')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_nodes(G, pos, node_color='blue')
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    nx.draw_networkx_labels(G, pos)

    if shortest_only:
        # Vẽ đường đi ngắn nhất
        path_edges = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

    plt.axis('off')  # Tắt các trục
    plt.show()

# Tạo cửa sổ tkinter
root = tk.Tk()
root.title("Chuyển đổi hình ảnh và Giải bài toán")

# Tải hình ảnh ban đầu và các hình ảnh khác
image1 = load_image("image1.png")

# Tạo label để hiển thị hình ảnh ban đầu
label = tk.Label(root, image=image1)
label.pack()

# Tạo các nút để chuyển đổi hình ảnh và giải bài toán
button2 = tk.Button(root, text="Hiển thị Tất cả Đường", command=lambda: calculate_shortest_path_and_draw(shortest_only=False))
button1 = tk.Button(root, text="Đường đi ngắn nhất", command=calculate_shortest_path_and_draw)
result_label = tk.Label(root, text="")
result_label.pack()

button2.pack(side="left")
button1.pack(side="left")

# Tạo đối tượng Graph và thêm cạnh
graph_obj = Graph()
edges = [('A', 'B', 1.6), ('A', 'D', 1.8), ('B', 'C', 1.75),
         ('C', 'D', 1.6), ('C', 'F', 2.6), ('D', 'E', 2.15), ('E', 'F', 1.75), ('F', 'G', 1.5)]

for start, end, weight in edges:
    graph_obj.add_edge(start, end, weight)

# Create a NetworkX graph for visualization
G = nx.Graph()
for edge in edges:
    start, end, distance = edge
    G.add_edge(start, end, weight=distance)

# Khởi chạy giao diện người dùng
root.mainloop()
