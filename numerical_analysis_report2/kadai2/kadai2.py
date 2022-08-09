#!/bin/python3

from PIL import Image, ImageFilter
import numpy as np

class GN:
    def __init__(self, fig_name, rot):
        self.image_in = Image.open(fig_name).convert('L').resize((64, 64))
        self.image_out = self.image_in.rotate(rot, expand=True)
        self.image_out = self.image_out.resize((
            int(round(self.image_out.width * 1.0)), 
            int(round(self.image_out.height * 1.0))
        ))
        # カーネル
        self.div_x = np.array([-1, 0, 1, -1, 0, 1, -1, 0, 1])
        self.div_y = np.array([-1, -1, -1, 0, 0, 0, 1, 1, 1])
        self.im = np.array(self.image_in)
        self.im_ = np.array(self.image_out)

    # 角度とスケールパラメータの初期値
    def set_init(self, theta_0, scale_0):
        self.theta_0 = theta_0
        self.scale_0 = scale_0

    def calc_param(self):
        theta = self.theta_0
        scale = self.scale_0
        count = 0 # 収束するまでに何回繰り返したか
        while True:
            image_ = self.image_out.rotate(-theta * 180 / np.pi).resize((
                int(round(self.image_out.width / scale)), 
                int(round(self.image_out.height / scale))
            ))
            filtered_x = image_.filter(ImageFilter.Kernel((3, 3), self.div_x, scale=6))
            filtered_y = image_.filter(ImageFilter.Kernel((3, 3), self.div_y, scale=6))
            image_x = filtered_x.rotate(theta * 180 / np.pi, expand=True).resize((
                int(round(filtered_x.width * scale)), 
                int(round(filtered_x.height * scale))
            ))
            image_y = filtered_y.rotate(theta * 180 / np.pi, expand=True).resize((
                int(round(filtered_y.width * scale)), 
                int(round(filtered_y.height * scale))
            ))
            im_x = np.array(image_x)
            im_y = np.array(image_y)
            j_th, j_thth, j_s, j_ss, j_ths = 0., 0., 0., 0., 0.
            for y in range(self.image_in.height):
                y -= self.image_in.height / 2.0
                for x in range(self.image_in.width):
                    x -= self.image_in.width / 2.0
                    x_ = scale * (x * np.cos(theta) - y * np.sin(theta))
                    y_ = scale * (x * np.sin(theta) + y * np.cos(theta))
                    dxdth = scale * (-x * np.sin(theta) - y * np.cos(theta))
                    dydth = scale * (x * np.cos(theta) - y * np.sin(theta))
                    dxds = x * np.cos(theta) - y * np.sin(theta)
                    dyds = x * np.sin(theta) + y * np.cos(theta)
                    didx = self.acc(im_x, im_x, x_, y_)
                    didy = self.acc(im_y, im_x, x_, y_)
                    tmp_i = int(self.acc(self.im_, im_x, x_, y_)) - self.acc(self.im, im_x, x, y)
                    tmp_th = didx * dxdth + didy + dydth
                    tmp_s = didx * dxds + didy + dyds

                    j_th += tmp_i * tmp_th
                    j_thth += tmp_th * tmp_th
                    j_s += tmp_i * tmp_s
                    j_ss += tmp_s * tmp_s
                    j_ths += tmp_th * tmp_s

            h = np.array([[j_thth, j_ths], [j_ths, j_ss]])
            j_x = np.array([[j_th], [j_s]])
            delta = -np.linalg.inv(h).dot(j_x)

            theta += delta[0, 0]
            scale += delta[1, 0]
            count += 1
            if np.linalg.norm(delta, ord=2) < 0.03:
                break
        return theta, scale, count

    def acc(self, fig, im_x, x, y):
        yi, xi = int(round(y + fig.shape[0] / 2.)), int(round(x + fig.shape[1] / 2.))
        try:
            return im_x[yi, xi]
        except Exception:
            return 0

if __name__ == '__main__':
    scale_0 = 0.5
    rot = 25
    for i in range(10):
        theta_0 = (i*20)/180*np.pi

        gn_line = GN(fig_name='./line.jpg', rot=rot)
        gn_line.set_init(theta_0=theta_0, scale_0=scale_0)
        theta, scale, count = gn_line.calc_param()
        print(i*20, theta*(180/np.pi), scale, count)
        
        gn_tri = GN(fig_name='./tri.jpg', rot=rot)
        gn_tri.set_init(theta_0=theta_0, scale_0=scale_0)
        theta, scale, count = gn_tri.calc_param()
        print(i*20, theta*(180/np.pi), scale, count)

        gn_cat = GN(fig_name='./cat.jpg', rot=rot)
        gn_cat.set_init(theta_0=theta_0, scale_0=scale_0)
        theta, scale, count = gn_cat.calc_param()
        print(i*20, theta*(180/np.pi), scale, count)