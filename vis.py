import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 盤面のサイズNを入力として受け取る
N = st.number_input('Enter the size of the grid (N):', min_value=10, max_value=100, value=10)

# 縦の壁の情報をテキストエリアで受け取る
vertical_walls_input = st.text_area("Enter the vertical walls (v) as N rows of 0s and 1s, each N-1 characters long:", height=150)

# 横の壁の情報をテキストエリアで受け取る
horizontal_walls_input = st.text_area("Enter the horizontal walls (h) as N-1 rows of 0s and 1s, each N characters long:", height=150)

# マスの値の情報をテキストエリアで受け取る
grid_numbers_input = st.text_area("Enter the grid numbers (a) as N rows of numbers, each separated by space:", height=150)

# ユーザーが提供する出力情報（初期配置および操作）を入力する
user_output = st.text_area("Enter the user output (initial positions and actions):", height=100)

# 文字列入力を数値のリストに変換する関数
def parse_input(input_str, is_grid=False):
    rows = input_str.split('\n')
    if is_grid:
        return [[int(num) for num in row.split()] for row in rows if row]
    else:
        return [[int(num) for num in row] for row in rows if row]
    
# 文字列入力を数値のリストに変換する関数
def parse_walls(input_str, vertical=True):
    lines = input_str.split('\n')
    if not lines[-1]:  # 最後の改行を削除
        lines.pop()
    walls = [[int(char) for char in line] for line in lines]
    if vertical:
        # 垂直壁はN行N-1列であるべき
        assert all(len(row) == N-1 for row in walls)
    else:
        # 水平壁はN-1行N列であるべき
        assert all(len(row) == N for row in walls)
    return walls

vertical_walls = parse_walls(vertical_walls_input, vertical=True)
horizontal_walls = parse_walls(horizontal_walls_input, vertical=False)
grid_numbers = [[int(num) for num in row.split()] for row in grid_numbers_input.split("\n") if row]

# ユーザー出力をパースする関数
def parse_user_output(user_output):
    lines = user_output.strip().split("\n")
    initial_positions = list(map(int, lines[0].split()))
    actions = [line for line in lines[1:] if line]  # 空行を除外
    
    return initial_positions, actions

initial_positions, actions = parse_user_output(user_output)  # この行を修正/確認

# 盤面をDataFrameで作成する関数
def create_grid(N, grid_numbers):
    grid = pd.DataFrame(grid_numbers)
    return grid

grid = create_grid(N, grid_numbers)


# 盤面を更新する関数
def update_grid(grid, actions, initial_positions):
    pi, pj, qi, qj = initial_positions  # 初期位置を設定
    for action in actions:
        try:
            s, d, e = action.split()
        except ValueError:
            continue  # フォーマットが不正な行は無視
        s = int(s)
        
        # 数字の交換
        if s == 1:
            grid.iat[pi, pj], grid.iat[qi, qj] = grid.iat[qi, qj], grid.iat[pi, pj]
        
        # 高橋君の移動
        if d == 'U': pi = max(0, pi-1)
        elif d == 'D': pi = min(N-1, pi+1)
        elif d == 'L': pj = max(0, pj-1)
        elif d == 'R': pj = min(N-1, pj+1)
        
        # 青木君の移動
        if e == 'U': qi = max(0, qi-1)
        elif e == 'D': qi = min(N-1, qi+1)
        elif e == 'L': qj = max(0, qj-1)
        elif e == 'R': qj = min(N-1, qj+1)

    return grid

# 盤面を更新
grid = update_grid(grid, actions, initial_positions)

# 盤面のビジュアライズに壁の情報を含める関数
# 盤面のビジュアライズに壁の情報を含める関数
def visualize_grid_with_walls(grid, vertical_walls, horizontal_walls):
    fig, ax = plt.subplots(figsize=(N, N))  # 盤面のサイズに応じて調整
    ax.matshow(grid, cmap='viridis', alpha=0.8)  # matshowを使用して盤面を表示

    # 壁の表示
    for i in range(N):
        for j in range(N-1):
            if vertical_walls[i][j] == 1:
                ax.plot([j + 0.5, j + 0.5], [i - 0.5, i + 0.5], 'k-', lw=2)
    for i in range(N-1):
        for j in range(N):
            if horizontal_walls[i][j] == 1:
                ax.plot([j - 0.5, j + 0.5], [i + 0.5, i + 0.5], 'k-', lw=2)
    # マスの数字の表示
    for i in range(N):
        for j in range(N):
            ax.text(j, i, str(grid.iat[i, j]), ha='center', va='center', color='white')

    # 軸の表示をオフにする
    ax.set_xticks([])
    ax.set_yticks([])
    ax.xaxis.set_major_formatter(plt.NullFormatter())
    ax.yaxis.set_major_formatter(plt.NullFormatter())

    # Streamlit上に描画
    st.pyplot(fig)


# 盤面のビジュアライズに壁の情報を含める関数を呼び出し
visualize_grid_with_walls(grid, vertical_walls, horizontal_walls)

