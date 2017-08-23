import os, sys, numpy as np
import re
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def load_pfm(filename):
  color = None
  width = None
  height = None
  scale = None
  endian = None

  file = open(filename, 'rb')

  header = file.readline().rstrip()
 
  if header == 'PF':
    color = True    
  elif header == 'Pf':
    color = False
  else:
    raise Exception('Not a PFM file.')

  dim_match = re.match(r'^(\d+)\s(\d+)\s$', file.readline())
  if dim_match:
    width, height = map(int, dim_match.groups())
  else:
    raise Exception('Malformed PFM header.')

  scale = float(file.readline().rstrip())
  if scale < 0: # little-endian
    endian = '<'
    scale = -scale
  else:
    endian = '>' # big-endian
  data = np.fromfile(file, endian + 'f')
  shape = (height, width, 3) if color else (height, width)
  print "shape ===== ",shape
  return np.reshape(data, shape), scale

print('-------------------------------')



def save_pfm(filename, image, scale = 1):
  color = None
  file = open(filename,'wb')
  if image.dtype.name != 'float32':
    raise Exception('Image dtype must be float32.')

  if len(image.shape) == 3 and image.shape[2] == 3: # color image
    color = True
  elif len(image.shape) == 2 or len(image.shape) == 3 and image.shape[2] == 1: # greyscale
    color = False
  else:
    raise Exception('Image must have H x W x 3, H x W x 1 or H x W dimensions.')

  file.write('PF\n' if color else 'Pf\n')
  file.write('%d %d\n' % (image.shape[1], image.shape[0]))

  endian = image.dtype.byteorder

  if endian == '<' or endian == '=' and sys.byteorder == 'little':
    scale = -scale

  file.write('%f\n' % scale)

  image.tofile(file)  



KITTI_Disparity_Path = './disp_noc_0/'
KITTI_Disparity_Pngs = os.listdir(KITTI_Disparity_Path)

for eachpng in KITTI_Disparity_Pngs:
  print eachpng  + ' -> ' + str(eachpng)[0:8] + '0.pfm'
  png = mpimg.imread(KITTI_Disparity_Path + str(eachpng))
  save_pfm("./disp_noc_0_pfm/"+str(eachpng)[0:8] + '0.pfm', png * 255, 1)



