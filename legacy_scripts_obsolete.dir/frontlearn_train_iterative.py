#!/usr/bin/env python
u"""
frontlearn_train_iterative.py
by Yara Mohajerani (04/2018)

Train U-Net model in frontlearn_unet.py

Update History
        04/2018 Written
"""
import os
import numpy as np
import keras
from keras.preprocessing import image
import imp
import sys
from glob import glob
from PIL import Image
import matplotlib.pyplot as plt

#-- read in images
def load_data(trn_dir,tst_dir,subdir):
    #-- make subdirectories for input images
    trn_subdir = os.path.join(trn_dir,subdir)
    tst_subdir = os.path.join(tst_dir,subdir)
    #-- get a list of the input files
    trn_list = glob(os.path.join(trn_subdir,'*.png'))
    tst_list = glob(os.path.join(tst_subdir,'*.png'))
    #-- get just the file names
    trn_files = [os.path.basename(i) for i in trn_list]
    tst_files = [os.path.basename(i) for i in tst_list]

    #-- read training data
    n = len(trn_files)
    #-- get dimensions, force to 1 b/w channel
    w,h = np.array(Image.open(trn_list[0]).convert('L')).shape

    train_img = np.zeros((n,h,w,1))
    train_lbl = np.zeros((n,w,h,1))
    for i,f in enumerate(trn_files):
        #-- same file name but different directories for images and labels
        train_img[i,:,:,0] = np.array(Image.open(os.path.join(trn_subdir,f)).convert('L'))/255.
        train_lbl[i,:,:,0] = np.array(Image.open(os.path.join(trn_dir,'labels',f)).convert('L'))/255.

    #-- also get the test data
    n_test = len(tst_files)
    #-- get dimensions, force to 1 b/w channel
    w_test,h_test = np.array(Image.open(tst_list[0]).convert('L')).shape
    test_img = np.zeros((n_test,h_test,w_test,1))
    for i in range(n_test):
        test_img[i,:,:,0] = np.array(Image.open(tst_list[i]).convert('L'))/255.

    return {'trn_img':train_img,'trn_lbl':train_lbl,'tst_img':test_img,\
        'trn_names':trn_files,'tst_names':tst_files}

