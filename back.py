class Graph:
    def __init__(self):
        # 使用字典嵌套字典结构存储有向邻接表
        # 外层键为节点，内层键为邻接节点，值为电阻
        self.adj_list = {}

    def parse_input(self):
        """解析用户输入，构建有向邻接表"""
        try:
            # 读取节点数和边数
            nodes, edges = map(int, input("输入节点数和边数（格式：节点数 边数）：").split())
            print(f"节点数：{nodes}，边数：{edges}")

            # 逐行读取边的信息
            for _ in range(edges):
                line = input("输入边信息（格式：起点 终点 电阻值）：").strip().split()
                if len(line) != 3:
                    print("输入格式错误，应为：起点 终点 电阻值")
                    continue
                start, end, resistance = line[0], line[1], float(line[2])
                self.add_edge(start, end, resistance)
        except ValueError as e:
            print(f"输入错误：{e}，请确保输入正确的数字格式")
        except Exception as e:
            print(f"发生异常：{e}")

    def add_node(self, node):
        """添加节点，如果节点不存在则初始化"""
        if node not in self.adj_list:
            self.adj_list[node] = {}

    def add_edge(self, start, end, resistance):
        """添加有向边，仅存储单向关系"""
        # 添加起点和终点节点（如果不存在）
        self.add_node(start)
        self.add_node(end)
        # 有向边：仅从 start 到 end
        self.adj_list[start][end] = resistance
        print(f"添加边：{start} → {end}，电阻值：{resistance}Ω")

    def delete_node(self, node):
        """删除节点及其所有出边和入边"""
        if node in self.adj_list:
            # 删除所有指向该节点的入边
            for n in list(self.adj_list.keys()):
                if node in self.adj_list[n]:
                    del self.adj_list[n][node]
            # 删除节点及其出边
            del self.adj_list[node]
            print(f"删除节点：{node}")
        else:
            print(f"节点 {node} 不存在")

    def delete_edge(self, start, end):
        """删除指定有向边"""
        if start in self.adj_list and end in self.adj_list[start]:
            del self.adj_list[start][end]
            print(f"删除边：{start} → {end}")
        else:
            print(f"边 {start} → {end} 不存在")

    def display_graph(self):
        """显示当前邻接表内容"""
        if not self.adj_list:
            print("图为空")
            return
        print("当前邻接表：")
        for node in self.adj_list:
            connections = self.adj_list[node]
            print(f"{node}: {connections}")

    def detect_cycles(self):
        """检测图中的所有非法环路（包括自环和多节点环路）"""
        visited = set()  # 记录已访问的节点
        cycles = set()  # 存储检测到的独立环路（以元组形式）

        def dfs(node, path):
            """递归 DFS 辅助函数，检测从 node 开始的环路"""
            # 如果当前节点已在路径中，说明发现环路
            if node in path:
                cycle_start_index = path.index(node)
                cycle = tuple(path[cycle_start_index:] + [node])
                cycles.add(cycle)
                return
            # 如果节点已被访问且不在当前路径中，跳过
            if node in visited:
                return
            visited.add(node)
            path.append(node)
            # 遍历当前节点的邻接节点
            for neighbor in self.adj_list.get(node, {}):
                if neighbor == node:
                    # 检测到自环，直接记录
                    cycles.add((node, node))
                else:
                    # 继续 DFS 遍历
                    dfs(neighbor, path)
            path.pop()  # 回溯，移除当前节点

        # 从每个未访问的节点开始 DFS，确保检测所有独立环路
        for node in self.adj_list:
            if node not in visited:
                dfs(node, [])

        # 输出检测结果
        if cycles:
            print("检测到以下非法环路：")
            for cycle in cycles:
                print(" → ".join(cycle))
        else:
            print("未检测到非法环路")

        return cycles

def main():
    # 创建图实例
    graph = Graph()

    # 示例：解析用户输入
    print("请输入电路节点和边的信息：")
    graph.parse_input()

    # 显示初始邻接表
    graph.display_graph()

    # 示例动态操作
    while True:
        action = input("\n选择操作（add_edge/delete_node/delete_edge/detect_cycles/exit）：").strip().lower()
        if action == "add_edge":
            try:
                start, end, resistance = input("输入边信息（格式：起点 终点 电阻值）：").split()
                graph.add_edge(start, end, float(resistance))
                graph.display_graph()
            except ValueError:
                print("电阻值必须为数字")
        elif action == "delete_node":
            node = input("输入要删除的节点：")
            graph.delete_node(node)
            graph.display_graph()
        elif action == "delete_edge":
            start, end = input("输入要删除的边（格式：起点 终点）：").split()
            graph.delete_edge(start, end)
            graph.display_graph()
        elif action == "detect_cycles":
            graph.detect_cycles()
        elif action == "exit":
            print("退出程序")
            break
        else:
            print("无效操作，请重新输入")


if __name__ == "__main__":
    main()
