
from keras.models import load_model
import os
import random
import cv2
from scipy.optimize import minimize
import scipy.ndimage as nd
import numpy as np
from keras.utils import to_categorical
import matplotlib.pyplot as plt
from scipy.io import savemat
import matplotlib
# from noise_generator import occlusion
import tensorflow.compat.v1 as tf

def unison_shuffled(a, b):
    p = np.random.permutation(len(a))
    return a[p], b[p]

model = [load_model('C:\\Users\\Home\\Desktop\\hw2\\model_' + str(i) + 'final.h5') for i in range(6)]
def model_predict(DOG_image):
    global model
    threshold = [8, 0, 100, 0, 3]

    last_layer_out_sum = np.zeros((30, 30))

    v_prev = [np.zeros((1,) + input_shapes[1], dtype=np.float32), 0,
              np.zeros((1,) + input_shapes[3], dtype=np.float32), 0,
              np.zeros((1,) + input_shapes[5], dtype=np.float32)]

    mask = [np.ones((1,) + input_shapes[1]),
            np.ones((1,) + input_shapes[2]),
            np.ones((1,) + input_shapes[3]),
            np.ones((1,) + input_shapes[4]),
            np.ones((1,) + input_shapes[5])]

    cumulative_out = [np.zeros(input_shapes[0], dtype=np.float32),
                      np.zeros(input_shapes[1], dtype=np.float32),
                      np.zeros(input_shapes[2], dtype=np.float32),
                      np.zeros(input_shapes[3], dtype=np.float32),
                      np.zeros(input_shapes[4], dtype=np.float32),
                      np.zeros(input_shapes[5], dtype=np.float32),
                      np.zeros(input_shapes[6], dtype=np.float32),
                      np.zeros(50)]

    t = DOG_image.reshape((-1,)).copy()
    t.sort()
    t = t[-10000:]
    parts = np.percentile(t, np.linspace(0, 100, 31))
    del t

    # cv2.waitKey()
    for j in range(30, 0, -1):
        # lower_bound = 8.5 * (j - 1)
        lower_bound = parts[j - 1]
        # upper_bound = 8.5 * j
        upper_bound = parts[j + 1] if j <= 29 else 255

        # ret, img = cv2.threshold(DOG_image, (8.5 * i), 255, 0)
        img = DOG_image.copy()
        # plt.hist(DOG_image, bins=512)
        # plt.show()


        img[img <= lower_bound] = 0
        img[img > lower_bound] = 1
        img[DOG_image > upper_bound] = 0

        # if 1 not in img:
        #     continue
        # cv2.imshow('image', cv2.resize(img, None, fx=2, fy=2))
        # cv2.waitKey(200)
        # cv2.imshow('image', cv2.resize(np.zeros(img.shape), None, fx=2, fy=2))
        # cv2.waitKey(100)
        # if j == 30:

        input_img = img.reshape(1, 256, 256, 1)

        out = [input_img] + [np.zeros((1,) + input_shapes[1], dtype=np.float32),
                             np.zeros((1,) + input_shapes[2], dtype=np.float32),
                             np.zeros((1,) + input_shapes[3], dtype=np.float32),
                             np.zeros((1,) + input_shapes[4], dtype=np.float32),
                             np.zeros((1,) + input_shapes[5], dtype=np.float32),
                             np.zeros((1,) + input_shapes[6], dtype=np.float32),
                             np.zeros((1, 30))]

        cumulative_out[0] += out[0][0]

        # compute conv layer 1
        layer = 0
        v_prev[layer] += model[layer].predict(out[layer])
        v_prev[layer] = v_prev[layer] * mask[layer]
        thresh_passed = (v_prev[layer] > threshold[layer]).astype(np.float32)
        if 1 in thresh_passed[0]:
            v_max = v_prev[layer][0].max(axis=2)
            v_max_one_hot = (v_prev[layer][0] == v_max[:, :, None])
            out[layer + 1][0] = thresh_passed * v_max_one_hot

        # mask[layer] -= out[layer + 1]
        v_prev[layer][thresh_passed == 1] = 0

        # compute pooling1 layer 2
        layer = 1
        out[layer + 1] = model[layer].predict(out[1])
        out[layer + 1] *= mask[layer]
        # mask[layer] -= out[layer + 1]
        cumulative_out[layer + 1] += out[layer + 1][0]

        # ---------------------------------------------------------
        # compute conv layer 3
        layer = 2
        v_prev[layer] += model[layer].predict(out[layer])
        v_prev[layer] = v_prev[layer] * mask[layer]
        thresh_passed = (v_prev[layer] > threshold[layer]).astype(np.float32)
        out[layer + 1][0] = thresh_passed
        # mask[layer] -= out[layer + 1]
        v_prev[layer][thresh_passed == 1] = 0

        # compute pooling layer 3
        layer = 3
        out[layer + 1] = model[layer].predict(out[layer])
        out[layer + 1] *= mask[layer]
        # mask[layer] -= out[layer + 1]
        cumulative_out[layer + 1] += out[layer + 1][0]

        # ---------------------------------------------------------
        # compute conv layer 3
        layer = 4
        v_prev[layer] += model[layer].predict(out[layer])
        v_prev[layer] = v_prev[layer] * mask[layer]
        thresh_passed = (v_prev[layer] > threshold[layer]).astype(np.float32)
        out[layer + 1][0] = thresh_passed
        # mask[layer] -= out[layer + 1]
        v_prev[layer][thresh_passed == 1] = 0


        last_layer_out_sum[30 - j] = np.sum(np.sum(out[layer + 1][0], axis=1), axis=0)

        del img, out

    del v_prev, mask, cumulative_out

    return last_layer_out_sum

