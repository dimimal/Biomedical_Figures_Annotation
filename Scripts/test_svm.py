#!/usr/bin/python3

import os
import sys
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score
import argparse
import matplotlib.pyplot as plt
import pandas as pd
import pickle
from train_svm import load_image, loadModel
import cv2 as cv
from keras.preprocessing import image
from keras.applications.resnet50 import ResNet50, preprocess_input


PATH      = '/home/dimitris/GitProjects/Biomedical_Figure_Annotator/model.pkl'
TEST_PATH = '/home/dimitris/GitProjects/Biomedical_Figure_Annotator/test_data.csv'

def plot_results():
    pass

def parse_arguments():
    parser = argparse.ArgumentParser(description='Path arguments')
    parser.add_argument('-mp', '--model_path', nargs=1)
    parser.add_argument('-tp', '--test_path', nargs=1)
    return parser.parse_args()

def load_svm(path):
    svm = joblib.load(path)
    return svm

def check_args(args):
    if not os.path.exists(args.model_path[0]) and os.path.exists(args.testPath[0]):
        raise Exception('Missing Paths: \n === \n model Path: {} \n test Path {}')
        sys.exit(-1)

def load_data(path):
    data_frame = pd.read_csv(path, header=None)#, index_col=0)
    return data_frame[0].tolist(), np.array(data_frame[1].values)

def main(args):
    feats = np.array([])
    print(args)
    print(args.model_path)
    print(type(args.model_path))
    check_args(args)
    svm_model = load_svm(args.model_path[0])   
    figures, labels = load_data(args.test_path[0])
    model = loadModel('vgg')
    for image in figures:
        figure = load_image(image)
        if feats.size == 0:
            feats = model.predict(figure)
        else:
            feats = np.concatenate((feats, model.predict(figure)), axis=0)
    
    #feats = np.max(feats, axis=-1)
    feats = np.reshape(feats, (feats.shape[0],-1))
    predictions = svm_model.predict(feats)
    score = accuracy_score(labels, predictions)
    print('Score {}'.format(score))
    print('Predictions {}'.format(predictions))
    print('labels {}'.format(labels))
if __name__ == '__main__':
    args = parse_arguments()
    main(args)
    sys.exit(1)
