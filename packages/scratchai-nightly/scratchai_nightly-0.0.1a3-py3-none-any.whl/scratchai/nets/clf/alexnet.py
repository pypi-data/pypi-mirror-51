"""
Alexnet

https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-
convolutional-neural-networks.pdf
from Alex Krizhevsky Ilya Sutskever Geoffrey E. Hinton
"""

import torch
import torch.nn as nn

from scratchai.nets.common import Flatten
from scratchai.utils import load_pretrained
from scratchai.pretrained import urls


__all__ = ['alexnet', 'alexnet_mnist']


def conv(ic:int, oc:int, k:int=3, s:int=1, p:int=1, pool:bool=True):
  layers = [nn.Conv2d(ic, oc, k, s, p), nn.ReLU(inplace=True)]
  if pool: layers += [nn.MaxPool2d(3, 2)]
  return layers

def linear(inn:int, otn:int):
  return [nn.Dropout(), nn.Linear(inn, otn), nn.ReLU(inplace=True)]

class Alexnet(nn.Module):
  """
  Implmentation of Alexnet.  
  
  Arguments 
  --------- 
  nc : int 
       # of classes 
  ic : int 
       # of channels

  References
  ----------
  https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-
  convolutional-neural-networks.pdf
  """
  def __init__(self, nc:int=1000, ic:int=3):
    super().__init__()
    # Special Case: MNIST. (2D inputs)
    ic2 = 64 if ic == 3 else 1
    first_layer = conv(ic, 64, 11, 4, 2) if ic == 3 else []
    self.features = nn.Sequential(*first_layer, *conv(ic2, 192, 5, p=2), 
                                  *conv(192, 384, pool=False), 
                                  *conv(384, 256, pool=False), 
                                  *conv(256, 256))

    self.avgpool = nn.AdaptiveAvgPool2d((6, 6))

    self.classifier = nn.Sequential(*linear(256*6*6, 4096),
                                    *linear(4096, 4096), nn.Linear(4096, nc))

  def forward(self, x):
    x = self.features(x)
    x = self.avgpool(x)
    x = x.reshape(x.size(0), -1)
    x = self.classifier(x)
    return x


def alexnet_mnist(pretrained=True, **kwargs):
  cust_nc = kwargs['nc'] if 'nc' in kwargs else None
  kwargs['ic'] = 1; kwargs['nc'] = 10
  net = Alexnet(**kwargs)
  if pretrained:
    return load_pretrained(net, urls.alexnet_mnist_url, 'alexnet_mnist', 
                           nc=cust_nc, attr='classifier', inn=9216)
  return net

def alexnet(pretrained=True, **kwargs):
  cust_nc = None
  if pretrained and 'nc' in kwargs: cust_nc = kwargs['nc']; kwargs['nc'] = 1000
  net = Alexnet(**kwargs)
  if pretrained:
    return load_pretrained(net, urls.alexnet_url, 'alexnet', nc=cust_nc, 
                           attr='classifier', inn=9216)
  return net
