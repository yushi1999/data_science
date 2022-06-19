'''
データサイエンス特論授業課題第1回
作成日: 2022年6月19日
作成者: M1 203324 紺谷優志

IRISのデータをMatplotlibでプロットする
'''

import matplotlib.pyplot as plt
import pandas as pld
from sklearn.datasets import load_iris  # irisデータセットをロード

iris = load_iris()

markers = ["o", "^", "s"]  # 丸、三角、四角
colors = ["blue", "red", "green"]  # プロット時の色

x_num = 2
y_num = 3

# figure:描画領域全体
fig = plt.figure(figsize=(8, 6))  # figsize:幅と高さ(インチ)
# axes:(個別の)座標軸。figure内に複数並べることもできる。
ax = fig.add_subplot(111)  # 111はfigure内の1行目1列1番目の意味。

for i, label in enumerate(iris.target_names):
    # 散布図の内容を定義
    ax.scatter(x=iris.data[iris.target == i, x_num],
               y=iris.data[iris.target == i, y_num],
               label=iris.target_names[i],
               marker=markers[i], c=colors[i])

ax.legend(loc="best", fontsize=14)  # legend:グラフ中の凡例
ax.set_xlabel(iris.feature_names[x_num], size=14)  # x軸のラベルを設定
ax.set_ylabel(iris.feature_names[y_num], size=14)  # y軸のラベルを設定

plt.show()  # 描画
fig.savefig("ex1.pdf")  # pdfに保存