input_shapes = [(256, 256, 1),
                (256, 256, 4),
                (43, 43, 4),
                (43, 43, 50),
                (11, 11, 50),
                (11, 11, 30),
                (1, 1, 30)]

filter_size = [(5, 5),
               (7, 7),
               (19, 19),  # it was 16 * 16 -> we made it 17 * 17 to make it even
               (4, 4),
               (7, 7),
               (16, 16)]


imageFormats = ['jpg', 'png', 'gif']


def fined_images_name_test(baseAddress):
    files = []
    Y = []
    subFiles = os.listdir(baseAddress)
    random.shuffle(subFiles)
    for subFileName in subFiles:
        temp = os.path.join(baseAddress, subFileName)
        if os.path.isfile(temp):
            if temp[-3:] in imageFormats:
                files.append(temp)
                # print(temp[9])
                # cohers.append(int(temp[9] == 'f') * 100)
                print(baseAddress)
                Y.append(temp)
            # else:
            #     print(temp)
        else:
            f, y = fined_images_name_test(temp)
            files += f
            Y = Y + y
    return files, Y


def get_pred(images):
    pred = np.zeros((len(images), 30, 30))

    for i, image_name in enumerate(images):
        print(i)
        image = cv2.imread(image_name, 0)
        image = cv2.resize(image, (256, 256))
        # image = nd.gaussian_filter(image, sigma=8)
        DOG_image = image.astype(np.float32)
        DOG_image = cv2.GaussianBlur(DOG_image, (7, 7), 2)\
                    - cv2.GaussianBlur(DOG_image, (7, 7), 1)

        DOG_image = 255 * DOG_image / np.max(DOG_image)
        prd = model_predict(DOG_image)
        pred[i] = prd

        del image, DOG_image, prd
    return pred


images, y = fined_images_name_test('C:\\Users\\Home\\Desktop\\hw2\\data') # dataset path
y = np.array(y)
images = np.array(images)

print(y)

pred = get_pred(images)

np.save('pred_amin_all.npy', pred)
np.save('y_amin_all.npy', y)
