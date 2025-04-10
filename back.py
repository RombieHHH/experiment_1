from heapq import heappush, heappop
from math import inf

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
        cycles = set()  # 存储检测到的环路

        # 对每个节点执行DFS
        for start_node in self.adj_list:
            # 当前DFS路径中的节点
            stack = []
            # 标记当前DFS路径中的节点
            on_stack = set()

            def dfs(node):
                # 如果节点已在当前路径中，找到环路
                if node in on_stack:
                    # 找到环路的起点位置
                    start_idx = stack.index(node)
                    # 获取环路节点
                    cycle_nodes = stack[start_idx:] + [node]

                    # 标准化环路表示，使相同环路具有相同表示
                    # 1. 找到环路中字典序最小的节点
                    min_node_idx = 0
                    min_node = cycle_nodes[0]
                    for i, n in enumerate(cycle_nodes[:-1]):  # 最后一个节点是重复的，排除
                        if n < min_node:
                            min_node = n
                            min_node_idx = i

                    # 2. 从最小节点开始重新排列环路
                    normalized_cycle = tuple(cycle_nodes[min_node_idx:-1] +
                                             cycle_nodes[:min_node_idx] +
                                             [cycle_nodes[min_node_idx]])

                    # 添加标准化后的环路
                    cycles.add(normalized_cycle)
                    return

                # 将节点加入当前路径
                stack.append(node)
                on_stack.add(node)

                # 探索所有邻居
                for neighbor in self.adj_list.get(node, {}):
                    if neighbor == node:
                        # 处理自环
                        cycles.add((node, node))
                    else:
                        dfs(neighbor)

                # 回溯：从当前路径中移除节点
                stack.pop()
                on_stack.remove(node)

            # 从当前起点执行DFS
            dfs(start_node)

        # 输出结果
        if cycles:
            print("检测到以下非法环路：")
            for cycle in cycles:
                print(" → ".join(cycle))
        else:
            print("未检测到非法环路")

        return cycles

    def all_paths_simulation(self, start_node, end_node):
        """
        计算从起点到终点的所有可能路径及总电阻值

        参数:
        start_node -- 起始节点
        end_node -- 目标节点

        返回:
        路径列表，每个元素为(路径, 总电阻值)的元组
        """
        if start_node not in self.adj_list or end_node not in self.adj_list:
            print(f"错误：节点 {start_node} 或 {end_node} 不存在")
            return []

        all_paths = []
        current_path = [start_node]
        visited = {node: False for node in self.adj_list}

        def backtrack(node, resistance_sum):
            # 到达终点
            if node == end_node:
                all_paths.append((current_path.copy(), resistance_sum))
                return

            # 标记当前节点为已访问
            visited[node] = True

            # 探索所有邻接节点
            for neighbor, resistance in self.adj_list.get(node, {}).items():
                # 剪枝：避免循环路径
                if not visited[neighbor]:
                    # 添加节点到路径
                    current_path.append(neighbor)
                    # 递归探索
                    backtrack(neighbor, resistance_sum + resistance)
                    # 回溯：移除节点
                    current_path.pop()

            # 回溯：将节点标记为未访问，允许其在其他路径中使用
            visited[node] = False

        # 开始回溯搜索
        backtrack(start_node, 0)

        # 输出结果
        if all_paths:
            print(f"从 {start_node} 到 {end_node} 的所有可能路径:")
            for path, resistance in all_paths:
                path_str = " → ".join(path)
                print(f"{path_str} ({resistance}Ω)")
        else:
            print(f"没有找到从 {start_node} 到 {end_node} 的路径")

        return all_paths

    def shortest_path(self, start, end):
        """
        使用 Dijkstra 算法计算两点间电阻最小的路径

        参数:
        start -- 起始节点
        end -- 目标节点

        返回:
        (最小电阻值, 路径列表)
        """
        if start not in self.adj_list or end not in self.adj_list:
            print(f"错误：节点 {start} 或 {end} 不存在")
            return None

        # 初始化距离字典和父节点字典
        distances = {node: inf for node in self.adj_list}
        distances[start] = 0
        parents = {node: None for node in self.adj_list}

        # 优先队列，存储 (当前距离, 节点) 元组
        pq = [(0, start)]

        while pq:
            current_distance, current_node = heappop(pq)

            # 如果找到目标节点，终止搜索
            if current_node == end:
                break

            # 如果当前距离大于已知最短距离，跳过
            if current_distance > distances[current_node]:
                continue

            # 遍历所有邻接节点
            for neighbor, resistance in self.adj_list[current_node].items():
                distance = current_distance + resistance

                # 如果找到更短路径，更新距离和父节点
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    parents[neighbor] = current_node
                    heappush(pq, (distance, neighbor))

        # 构建最短路径
        if distances[end] == inf:
            print(f"不存在从 {start} 到 {end} 的路径")
            return None

        path = []
        current = end
        while current is not None:
            path.append(current)
            current = parents[current]
        path.reverse()

        # 输出结果
        print(f"\n最短路径：{' → '.join(path)}")
        print(f"总电阻：{distances[end]}Ω")

        return distances[end], path


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
        action = input("\n选择操作（add_edge/delete_node/delete_edge/detect_cycles/all_paths_simulation/shortest_path/exit）：").strip().lower()
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
        elif action == "all_paths_simulation":
            start, end = input("输入仿真的路径起点和终点（格式：起点 终点）：").split()
            graph.all_paths_simulation(start, end)
        elif action == "shortest_path":
            try:
                start, end = input("输入起点和终点（格式：起点 终点）：").split()
                graph.shortest_path(start, end)
            except ValueError:
                print("输入格式错误")
        elif action == "exit":
            print("退出程序")
            break
        else:
            print("无效操作，请重新输入")


if __name__ == "__main__":
    main()
