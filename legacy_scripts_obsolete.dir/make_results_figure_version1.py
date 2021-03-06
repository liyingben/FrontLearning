u"""
make_results_figure

Plot Figure 3 of paper. Temporary script for figure.
"""

import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

#-- directory setup
#- current directory
current_dir = os.path.dirname(os.path.realpath(__file__))
main_dir = os.path.join(current_dir,'..','FrontLearning_data')
glacier_ddir = os.path.join(main_dir,'all_data2.dir')
ddir = os.path.join(glacier_ddir, 'data/test')

prefix = 'LT05_L1TP_233013_19890629_20170202_01_T1_B2' #'LE07_L1TP_233013_20000331_20170212_01_T2_B8'
fig, ax = plt.subplots(nrows=4, ncols=4, figsize=(7, 9),
                                    sharex=True, sharey=True)

#-- make custom colormap for final panel (comparison)
colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)] # red, green, blue, white
my_cm = LinearSegmentedColormap.from_list('myColors', colors, N=4)


in_img_file = os.path.join(ddir,'images_equalize_autocontrast_smooth_edgeEnhance',\
    '%s_Subset.png'%prefix)
in_img = np.array(Image.open(in_img_file).convert('L'))/255.


front_file = os.path.join(ddir,'labels','%s_Front.png'%prefix)
front = np.array(Image.open(front_file).convert('L'))/255.



f = os.path.join(ddir,'output_10batches_100epochs_4layers_32init_82.22weight_w0.2drop_equalize_autocontrast_smooth_edgeEnhance_cropped',\
    '%s_nothreshold.png'%prefix)
l4_noAug = np.array(Image.open(f).convert('L'))/255.


f = os.path.join(ddir,'output_10batches_60epochs_4layers_32init_82.22weight_w0.2drop_augment-x2_equalize_autocontrast_smooth_edgeEnhance_cropped',\
    '%s_nothreshold.png'%prefix)
l4_augx2 = np.array(Image.open(f).convert('L'))/255.


f = os.path.join(ddir,'output_10batches_60epochs_4layers_32init_82.22weight_w0.2drop_augment-x3_equalize_autocontrast_smooth_edgeEnhance_cropped',\
    '%s_nothreshold.png'%prefix)
l4_augx3 = np.array(Image.open(f).convert('L'))/255.


f = os.path.join(ddir,'output_10batches_60epochs_5layers_32init_86.60weight_w0.2drop_equalize_autocontrast_smooth_edgeEnhance_cropped',\
    '%s_nothreshold.png'%prefix)
l5_noAug = np.array(Image.open(f).convert('L'))/255.

f = os.path.join(ddir,'output_3batches_60epochs_4layers_32init_82.22weight_w0.2drop_equalize_autocontrast_smooth_edgeEnhance_cropped',\
    '%s_nothreshold.png'%prefix)
l4_3b = np.array(Image.open(f).convert('L'))/255.

f = os.path.join(ddir,'output_30batches_100epochs_4layers_32init_82.22weight_w0.2drop_equalize_autocontrast_smooth_edgeEnhance_cropped',\
    '%s_nothreshold.png'%prefix)
l4_30b = np.array(Image.open(f).convert('L'))/255.

f = os.path.join(ddir,'output_10batches_4layers_32init_1.00weight_w0.2drop_equalize_autocontrast_smooth_edgeEnhance_cropped',\
    '%s_nothreshold.png'%prefix)
l4_noweight = np.array(Image.open(f).convert('L'))/255.

sobel_out_file = os.path.join(ddir,'output_sobel_equalize_autocontrast_smooth_edgeEnhance',\
    '%s.png'%prefix)
sobel_out = np.array(Image.open(sobel_out_file).convert('L'))/255.

cnn_p_file = os.path.join(ddir,'Post Processing Results/CNN HF/CNN HF Post-Processed','%s_Solution.png'%prefix)
cnn_p = np.array(Image.open(cnn_p_file).convert('L'))/255.

sobel_p_file = os.path.join(ddir,'Post Processing Results/Sobel/Sobel Post-Processed','%s_Solution.png'%prefix)
sobel_p = np.array(Image.open(sobel_p_file).convert('L'))/255.

#-- input image
ax[0,1].imshow(in_img, cmap=plt.cm.gray)
ax[0,1].set_title(r"$\bf{a)}$" + " Pre-processsed Input", fontsize=12, color='navy')

