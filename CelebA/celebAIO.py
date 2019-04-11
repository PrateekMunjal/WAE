import tensorflow as tf 
import numpy as np 
import os
import sys
import matplotlib.pyplot as plt 
import config
import PIL
from PIL import Image

opts = config.config_celebA
crop_style = opts['celebA_crop'];
celeb_source = opts['dataset_dir'];

#Given absolute image path, returns image in numpy
def read_image(path): 
    logging.debug('In read_image function for path : ',path);
    img = misc.imread(path);
    return img;

#Returns meta data about image i.e height,width,num_channels
def image_meta(image):
    logging.debug('In image_meta function');
    return image.shape[0],image.shape[1],image.shape[2];
    #return image.size[0],image.size[1],opts['num_channels'];

def denormalize_image(image):
    image /= 2. #rescale value from [-1,1] to [-0.5,0.5]
    image = image + 0.5 #rescale value from [-0.5,0.5] to [0,1]
    return image;

def plot_denormalized_image(image,title):
    image = denormalize_image(image);
    plt.figure();
    plt.title(title);
    plt.imshow(image);

def plot_image(image,title):
    plt.figure();
    plt.axis('off');
    plt.title(title);
    plt.imshow(image);
    
    #plt.show();
    #plt.close();

def crop(im):
    width = 178
    height = 218
    new_width = 140
    new_height = 140
    if crop_style == 'closecrop':
        # This method was used in DCGAN, pytorch-gan-collection, AVB, ...
        left = (width - new_width) / 2
        top = (height - new_height) / 2
        right = (width + new_width) / 2
        bottom = (height + new_height)/2
        im = im.crop((left, top, right, bottom))
        im = im.resize((64, 64), PIL.Image.ANTIALIAS)
    elif self.crop_style == 'resizecrop':
        # This method was used in ALI, AGE, ...
        im = im.resize((64, 78), PIL.Image.ANTIALIAS)
        im = im.crop((0, 7, 64, 64 + 7))
    else:
        raise Exception('Unknown crop style specified')
    return np.array(im).reshape(64, 64, 3) / 255.

def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def normalize_image(image):
    normalized_image = image - 0.5;
    normalized_image *= 2;
    # normalized_image = (image - np.min(image))/(np.max(image)-np.min(image));
    # normalized_image = 2*normalized_image;
    # normalized_image -= 1;
    return normalized_image;

def get_random_batch(file_iter,batch_size = 3,):
    random_file_iter = np.random.choice(file_iter,batch_size,replace=False);
    #print("Random_file_iter");
    #print(random_file_iter);
    #sys.exit(0);
    X = np.zeros([len(random_file_iter),opts['img_height'],opts['img_width'],opts['num_channels']]);
    #print(X.shape);
    index = -1;
    for f in random_file_iter:
        index += 1;
        f = f + '.jpg';
        curr_img = Image.open(f);
        curr_img = crop(curr_img);
        #print(np.min(curr_img));
        curr_img = normalize_image(curr_img);
        #print(np.min(curr_img));
        #print (curr_img.shape);
        X[index] = curr_img;
    return X;