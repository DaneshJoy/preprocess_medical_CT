# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 11:44:35 2019

@author: Mohagheghi
"""

import glob
import os
import numpy as np
import SimpleITK as sitk

def read_image(in_file):
    image = sitk.ReadImage(in_file)
    return image

def get_image(subject_folder, name):
    files = glob.glob(os.path.join(subject_folder, name))
    if len(files)>0:
        return files[0]
    else:
        return None
    
def getDatasetInfo(Dataset_folder):
    slices_total = 0
    spacing_minx = 1000
    spacing_maxx = 0
    spacing_minz = 1000
    spacing_maxz = 0
    min_z = 1000
    max_z = 0
    num = 0
    for subject_folder in glob.glob(os.path.join(Dataset_folder, "*")):
        if os.path.isdir(subject_folder):
            subject = os.path.basename(subject_folder)
            
             # Osaka
#            image_file = get_image(subject_folder, "OsakaID*.nii.gz")
#            data_image = read_image(image_file)
#            liver_file = get_image(subject_folder, "MaskOsakaID*.nii.gz")
#            data_liver = read_image(liver_file)
#            data_mask = None

#            # MICCAI2007
#            image_file = get_image(subject_folder, "*-orig*.nii.gz")
#            data_image = read_image(image_file)
#            liver_file = get_image(subject_folder, "*-seg*.nii.gz")
#            data_liver = read_image(liver_file)
#            data_mask = None
           
#            # 3DirCab
#            image_file = get_image(subject_folder, "*-patient*.nii.gz")
#            data_image = read_image(image_file)
#            liver_file = get_image(subject_folder, "*-liver*.nii.gz")
#            data_liver = read_image(liver_file)
#            mask_file = get_image(subject_folder, "*-skin*.nii.gz")
#            data_mask = read_image(mask_file)
            
            # Srr
#            image_file = get_image(subject_folder, "*_ART.nii.gz")
#            image_file = get_image(subject_folder, "*_NC.nii.gz")
            image_file = get_image(subject_folder, "*_PV.nii.gz")
            if not image_file == None:
                data_image = read_image(image_file)
                size = data_image.GetSize()
                slices_total += size[2]
                if size[2] > max_z:
                    max_z = size[2]
                if size[2] < min_z:
                    min_z = size[2]
                spacing = data_image.GetSpacing()
                if spacing[0] > spacing_maxx:
                    spacing_maxx = spacing[0]
                if spacing[0] < spacing_minx:
                    spacing_minx = spacing[0]
                if spacing[2] > spacing_maxz:
                    spacing_maxz = spacing[2]
                if spacing[2] < spacing_minz:
                    spacing_minz = spacing[2]
                num += 1
                    
            
            
#            # Test
#            image_file = get_image(subject_folder, "*-orig*.nii.gz")
#            data_image = read_image(image_file)
#            data_liver = None
#            data_mask = None
#            resize = True
    print('num of images:', num)
    print('total slices:', slices_total)
    print('min_z:', min_z)
    print('max_z:', max_z)
    print('min spacing xy:', spacing_minx)
    print('max spacing xy:', spacing_maxx)
    print('min spacing z:', spacing_minz)
    print('max spacing z:', spacing_maxz)
                
            
            
if __name__ == "__main__":
#    Dataset_folder = "Osaka_Raw"
#    Dataset_folder = "MICCAI2007_Raw"
#    Dataset_folder = "3DirCab_Raw"
#    Dataset_folder = "SRR_ART_Raw"
#    Dataset_folder = "SRR_NC_Raw"
    Dataset_folder = "SRR_PV_Raw"
#    Dataset_folder = "Dataset_Test_Raw"
    getDatasetInfo(Dataset_folder)