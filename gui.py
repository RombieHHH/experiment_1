import tkinter as tk
from tkinter import ttk, messagebox
from back import Graph


class CircuitAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("电路分析器")
        self.graph = Graph()

        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 创建所有界面组件
        self.create_input_section()
        self.create_operation_section()
        self.create_display_section()

        # 显示初始化对话框
        self.show_init_dialog()

    def show_init_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("初始化电路")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.geometry("600x400")

        # 创建主框架
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 输入框区域
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)

        ttk.Label(input_frame, text="节点数:").pack(side=tk.LEFT, padx=5)
        nodes = ttk.Entry(input_frame, width=10)
        nodes.pack(side=tk.LEFT, padx=5)

        ttk.Label(input_frame, text="边数:").pack(side=tk.LEFT, padx=5)
        edges = ttk.Entry(input_frame, width=10)
        edges.pack(side=tk.LEFT, padx=5)

        # 创建带滚动条的画布
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        # 配置画布
        canvas.configure(yscrollcommand=scrollbar.set)

        # 绑定鼠标滚轮事件
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)

        # 创建窗口以在画布中显示滚动框架
        canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor=tk.NW)

        # 调整画布大小
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def configure_canvas_width(event):
            canvas.itemconfig(canvas_frame, width=event.width)

        scrollable_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_canvas_width)

        # 放置画布和滚动条
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        edge_entries = []

        def update_edge_inputs(*args):
            try:
                # 清除现有的输入框
                for widget in scrollable_frame.winfo_children():
                    widget.destroy()
                edge_entries.clear()

                num_edges = int(edges.get()) if edges.get() else 0
                if num_edges > 0:
                    # 创建边输入区域
                    edges_frame = ttk.LabelFrame(scrollable_frame, text="边列表")
                    edges_frame.pack(fill=tk.X, padx=5, pady=5)

                    # 创建新的边输入框
                    for i in range(num_edges):
                        row_frame = ttk.Frame(edges_frame)
                        row_frame.pack(fill=tk.X, pady=2)

                        ttk.Label(row_frame, text=f"边 {i + 1}:").pack(side=tk.LEFT, padx=2)
                        start = ttk.Entry(row_frame, width=10)
                        start.pack(side=tk.LEFT, padx=2)
                        ttk.Label(row_frame, text="到").pack(side=tk.LEFT, padx=2)
                        end = ttk.Entry(row_frame, width=10)
                        end.pack(side=tk.LEFT, padx=2)
                        ttk.Label(row_frame, text="电阻:").pack(side=tk.LEFT, padx=2)
                        resistance = ttk.Entry(row_frame, width=10)
                        resistance.pack(side=tk.LEFT, padx=2)

                        edge_entries.append((start, end, resistance))

            except ValueError:
                pass

        # 绑定输入事件
        edges.bind('<KeyRelease>', update_edge_inputs)

        # 确认按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        def confirm():
            try:
                edge_info = []
                for start, end, resistance in edge_entries:
                    if all([start.get(), end.get(), resistance.get()]):
                        edge_info.append((start.get(), end.get(), float(resistance.get())))

                for start, end, resistance in edge_info:
                    self.graph.add_edge(start, end, resistance)

                self.update_display()
                dialog.destroy()

            except ValueError:
                messagebox.showerror("错误", "请确保所有输入都是有效的，电阻值必须是数字")

        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="确认", command=confirm).pack(side=tk.RIGHT, padx=5)

        # 等待对话框关闭
        self.root.wait_window(dialog)

    def create_input_section(self):
        input_frame = ttk.LabelFrame(self.main_frame, text="添加边", padding="5")
        input_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        ttk.Label(input_frame, text="起点:").grid(row=0, column=0)
        self.start_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.start_var, width=10).grid(row=0, column=1)

        ttk.Label(input_frame, text="终点:").grid(row=0, column=2)
        self.end_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.end_var, width=10).grid(row=0, column=3)

        ttk.Label(input_frame, text="电阻值:").grid(row=0, column=4)
        self.resistance_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.resistance_var, width=10).grid(row=0, column=5)

        ttk.Button(input_frame, text="添加", command=self.add_edge).grid(row=0, column=6, padx=5)

    def create_operation_section(self):
        op_frame = ttk.LabelFrame(self.main_frame, text="操作", padding="5")
        op_frame.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        ttk.Button(op_frame, text="检测环路", command=self.detect_cycles).grid(row=0, column=0, padx=5)
        ttk.Button(op_frame, text="计算最短路径", command=self.show_shortest_path_dialog).grid(row=0, column=1, padx=5)
        ttk.Button(op_frame, text="显示所有路径", command=self.show_all_paths_dialog).grid(row=0, column=2, padx=5)

    def create_display_section(self):
        display_frame = ttk.LabelFrame(self.main_frame, text="显示区域", padding="5")
        display_frame.grid(row=2, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        # 创建文本显示区域和滚动条
        text_scroll = ttk.Scrollbar(display_frame)
        text_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))

        self.text_display = tk.Text(display_frame, height=15, width=60)
        self.text_display.grid(row=0, column=0, padx=5, pady=5)

        # 连接滚动条和文本区域
        self.text_display.config(yscrollcommand=text_scroll.set)
        text_scroll.config(command=self.text_display.yview)

        # 设置文本区域字体
        self.text_display.config(font=('Courier', 10))

    def add_edge(self):
        try:
            start = self.start_var.get()
            end = self.end_var.get()
            resistance = float(self.resistance_var.get())

            if not all([start, end]):
                messagebox.showerror("错误", "请输入起点和终点")
                return

            self.graph.add_edge(start, end, resistance)
            self.update_display()
            self.clear_inputs()
        except ValueError:
            messagebox.showerror("错误", "电阻值必须为数字")

    def detect_cycles(self):
        cycles = self.graph.detect_cycles()
        self.text_display.delete(1.0, tk.END)

        if not cycles:
            self.text_display.insert(tk.END, "未检测到环路")
        else:
            self.text_display.insert(tk.END, "检测到以下非法环路：\n")
            for i, cycle in enumerate(cycles, 1):
                path_str = " → ".join(cycle)
                self.text_display.insert(tk.END, f"环路 {i}: {path_str}\n")

    def show_shortest_path_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("计算最短路径")

        ttk.Label(dialog, text="起点:").grid(row=0, column=0)
        start = ttk.Entry(dialog, width=10)
        start.grid(row=0, column=1)

        ttk.Label(dialog, text="终点:").grid(row=0, column=2)
        end = ttk.Entry(dialog, width=10)
        end.grid(row=0, column=3)

        def calculate():
            result = self.graph.shortest_path(start.get(), end.get())
            if result:
                resistance, path = result
                self.text_display.delete(1.0, tk.END)
                self.text_display.insert(tk.END, f"最短路径: {' → '.join(path)}\n")
                self.text_display.insert(tk.END, f"总电阻: {resistance}Ω")
            dialog.destroy()

        ttk.Button(dialog, text="计算", command=calculate).grid(row=1, column=0, columnspan=4, pady=10)

    def show_all_paths_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("显示所有路径")

        ttk.Label(dialog, text="起点:").grid(row=0, column=0)
        start = ttk.Entry(dialog, width=10)
        start.grid(row=0, column=1)

        ttk.Label(dialog, text="终点:").grid(row=0, column=2)
        end = ttk.Entry(dialog, width=10)
        end.grid(row=0, column=3)

        def calculate():
            paths = self.graph.all_paths_simulation(start.get(), end.get())
            self.text_display.delete(1.0, tk.END)

            if not paths:
                self.text_display.insert(tk.END, f"没有找到从 {start.get()} 到 {end.get()} 的路径")
            else:
                self.text_display.insert(tk.END, f"从 {start.get()} 到 {end.get()} 的所有可能路径:\n")
                for path, resistance in paths:
                    path_str = " → ".join(path)
                    self.text_display.insert(tk.END, f"{path_str} ({resistance}Ω)\n")

            dialog.destroy()

        ttk.Button(dialog, text="显示", command=calculate).grid(row=1, column=0, columnspan=4, pady=10)

    def update_display(self):
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, "当前电路结构:\n")
        for node, edges in self.graph.adj_list.items():
            self.text_display.insert(tk.END, f"{node}: {edges}\n")

    def clear_inputs(self):
        self.start_var.set("")
        self.end_var.set("")
        self.resistance_var.set("")


def main():
    root = tk.Tk()
    app = CircuitAnalyzerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()