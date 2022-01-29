#Import Function

from pydoc import text
from re import L
import torch
from torch import nn, load, utils
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
from torchvision import datasets, transforms, models
from torchvision.models.vgg import model_urls
from os import path, listdir
import os
model_urls['vgg19'] = model_urls['vgg19'].replace('https://', 'http://')

from scipy.spatial import distance_matrix
from scipy.spatial import distance
import pandas as pd
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import argparse
#import cv2

#VGG model
class VGG:
	def __init__(self):
		model = models.vgg19(pretrained=True, progress=True)
		model.classifier = nn.Sequential(*list(model.classifier.children())[:3])
		self.model = model.cuda().eval()

	def __call__(self, x):
		return self.model(x)
vgg = VGG()
def get_features(model, loader):
    features = []
    with torch.no_grad():
        for batch, _ in tqdm(loader):
            if torch.cuda.is_available():
                batch = batch.cuda()
            b_features = model(batch).detach().cpu().numpy()
            for f in b_features:
                features.append(f)

    return features
def get_dataset(images_path):
  transform = transforms.Compose([
    transforms.Resize(size=32),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
  ])

  dataset = datasets.ImageFolder(images_path, transform=transform)
  loader = utils.data.DataLoader(dataset, batch_size=100, shuffle=False, num_workers=1, pin_memory=True)
  return loader
def get_euclidean(base_car,diff_view):
    dist = []
    for i in range(len(diff_view)):
        x = distance.euclidean(base_car[i],diff_view[i])
        dist.append(x)
    return(dist)
def get_damage(distance):
    f_car = ((distance[0] - 3.57)/(37.564-3.57)*100)
    r_car = ((distance[1] - 4.308)/(37.966-4.308)*100)
    b_car = ((distance[2] - 3.401)/(21.090-3.401)*100)
    l_car = ((distance[3] - 11.230)/(48.075-11.230)*100)
    dmgs = [f_car,r_car,b_car,l_car]
    return dmgs


    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test program to learn about argparse ')
    parser.add_argument(
        '--c',
        type = str,
        help = 'path model')
    args = parser.parse_args()
    f  = args.c

    base_path = os.path.join('data/base/'+str(f))
    dmg_path = os.path.join('data/dmg/'+str(f))
    car_loader = get_dataset(base_path)
    dmg_loader = get_dataset(dmg_path)
    base_feat = get_features(vgg,car_loader)
    dmg_feat = get_features(vgg,dmg_loader)
    eucli= get_euclidean(base_feat,dmg_feat)
    show_out = get_damage(eucli)
    print(f'The front of  the  car was damaged {round(show_out[0],2)}%')
    print(f'The Right of  the  car was damaged {round(show_out[1],2)}%')
    print(f'The Back  of  the  car was damaged {round(show_out[2],2)}%')
    print(f'The Left  of  the  car was damaged {round(show_out[3],2)}%')