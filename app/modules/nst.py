import numpy as np
import matplotlib
from matplotlib import gridspec
import matplotlib.pylab as plt
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from pathlib import Path
from PIL import Image

## paths definitions
path_model_folder = Path('../model')

## load nst model
hub_module = hub.load(str(path_model_folder))

## load image as tensorflow object
def decode_img(img_path):
        img = tf.io.read_file(str(img_path))
        img = tf.image.decode_jpeg(img, channels=3)
        img = tf.image.convert_image_dtype(img, tf.float32)
        img = tf.image.resize(img, [400,400])
        return img


def apply_neural_style_transfer(path_img_content, path_img_style, path_img_output):
    """
    Applies neural style transfer
    :returns : path_img_output
    """
    img_cnt = decode_img(str(path_img_content))
    img_cnt = tf.expand_dims(img_cnt, 0) if len(img_cnt.shape) == 3 else img_cnt
    img_style = decode_img(str(path_img_style))
    img_style = tf.expand_dims(img_style, 0) if len(img_style.shape) == 3 else img_style
    
    outputs = hub_module(tf.constant(img_cnt), tf.constant(img_style))
    img_output = tf.squeeze(outputs[0],0)
    img_output = Image.fromarray(np.uint8(np.array(img_output)*255.))
    img_output.save(path_img_output)
    
    return path_img_output