def train_model(parameters):
    n_batch = int(parameters['BATCHES'])
    n_epochs = int(parameters['EPOCHS'])
    n_layers = int(parameters['LAYERS_DOWN'])
    n_tot = 2*n_layers+1
    n_init = np.int(parameters['N_INIT'])
    #filter_type = parameters['INPUT_FILTER']
    #filter_fraction = np.float(parameters['FILTER_FRACTION'])
    sharpness = float(parameters['SHARPNESS'])
    contrast = float(parameters['CONTRAST'])
    drop = float(parameters['DROPOUT'])
    n_batch_new = np.int(parameters['BATCHES_NEW'])
    n_epochs_new = np.int(parameters['EPOCHS_NEW'])
    n_layers_new = np.int(parameters['LAYERS_DOWN_NEW'])
    n_init_new = np.int(parameters['N_INIT_NEW'])
    #-- directory setup
    #- current directory
    current_dir = os.path.dirname(os.path.realpath(__file__))
    ddir = os.path.join(current_dir,'%s.dir'%glacier)
    data_dir = os.path.join(ddir, 'data')
    trn_dir = os.path.join(data_dir,'train')
    tst_dir = os.path.join(data_dir,'test')

    #-- set up labels from parameters
    drop_str = ''
    if drop>0:
        drop_str = '_w%.1fdrop'%drop

    '''
    if filter_type in ['None','none','NONE','N','n']:
        filter_str = ''
        fraction_str = ''
    else:
        filter_str = '_%s'%filter_type
        fraction_str = '_%.3f'%filter_fraction
    '''
    if sharpness in ['None','none','NONE','N','n']:
        sharpness_str = ''
    else:
        sharpness_str = '_sharpness%.1f'%sharpness
    if contrast in ['None','none','NONE','N','n']:
        contrast_str = ''
    else:
        contrast_str = '_contrast%.1f'%contrast

    #-- subdircetory
    subdir = 'output_%ibtch_%iepochs_%ilayers_%iinit%s%s%s'\
        %(n_batch,n_epochs,n_tot,n_init,drop_str,sharpness_str,contrast_str)

    data = load_data(trn_dir,tst_dir,subdir)
    n,height,width,channels=data['trn_img'].shape
    print('width=%i'%width)
    print('height=%i'%height)

    #-- import mod
    unet = imp.load_source('unet_model', os.path.join(current_dir,'frontlearn_unet_dynamic.py'))
    model,n_tot_new = unet.unet_model(height=height,width=width,channels=channels,\
        n_init=n_init_new,n_layers=n_layers_new,drop=drop)

    #-- checkpoint file
    chk_file = os.path.join(ddir,'frontlearn_weights_%ibtch_%iepochs_%ilayers_%iinit%s%s%s_iterative_%ibtch_%iepochs_%ilayers_%iinit.h5'\
        %(n_batch,n_epochs,n_tot,n_init,drop_str,sharpness_str,contrast_str,n_batch_new,n_epochs_new,n_tot_new,n_init_new))

    #-- if file exists, just read model from file
    if os.path.isfile(chk_file):
        print('Check point exists; loading model from file.')
        # load weights
        model.load_weights(chk_file)
        # Compile model (required to make predictions)
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    #-- if not train model
    else:
        print('Did not find check points. Training model...')
        #-- create checkpoint
        model_checkpoint = keras.callbacks.ModelCheckpoint(chk_file, monitor='loss',\
            verbose=1, save_best_only=True)
        #-- now fit the model
        model.fit(data['trn_img'], data['trn_lbl'], batch_size=n_batch_new, epochs=n_epochs_new, verbose=1,\
            validation_split=0.2, shuffle=True, callbacks=[model_checkpoint])

    print('Model is trained. Running on test data...')

    #-- make dictionaries for looping through train and test sets
    in_img = {}
    in_img['train'] = data['trn_img']
    in_img['test'] = data['tst_img']
    outdir = {}
    outdir['train'] = trn_dir
    outdir['test'] = tst_dir
    names = {}
    names['train'] = data['trn_names']
    names['test'] = data['tst_names']
    #-- Now test the model on both the test data and the train data
    for t in ['train','test']:
        out_imgs = model.predict(in_img[t], batch_size=1, verbose=1)
        print out_imgs.shape
        #-- save the test image
        for i in range(len(out_imgs)):
            im = image.array_to_img(out_imgs[i])
            im.save(os.path.join(outdir[t],subdir,'%s_iterative_%ibtch_%iepochs_%ilayers_%iinit.png'\
                %(names[t][i],n_batch_new,n_epochs_new,n_tot_new,n_init_new)))

#-- main function to get parameters and pass them along to fitting function
def main():
    if (len(sys.argv) == 1):
        sys.exit('You need to input at least one parameter file to set run configurations.')
    else:
        #-- Input Parameter Files (sys.argv[0] is the python code)
        input_files = sys.argv[1:]
        #-- for each input parameter file
        for file in input_files:
            #-- keep track of progress
            print(os.path.basename(file))
            #-- variable with parameter definitions
            parameters = {}
            #-- Opening parameter file and assigning file ID number (fid)
            fid = open(file, 'r')
            #-- for each line in the file will extract the parameter (name and value)
            for fileline in fid:
                #-- Splitting the input line between parameter name and value
                part = fileline.split()
                #-- filling the parameter definition variable
                parameters[part[0]] = part[1]
            #-- close the parameter file
            fid.close()

            #-- pass parameters to training function
            train_model(parameters)

if __name__ == '__main__':
    main()
