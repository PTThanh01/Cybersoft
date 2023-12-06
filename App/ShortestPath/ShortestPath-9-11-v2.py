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
    
    def bfs_shortest_path(self, start, end):
        if start not in self.graph or end not in self.graph:
            return None  

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

    # Tìm đường đi ngắn nhất bằng thuật toán Dijkstra
    if shortest_only:
        shortest_path, total_distance = calculate_shortest_path(graph_obj, start_node, end_node)
        result_label.config(text=f"Đường đi ngắn nhất từ {start_node} đến {end_node}: {' -> '.join(shortest_path)}\nVới khoảng cách {total_distance:.2f}")
        result_label.update()  # Cập nhật giao diện người dùng

    draw_graph(G, node_positions, node_labels, shortest_path if shortest_only else None)


def calculate_shortest_path_and_draw_bfs(shortest_only=True):
    start_node = start_node_entry.get()
    end_node = end_node_entry.get()

    if shortest_only:
        shortest_path, total_distance = calculate_shortest_path(graph_obj, start_node, end_node, method="bfs")
        result_label.config(text=f"Đường đi ngắn nhất từ {start_node} đến {end_node}: {' -> '.join(shortest_path)}\nVới khoảng cách {total_distance}")
        result_label.update()  # Cập nhật giao diện người dùng

    draw_graph(G, node_positions, node_labels, shortest_path if shortest_only else None)


def calculate_shortest_path_and_draw_dfs(shortest_only=True):
    start_node = start_node_entry.get()
    end_node = end_node_entry.get()

    if shortest_only:
        shortest_path, total_distance = calculate_shortest_path(graph_obj, start_node, end_node, method="dfs")
        result_label.config(text=f"Đường đi ngắn nhất từ {start_node} đến {end_node}: {' -> '.join(shortest_path)}\nVới khoảng cách {total_distance}")
        result_label.update()  # Cập nhật giao diện người dùng

    draw_graph(G, node_positions, node_labels, shortest_path if shortest_only else None)


def calculate_shortest_path(graph_obj, start_node, end_node, method="dijkstra"):
    if method == "dijkstra":
        shortest_path = graph_obj.dijkstra(start_node, end_node)
    elif method == "bfs":
        shortest_path = graph_obj.bfs_shortest_path(start_node, end_node)
    elif method == "dfs":
        shortest_path = graph_obj.dfs_shortest_path(start_node, end_node)

    total_distance = 0
    for i in range(len(shortest_path) - 1):
        start_node, end_node = shortest_path[i], shortest_path[i + 1]
        distance = graph_obj.graph[start_node][end_node]
        total_distance += distance

    return shortest_path, total_distance


def draw_graph(G, node_positions, node_labels, shortest_path=None):
    # Load the original image
    img = mpimg.imread("default1.png")
    img_width = img.shape[1]
    img_height = img.shape[0]

    # Calculate the extent based on the original image size
    extent = [-img_width / 2, img_width / 2, -img_height / 2, img_height / 2]

    # Draw the graph on the original image
    plt.imshow(img, extent=extent)
    pos = nx.spring_layout(G, pos=node_positions, fixed=node_positions.keys(), weight='weight')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_nodes(G, pos, node_color='blue')
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    nx.draw_networkx_labels(G, pos)
    pos = nx.spring_layout(G, pos=node_positions, fixed=node_positions.keys(), weight='weight')

    # Adjust the label positions
    label_pos = {node: (pos[node][0], pos[node][1] + 20) for node in node_labels}

    # Add labels to nodes with adjusted positions
    nx.draw_networkx_labels(G, labels=node_labels, pos=label_pos, font_size=10, font_color="black")

    if shortest_path:
        # Draw the shortest path
        path_edges = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=1.1)

    plt.axis('off')
    plt.show()
    
            
# Tạo cửa sổ tkinter
root = tk.Tk()
root.title("Tìm đường đi ngắn nhất")

# new_image_width = 600
# new_image_height = 280
# image1 = load_image("default1.png", new_image_width, new_image_height)

# # Tạo label để hiển thị hình ảnh ban đầu
# label = tk.Label(root, image=image1)
# label.grid(row=0, column=0, columnspan=1)

