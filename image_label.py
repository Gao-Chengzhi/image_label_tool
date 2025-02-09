from cv2 import namedWindow, imshow, waitKeyEx, imread
import os
import shutil
import time
import sys
import csv
leftkeys = (81, 110, 65361, 2424832)
rightkeys = (83, 109, 65363, 2555904)
# 当前脚本工作的目录路径
root_dir = os.getcwd()
# print(root_dir)
# os.path.abspath()获得绝对路径
root_absdir = os.path.abspath(os.path.dirname(__file__))
# print(root_absdir)
# 待标注图片路径
unlabelled_image_dir = './data_all/' 

def make_dirs2(n):
    if not os.path.exists(os.path.join(root_dir,'labelled_images', n)):
        os.makedirs(os.path.join(root_dir, 'labelled_images', n))

def resume():
    labelled_images = []
    if os.path.exists(os.path.join(root_dir,'labelled_images')):
        cls_list = os.listdir(os.path.join(root_dir,'labelled_images'))
        for c in cls_list:
            image_list = os.listdir(os.path.join(root_dir,'labelled_images',c))
            labelled_images.extend(image_list)
    return labelled_images
def Classification_Tools(num_cls):
    labelled_images = resume()
    with open('test.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if len(labelled_images) == 0:
            writer.writerow(['id', 'prediction'])
        data_dir = unlabelled_image_dir   # 待分类数据路径
        if not os.path.exists(data_dir):
            print('data_dir not exists, please put data to: ', data_dir)
            time.sleep(5)
            exit()
        unconfirmed = 'unconfirmed'  # 不确定数据存放路径
        make_dirs2(unconfirmed)
        for i in range(num_cls):
            make_dirs2(str(i))
        image_list = os.listdir(data_dir)
        if len(image_list) == 0:
            print('no image in %s ... please put data to: %s'%(data_dir, data_dir))
            time.sleep(5)
            exit()
        namedWindow('Classification_Tools', 0)
        i = 0
        coccus_label = None
        while True:
            assert i < len(image_list), ('no image left...')
            print('i', i)
            image_path = os.path.join(data_dir, image_list[i])
            print(image_path)
            if image_path in labelled_images:
                continue
            image = imread(image_path)
            print(image.shape)
            imshow('Classification_Tools', image)
            key = waitKeyEx()

            if key == ord('d'):
                coccus_label = 'unconfirmed'
                shutil.move(image_path, os.path.join(root_dir, 'labelled_images', unconfirmed))
                i += 1  # (i + 1) % len(image_list)
            if key in rightkeys:
                i += 1  # (i + 1) % len(image_list)
            if key in leftkeys and coccus_label != None:
                # if not os.path.exists(os.path.join(('./' + str(coccus_label)), image_list[i-1])):
                print('leftkeys:', os.path.join(('./' + str(coccus_label)), image_list[i - 1]))
                if os.path.exists(os.path.join(('./' + str(coccus_label)), image_list[i - 1])):
                    print('ssssssssssssss', os.path.join(('./' + str(coccus_label)), image_list[i - 1]))
                    shutil.move(os.path.join(('./' + 'labelled_images/' + str(coccus_label)), image_list[i - 1]), data_dir)
                i -= 1
                if i < 0:
                    i = len(image_list) - 1

            if (key == ord('q')) or (key == 27):
                break

            for j in range(num_cls):
                if key & 0xFF == ord(str(j)):
                    coccus_label = str(j)
                
                    writer.writerow([image_list[i], coccus_label])
                    shutil.move(image_path, os.path.join(root_dir, 'labelled_images/', str(j)))
                    i += 1  # (i + 1) % len(image_list)
                    break


if __name__ == '__main__':
    # num_cls = sys.argv[1] # 传入类别数量
    num_cls = 2
    Classification_Tools(num_cls)
