import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

# 盤面のサイズNを入力として受け取る
N = st.number_input('Enter the size of the grid (N):', min_value=10, max_value=100, value=10)

# 縦の壁の情報をテキストエリアで受け取る
vertical_walls_input = st.text_area("縦の壁の情報を入力", height=150)

# 横の壁の情報をテキストエリアで受け取る
horizontal_walls_input = st.text_area("横の壁の情報を入力", height=150)

# マスの値の情報をテキストエリアで受け取る
grid_numbers_input = st.text_area("マスの値の情報を入力", height=150)

# 高橋君と青木君の初期位置を入力する
# initial_positions_input = st.text_input("高橋君と青木君の初期位置を入力", value="0 0 0 1")

# 文字列入力から青木君と高橋君の初期位置を解析する関数
def parse_positions(input_str):
    return list(map(int, input_str.split()))

# 青木君と高橋君の現在位置を取得
# pi, pj, qi, qj = parse_positions(initial_positions_input)

# 入力が適切に行われたかを確認する関数
def validate_input(*args):
    return all(arg != '' for arg in args) and all(arg is not None for arg in args)

# ユーザーが提供する出力情報（初期配置および操作）を入力する
user_output = st.text_area("初期位置および操作を入力", height=100)

# 文字列入力を数値のリストに変換する関数
def parse_input(input_str, is_grid=False):
    rows = input_str.split('\n')
    if is_grid:
        return [[int(num) for num in row.split()] for row in rows if row]
    else:
        return [[int(num) for num in row] for row in rows if row]
    
# 隣接するマスのペアの二乗和を計算する関数
def calculate_score(grid, vertical_walls, horizontal_walls):
    score = 0
    # 垂直方向の隣接マスのペアを調べる
    for i in range(N):
        for j in range(N-1):
            if vertical_walls[i][j] == 0:  # 壁がない場合
                score += (grid.iat[i, j] - grid.iat[i, j+1]) ** 2
    # 水平方向の隣接マスのペアを調べる
    for i in range(N-1):
        for j in range(N):
            if horizontal_walls[i][j] == 0:  # 壁がない場合
                score += (grid.iat[i, j] - grid.iat[i+1, j]) ** 2
    return score

def apply_action(grid, action, positions):
    pi, pj, qi, qj = positions
    s, d, e = action.split()
    s = int(s)

    # Apply the swap if needed
    if s == 1:
        grid.iat[pi, pj], grid.iat[qi, qj] = grid.iat[qi, qj], grid.iat[pi, pj]
    
    # Move Takahashi
    pi, pj = move_player(pi, pj, d)
    
    # Move Aoki
    qi, qj = move_player(qi, qj, e)

    return grid, (pi, pj, qi, qj)

# 入力が適切に行われている場合のみ処理を進める
if validate_input(vertical_walls_input, horizontal_walls_input, grid_numbers_input):

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

  pi, pj, qi, qj = initial_positions  # 高橋君と青木君の初期位置を取得

  # New code to create a slider and visualize step-by-step
  max_steps = len(actions)  # Total number of steps based on the actions
  step = st.slider("Step", 0, max_steps, 0)  # Slider to select the step



  # 盤面をDataFrameで作成する関数
  def create_grid(N, grid_numbers):
      grid = pd.DataFrame(grid_numbers)
      return grid

  grid = create_grid(N, grid_numbers)

  def move_player(i, j, action):
    if action == 'U':
        return max(0, i-1), j
    elif action == 'D':
        return min(N-1, i+1), j
    elif action == 'L':
        return i, max(0, j-1)
    elif action == 'R':
        return i, min(N-1, j+1)
    return i, j


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
  def visualize_grid_with_positions(grid, vertical_walls, horizontal_walls, pi, pj, qi, qj):
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

      # 現在のスコアを計算
      current_score = calculate_score(grid, vertical_walls, horizontal_walls)
      # D' (初期状態の二乗和) は最初にグリッドが生成されたときのスコアと仮定
      D_prime = current_score  # 初期状態のスコアとして現在のスコアを使用
      # D (最終状態の二乗和) は操作後のグリッドに対して計算されるスコアと仮定
      # ここでは操作を行っていないので、D_primeと同じになる
      D = current_score  # 最終状態のスコアとして現在のスコアを使用
      # 得点の計算
      score = max(1, round(10**6 * math.log2(D / D_prime))) if D_prime > 0 else 0

      for i in range(step):
        s, d, e = actions[i].split()
        pi, pj = move_player(pi, pj, d)  # 高橋君の移動を適用
        qi, qj = move_player(qi, qj, e)  # 青木君の移動を適用
        if s == '1':
            # 数字の交換
            grid.iat[pi, pj], grid.iat[qi, qj] = grid.iat[qi, qj], grid.iat[pi, pj]

      # 青木君と高橋君の現在位置をマークする
      ax.plot(pj, pi, "o", color="red", markersize=10)  # 高橋君の位置を赤い丸で表示
      ax.plot(qj, qi, "o", color="blue", markersize=10)  # 青木君の位置を青い丸で表示

      # Streamlit上に描画
      st.pyplot(fig)

      # scoreも描画
      # st.write(f"Score: {score}")
    



# 盤面のビジュアライズに壁の情報と青木君と高橋君の位置を含める関数を呼び出し
  visualize_grid_with_positions(grid, vertical_walls, horizontal_walls, pi, pj, qi, qj)

else:
    st.write("Please enter all input fields.")