#-- true front
ax[0,2].imshow(front, cmap=plt.cm.gray)
ax[0,2].set_title(r"$\bf{b)}$" + " True Front", fontsize=12, color='navy')

#-- 4 layer standard
ax[1,0].imshow(l4_noAug, cmap=plt.cm.gray)
ax[1,0].set_title(r"$\bf{c)}$" + " No Augmentation", fontsize=12, color='navy')

#-- 4 layer aug x2
ax[1,1].imshow(l4_augx2, cmap=plt.cm.gray)
ax[1,1].set_title(r"$\bf{d)}$" + " Augmented:\nMirrored", fontsize=12, color='navy')

#-- 4 layer aug x3
ax[1,2].imshow(l4_augx3, cmap=plt.cm.gray)
ax[1,2].set_title(r"$\bf{e)}$" + " Augmented:\nMirrored & Inverted", fontsize=12, color='navy')

#-- 5 layer 
ax[1,3].imshow(l5_noAug, cmap=plt.cm.gray)
ax[1,3].set_title(r"$\bf{f)}$" + " 37 Layers", fontsize=12, color='navy')

#-- 4 layer 30 batches
ax[2,0].imshow(l4_30b, cmap=plt.cm.gray)
ax[2,0].set_title(r"$\bf{g)}$" + " batch-size 30", fontsize=12, color='navy')

#-- 4 layer 3 batches
ax[2,1].imshow(l4_3b, cmap=plt.cm.gray)
ax[2,1].set_title(r"$\bf{h)}$" + " batch-size 3", fontsize=12, color='navy')

#-- 4 layer no weight
ax[2,2].imshow(l4_noweight, cmap=plt.cm.gray)
ax[2,2].set_title(r"$\bf{i)}$" + " No Weights", fontsize=12, color='navy')

#-- sobel
ax[2,3].imshow(sobel_out, cmap=plt.cm.gray)
ax[2,3].set_title(r"$\bf{j)}$" + " Sobel", fontsize=12, color='navy')

#-- NN post procossed
#-- combine cnn output and true front
out_nn = np.ones(front.shape)
ind1 = np.where(cnn_p==0.)
out_nn[ind1] = 0.0
ind2 = np.where(front==0.)
out_nn[ind2] = 0.6
ax[3,1].imshow(out_nn, cmap=my_cm)
ax[3,1].set_title(r"$\bf{k)}$" + " NN Comparison", fontsize=12, color='navy')
#-- make fake legend
ax[3,1].plot([],[],'-r',label='NN\nPost-processed')
ax[3,1].plot([],[],'-b',label='True Front')
ax[3,1].legend(loc='lower center',framealpha=1.0)


#-- sobel post processed
#-- combine sobel output and true front
out_s = np.ones(front.shape)
ind1 = np.where(sobel_p==0.)
out_s[ind1] = 0.0
ind2= np.where(front==0.)
out_s[ind2] = 0.6
ax[3,2].imshow(out_s, cmap=my_cm)
ax[3,2].set_title(r"$\bf{l)}$" + " Sobel Comparison", fontsize=12, color='navy')
#-- make fake legend
ax[3,2].plot([],[],'-r',label='Sobel\nPost-processed')
ax[3,2].plot([],[],'-b',label='True Front')
ax[3,2].legend(loc='lower center',framealpha=1.0)

for i in range(4):
    for j in range(4):
        #ax[i,j].axis('off')
        ax[i,j].axis('equal')
        ax[i,j].get_xaxis().set_ticks([])
        ax[i,j].get_yaxis().set_ticks([])
        ax[i,j].spines['top'].set_visible(True)
        ax[i,j].spines['right'].set_visible(True)
        ax[i,j].spines['bottom'].set_visible(True)
        ax[i,j].spines['left'].set_visible(True)
        ax[i,j].spines['bottom'].set_color('0.5')
        ax[i,j].spines['top'].set_color('0.5')
        ax[i,j].spines['right'].set_color('0.5')
        ax[i,j].spines['left'].set_color('0.5')

#-- no axes for hidden plots
ax[0,0].axis('off')
#ax[0,1].axis('off')
ax[0,3].axis('off')
ax[3,0].axis('off')
ax[3,3].axis('off')
fig.tight_layout()
#plt.show()
plt.savefig(os.path.join(ddir,'Figure_3_v1.pdf'),format='pdf',dpi=300)