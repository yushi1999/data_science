'''
データサイエンス特論授業課題第1回
作成日：2022年6月19日
作成者：M1 203324 紺谷優志

IRISのデータをMatplotlibでプロットする
'''

import matplotlib.pyplot as plt
import pandas as pld
from sklearn.datasets import load_iris  # irisデータセットをロード

iris_dataset = load_iris()

# load_irisは独自のデータ構造なので、PandasのDataFrameに変換する
