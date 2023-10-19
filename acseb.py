import random
import numpy as np

import matplotlib.pyplot as plt

# 参数
k = 10  # 生成k个地图
n, m = 100, 100  # 每个地图的大小
obs_ratio = 0.1  # 障碍物地图占比
obs_size = 1  # 障碍物的最小尺寸：obs_size * obs_size

def check_connectivity(map_data):
    n = len(map_data)
    m = len(map_data[0])
    visited = [[False for _ in range(m)] for _ in range(n)]
    stack = []

    start_i, start_j = 0, 0
    for i in range(n):
        for j in range(m):
            if map_data[i][j] == 0:
                start_i, start_j = i, j
                break
        if map_data[start_i][start_j] == 0:
            break

    stack.append((start_i, start_j))
    visited[start_i][start_j] = True

    while stack:
        i, j = stack.pop()

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in directions:
            ni, nj = i + dx, j + dy
            if 0 <= ni < n and 0 <= nj < m and not visited[ni][nj] and map_data[ni][nj] == 0:
                visited[ni][nj] = True
                stack.append((ni, nj))

    for i in range(n):
        for j in range(m):
            if map_data[i][j] == 0 and not visited[i][j]:
                return False
    return True

#定义0为可行动区域，1为障碍物,1的比例不应超过60%
def generate_map(n, m, ratio):
    map_data = [[1 for _ in range(m)] for _ in range(n)]
    total_cells = n * m
    num_zeros = int(total_cells * (1 - ratio))
    num_extra_zeros = min(num_zeros * 0.2, (total_cells - num_zeros) * 0.5)
    num_ones = num_zeros + num_extra_zeros

    # 生成一个全为0的地图
    map_data[0][0] = 0

    # 用于记录每个位置是否已被访问
    visited = [[False for _ in range(m)] for _ in range(n)]
    visited[0][0] = True

    # 用于记录与初始位置相邻的位置
    stack = [(0, 0)]
    num_zeros -= 1

    # 使用随机洪泛算法填充0
    while len(stack) > 0:
        i, j = stack.pop()

        map_data[i][j] = 0

        if num_zeros <= 0:
            continue

        # 打乱方向的顺序
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            ni, nj = i + dx, j + dy
            if 0 <= ni < n and 0 <= nj < m and not visited[ni][nj]:
                visited[ni][nj] = True
                stack.append((ni, nj))
                num_zeros -= 1

    for _ in range(int(num_extra_zeros)):
        while True:
            i = random.randint(0, n - 1)
            j = random.randint(0, m - 1)
            if map_data[i][j] == 0:
                map_data[i][j] = 1

                if check_connectivity(map_data):  # 判断连通性
                    break
                else:
                    map_data[i][j] = 0
                    continue

    return map_data

def dfs(i, j, map_data, visited):
    n = len(map_data)
    m = len(map_data[0])

    if i < 0 or i >= n or j < 0 or j >= m or visited[i][j] or map_data[i][j] == 1:
        return

    visited[i][j] = True

    dfs(i-1, j, map_data, visited)
    dfs(i+1, j, map_data, visited)
    dfs(i, j-1, map_data, visited)
    dfs(i, j+1, map_data, visited)

def save_map(map_data, filename):
    with open(filename, 'w') as file:
        for row in map_data:
            file.write(' '.join(map(str, row)) + '\n')

def load_map(filename):
    map_data = []
    with open(filename, 'r') as file:
        for line in file:
            row = list(map(int, line.strip().split()))
            map_data.append(row)
    return map_data

def visualize_map(map_data, color_0, color_1):
    n = len(map_data)
    m = len(map_data[0])

    plt.figure(figsize=(m, m))
    plt.axis('off')

    cmap = plt.cm.colors.ListedColormap([color_0, color_1])

    full_map = np.ones((n, m))

    for i in range(n):
        for j in range(m):
            if map_data[i][j] == 0:
                full_map[i][j] = 0

    plt.imshow(full_map, cmap=cmap, aspect='equal')

    plt.show()

if obs_size > 1:
    m = m // obs_size
    n = n // obs_size

for i in range(k):
    map_data = generate_map(n, m, obs_ratio)
    if obs_size > 1:
        map_data = np.kron(map_data, np.ones((obs_size, obs_size), dtype=int))
    filename = f'map_{i+1}.txt'
    save_map(map_data, filename)

    print(f"Map {i+1}:")
    visualize_map(map_data, 'pink', 'black')
    print()

# 读取地图文件并可视化
for i in range(k):
    filename = f'map_{i+1}.txt'
    map_data = load_map(filename)

    print(f"Map {i+1}:")
    visualize_map(map_data, 'pink', 'black')
    print()