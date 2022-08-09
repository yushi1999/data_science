import numpy as np
import cv2
from cv2 import Mat
from IPython.display import Image, display


class TransferedPicture:  # 画像の相似変換
    def __init__(self, pic: Mat, scale, theta):
        self.orig_img = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
        h, w = self.orig_img.shape
        mat = cv2.getRotationMatrix2D(
            (w / 2, h / 2), theta, scale)  # 相似変換のパラメータ設定
        self.img = cv2.warpAffine(self.orig_img, mat, (w, h))  # 相似変換を実行
        self.scale = scale
        self.theta = theta

    def write(self, img_name):
        cv2.imwrite(img_name, self.img)

    def get_img_array(self):  # オリジナル画像と変換後画像の配列を得る
        return self.orig_img, self.img

    def get_deff_array(self, img, axis=0):  # 微分画像を得る
        # axis=0: x方向の微分, axis=1: y方向の微分
        h, w = img.shape
        mat = np.zeros([h, w])
        for i in range(1, h-1):
            for j in range(1, w-1):
                if axis == 0:
                    mat[i][j] = (int(img[i][j+1])-int(img[i][j-1]))*0.5
                elif axis == 1:
                    mat[i][j] = (int(img[i+1][j])-int(img[i-1][j]))*0.5
        return mat

    def smooth_def(self):  # x方向,y方向それぞれの平滑微分画像を生成
        self.gs = cv2.GaussianBlur(self.img, (3, 3), 3)
        # x方向の平滑微分画像
        dst_x = self.get_deff_array(self.gs, axis=0)
        # y方向の微分
        dst_y = self.get_deff_array(self.gs, axis=1)

        return dst_x, dst_y


class GaussNewton:
    def __init__(self, orig: np.array, st: np.array, i_x: np.array, i_y: np.array, theta: float, scale: float):
        # θとsを初期化
        self.theta = theta*np.pi/180
        self.scale = scale
        # 各画像配列を保持
        self.orig = orig
        self.st = st
        self.i_x, self.i_y = i_x, i_y
        self.h, self.w = orig.shape

    # 各微分値
    def dx_dtheta(self, x, y):
        return self.scale*(-2*x*np.sin(self.theta)-(2*y*np.cos(self.theta)))

    def dy_dtheta(self, x, y):
        return self.scale*(2*x*np.cos(self.theta)-(2*y*np.sin(self.theta)))

    def dx_dscale(self, x, y):
        return 2*x*np.cos(self.theta)-(2*y*np.sin(self.theta))

    def dy_dscale(self, x, y):
        return 2*x*np.sin(self.theta)+(2*y*np.cos(self.theta))

    # 1周分の計算を行う
    def calc_param(self):
        h, w = int(self.h/2), int(self.w/2)
        j_t = j_tt = j_s = j_ss = j_ts = .0
        #print("θ={0}, s={1}".format(self.theta*180/np.pi,self.scale))
        for i in range(-1*h, h):
            for j in range(-1*w, w):
                # 配列の座標を画像の中心を原点とした座標に変換
                x, y = j, -1*i  # y軸の正の方向を向かせる
                x_d = int(self.scale*(np.cos(self.theta)
                          * x-(np.sin(self.theta)*y)))
                y_d = int(self.scale*(np.sin(self.theta)
                          * x+(np.cos(self.theta)*y)))

                # 各微分値
                dxdt = self.dx_dtheta(x_d, y_d)
                dydt = self.dy_dtheta(x_d, y_d)
                dxds = self.dx_dscale(x_d, y_d)
                dyds = self.dy_dscale(x_d, y_d)

                # 配列の座標値に逆変換
                x, y = x+w, -1*y+h
                x_d, y_d = x_d+w-1, -1*y_d+h-1

                I_dash = float(self.st[y_d][x_d])
                I = float(self.orig[y][x])
                I_dash_x = float(self.i_x[y_d][x_d])
                I_dash_y = float(self.i_y[y_d][x_d])

                j_t += (I_dash-I)*(I_dash_x*dxdt+(I_dash_y*dydt))
                j_tt += np.square(I_dash_x*dxdt+(I_dash_y*dydt))
                j_s += (I_dash-I)*(I_dash_x*dxds+(I_dash_y*dyds))
                j_ss += np.square(I_dash_x*dxds+(I_dash_y*dyds))
                j_ts += (I_dash_x*dxdt+(I_dash_y*dydt)) * \
                    (I_dash_x*dxds+(I_dash_y*dyds))

        # delta_thetaとdelta_scaleの計算
        mt = np.array([[j_tt, j_ts], [j_ts, j_ss]])
        deltas = -1*np.linalg.pinv(mt).dot(np.array([j_t, j_s]).T)
        #print("Δθ={0}, Δs={1}".format(deltas[0]*180/np.pi,deltas[1]))
        return deltas[0], deltas[1]

    def until_convergence(self):
        eps = 0.00001
        old_dt = old_ds = 1000
        i = 1
        while(True):
            # print("{0}周目".format(i))
            new_dt, new_ds = self.calc_param()
            self.theta += new_dt
            self.scale += new_ds
            if abs(new_dt-old_dt) < eps and abs(new_ds-old_ds) < eps:
                print("収束を確認")
                print("{0}周目".format(i))
                print("最終値: θ={0}, s={1}".format(
                    self.theta*180/np.pi, self.scale))
                break
            i += 1
            old_dt, old_ds = new_dt, new_ds


if __name__ == '__main__':
    orig_name = "sc1.png"

    # thetaとscaleの初期値を適当に決める
    s, t = 0.5, 100
    tp = TransferedPicture(pic=cv2.imread(orig_name), scale=s, theta=t)

    # 画像データを得る
    orig_img, st_img = tp.get_img_array()
    orig_array, st_array = np.array(orig_img), np.array(st_img)

    # Iの計算
    i_x, i_y = tp.smooth_def()
    i_x_array, i_y_array = np.array(i_x), np.array(i_y)

    # ガウスニュートン法によるパラメータ推定
    for i in range(1, 11):
        theta = 20*i
        scale = 0.3
        gn = GaussNewton(orig=orig_array, st=st_array,
                         i_x=i_x_array, i_y=i_y_array, theta=theta, scale=scale)
        gn.until_convergence()
