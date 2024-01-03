import customtkinter as ctk

class SortingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sorting App")

        # Create a frame to organize the widgets
        main_frame = ctk.CTkFrame(self)
        main_frame.pack()

        self.entry_label = ctk.CTkLabel(main_frame, text="Enter numbers (comma-separated): ")
        self.entry_label.grid(row=0, column=0, pady=10)

        self.entry = ctk.CTkEntry(main_frame)
        self.entry.grid(row=0, column=1, pady=10)

        self.algorithm_var = ctk.StringVar(value='Bubble Sort')

        self.algorithm_label = ctk.CTkLabel(main_frame, text="Choose sorting algorithm: ")
        self.algorithm_label.grid(row=1, column=0, pady=10)

        algorithms = ['Bubble Sort', 'Selection Sort']
        self.algorithm_combobox = ctk.CTkComboBox(main_frame, values=algorithms)
        self.algorithm_combobox.grid(row=1, column=1, pady=10)
        self.algorithm_combobox.set('Bubble Sort')  # Set the initial value

        self.sort_button = ctk.CTkButton(main_frame, text="Sort", command=self.sort_numbers)
        self.sort_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.result_label = ctk.CTkLabel(main_frame, text="")
        self.result_label.grid(row=3, column=0, columnspan=2, pady=10)

    def sort_numbers(self):
        numbers = list(map(int, self.entry.get().split(',')))
        algorithm = self.algorithm_var.get()

        if algorithm == 'Bubble Sort':
            self.bubble_sort(numbers)
        elif algorithm == 'Selection Sort':
            self.selection_sort(numbers)

        self.result_label.configure(text=f"Sorted numbers: {numbers}")

    def bubble_sort(self, arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]

    def selection_sort(self, arr):
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]

if __name__ == "__main__":
    app = SortingApp()
    app.mainloop()