# Tạo label và khung nhập chữ cho điểm bắt đầu mới
start_label = tk.Label(root, text="Điểm bắt đầu:")
start_node_entry = tk.Entry(root)
end_label = tk.Label(root, text="Điểm đến:")
end_node_entry = tk.Entry(root)
start_node_entry.insert(0, "0")  # Giá trị mặc định cho điểm bắt đầu
end_node_entry.insert(0, "13")  # Giá trị mặc định cho điểm kết thúc
start_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
start_node_entry.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
end_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
end_node_entry.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Tạo nút để tìm đường đi với điểm đến mới
calculate_button = tk.Button(
    root,
    text="Tìm đường đi ngắn nhất (Dijkstra)",
    command=lambda: calculate_shortest_path_and_draw(),
)
calculate_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Tạo nút để tìm đường đi với điểm đến mới
calculate_button = tk.Button(
    root,
    text="Tìm đường đi ngắn nhất (BFS)",
    command=lambda: calculate_shortest_path_and_draw_bfs(),
)
calculate_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Tạo nút để tìm đường đi với điểm đến mới
calculate_button = tk.Button(
    root,
    text="Tìm đường đi ngắn nhất (DFS)",
    command=lambda: calculate_shortest_path_and_draw_dfs(),
)
calculate_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# Tạo các nút để chuyển đổi hình ảnh và giải bài toán
button1 = tk.Button(
    root,
    text="Hiển thị Đường đi",
    command=lambda: calculate_shortest_path_and_draw(shortest_only=False),
)

result_label = tk.Label(root, text="")
result_label.grid(row=8, column=0, columnspan=2, padx=5, pady=5)
button1.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

for i in range(11):  # Thay đổi chỉ số hàng tùy thuộc vào số lượng hàng bạn có
    root.grid_rowconfigure(i, weight=1)

for j in range(2):
    root.grid_columnconfigure(j, weight=1)

def clear_shortest_path():
    global shortest_path, shortest_path_drawn
    shortest_path = []
    if shortest_path_drawn:
        plt.clf()
        shortest_path_drawn = False
    result_label.config(text="")

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
    
    
      
def toggle_edge_weight_visibility():
    if frame.winfo_ismapped():
        frame.grid_remove()
    else:
        frame.grid()   

def update_edge_weights(graph_obj, edges, entries):
    for i, entry in enumerate(entries):
        start, end, _ = edges[i]
        try:
            weight = float(entry.get())
            
            # Check if the entered weight is 0, and remove the edge if true
            if weight == 0 and start in graph_obj.graph and end in graph_obj.graph[start]:
                del graph_obj.graph[start][end]
                # You might also want to handle the case where the end node has no incoming edges
                if not graph_obj.graph[start]:
                    del graph_obj.graph[start]
            elif start in graph_obj.graph and end in graph_obj.graph[start]:
                graph_obj.graph[start][end] = weight
            else:
                # Có thể xử lý tạo cạnh nếu không tồn tại
                graph_obj.add_edge(start, end, weight)
        except ValueError:
            # Xử lý lỗi nhập không phải số
            pass

    # Cập nhật biểu đồ với trọng số mới
    update_networkx_graph(G, graph_obj.graph)  # Thêm dòng này để cập nhật biểu đồ
    draw_graph(G, node_positions, node_labels)

def update_networkx_graph(G, graph_data):
    G.clear()  # Xóa tất cả cạnh trong biểu đồ NetworkX
    for start, end_weights in graph_data.items():
        for end, weight in end_weights.items():
            G.add_edge(start, end, weight=weight)  # Thêm cạnh mới với trọng số


# Tạo Frame để chứa phần nhập trọng số và nút "Xác nhận"
frame = tk.Frame(root)

# Tạo danh sách Entry widgets cho trọng số của các cạnh
edge_weight_entries = []

# Đặt biến để theo dõi hàng và cột
current_row = 0
current_column = 0
entries_per_row = 4  # Số lượng cặp Label và Entry widgets trên mỗi hàng

for i, (start, end, weight) in enumerate(edges):
    label = tk.Label(frame, text=f"({start} -> {end}):")
    entry = tk.Entry(frame)
    entry.insert(0, str(weight))  # Set giá trị mặc định cho Entry
    edge_weight_entries.append(entry)

    label.grid(row=current_row, column=current_column, padx=5, pady=5, sticky="e")
    entry.grid(row=current_row, column=current_column + 1, padx=5, pady=5, sticky="w")

    current_column += 2
    if (i + 1) % entries_per_row == 0:
        current_row += 1
        current_column = 0

# Tạo nút "Xác nhận" để cập nhật trọng số
confirm_button = tk.Button(
    frame,
    text="Xác nhận Trọng số",
    command=lambda: update_edge_weights(graph_obj, edges, edge_weight_entries),
)
confirm_button.grid(row=current_row, column=current_column, columnspan=2, padx=5, pady=5)

# Grid frame vào root window
frame.grid(row=11, column=0, padx=10, pady=10)

# Tạo nút "Ẩn/Hiện" để ẩn và hiện phần nhập trọng số
toggle_button = tk.Button(root, text="Hiện/Ẩn Trọng số", command=toggle_edge_weight_visibility)
toggle_button.grid(row=10, column=0,columnspan=2, padx=5, pady=5)

frame.grid_remove()

# Create a NetworkX graph for visualization
G = nx.DiGraph()
for edge in edges:
    start, end, distance = edge
    G.add_edge(start, end, weight=distance)

# Khởi chạy giao diện người dùng
root.mainloop()