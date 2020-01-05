# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 18:53:24 2017

@author: Saeed Mohaqeqi
"""
import glob
import os
import numpy as np
import SimpleITK as sitk
import gc
import psutil

def window_intensities(image, _min=0, _max=255):
    out_image = sitk.IntensityWindowing(image, _min, _max)
    return out_image

def rescale(image, minimum=0, maximum=1):
    out_image = sitk.RescaleIntensity(image, minimum, maximum)
    return out_image

def maskImage(image, mask):
    mask = rescale(mask)
    mask = sitk.Cast(mask, image.GetPixelIDValue())
    mask.SetDirection(image.GetDirection())
    out_image = image * mask
    return out_image

def smooth_image(image):
#    out_image = sitk.CurvatureFlow(image1=image, timeStep=0.125, numberOfIterations=2)
#    out_image = sitk.DiscreteGaussian(image)
    out_image = sitk.SmoothingRecursiveGaussian(image, 0.5)
    return out_image


def read_image(in_file):
    image = sitk.ReadImage(in_file)
    return image

def write_image(image_data, image_path):
    # 3DirCab, MICCAI2007, Srr: Just GetArray/GetImage?
    # Osaka: fliplr + Direction
    _image = sitk.GetArrayFromImage(image_data)
#    _image = _image[::-1]
#    _image = np.fliplr(_image)
#    _image = np.flipud(_image)
    _image = sitk.GetImageFromArray(_image)
#    _image.SetSpacing(image_data.GetSpacing())
#    direction = (-1.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, -1.0)
#    _image.SetDirection(direction)
#    _image.SetDirection(image_data.GetDirection())
    sitk.WriteImage(_image, image_path)

def get_image(subject_folder, name):
    files = glob.glob(os.path.join(subject_folder, name))
    if len(files)>0:
        return files[0]
    else:
        return None

def resample_image(image, spacing=None):
    original_spacing = image.GetSpacing()
    original_size = image.GetSize()
    if spacing:
        min_spacing = spacing
    else:
        min_spacing = min(original_spacing)

    new_spacing = [min_spacing, min_spacing, min_spacing]
    new_size = [int(round(original_size[0]*(original_spacing[0]/min_spacing))),
                int(round(original_size[1]*(original_spacing[1]/min_spacing))),
                int(round(original_size[2]*(original_spacing[2]/min_spacing)))]
    resampled_img = sitk.Resample(image, new_size, sitk.Transform(),
                                  sitk.sitkLinear, image.GetOrigin(),
                                  new_spacing, image.GetDirection(), 0.0,
                                  image.GetPixelID())
    return resampled_img


def ROI_from_mask(data_image, data_liver):
    _liverArray = sitk.GetArrayFromImage(data_liver)
    x,y,z = np.nonzero(_liverArray)
    pad=10
    minX = max(1, min(x)-pad)
    minY = max(1, min(y)-pad)
    minZ = max(1, min(z)-pad)
    maxX = min(_liverArray.shape[0], max(x)+pad)
    maxY = min(_liverArray.shape[1], max(y)+pad)
    maxZ = min(_liverArray.shape[2], max(z)+pad)
    ROI_liver = _liverArray[minX:maxX, minY:maxY, minZ:maxZ]
    _liver = sitk.GetImageFromArray(ROI_liver)
    
    if data_image == None:
        _liver.SetSpacing(data_liver.GetSpacing())
        _image = None
    else:
        _imageArray = sitk.GetArrayFromImage(data_image)
        ROI_image = _imageArray[minX:maxX, minY:maxY, minZ:maxZ]
        _image = sitk.GetImageFromArray(ROI_image)
#        _image.SetSpacing(data_image.GetSpacing())
#        _image.SetDirection(data_image.GetDirection())
#        _liver.SetSpacing(data_image.GetSpacing())

    
    _liver.SetDirection(data_liver.GetDirection())
    
    
#    del _imageArray, ROI_image, _liverArray, ROI_liver
    return _image, _liver

def resize_image(image, newSize, scale=None, spacing=None):
    inSpacing = np.round(image.GetSpacing(), 3)
    if not spacing:
        outSpacing = np.round(inSpacing * image.GetSize() / newSize, 3)
    else:
        outSpacing = spacing

    filterResamp = sitk.ResampleImageFilter()
    filterResamp.SetSize(newSize)
    filterResamp.SetDefaultPixelValue(0)
    filterResamp.SetOutputDirection(image.GetDirection())
    filterResamp.SetOutputSpacing(outSpacing)
    filterResamp.SetOutputOrigin(image.GetOrigin())
    filterResamp.SetOutputPixelType(sitk.sitkInt16)
    filterResamp.SetInterpolator(sitk.sitkNearestNeighbor)
    out_image = filterResamp.Execute(image)

    return out_image

def zeropad_image(image, size):
    img = sitk.GetArrayFromImage(image)
    imgSize = img.shape
    img = np.pad(img, ((0,size[2]-imgSize[0]),(0,size[0]-imgSize[1]),(0,size[1]-imgSize[2])), 'constant', constant_values=0)
    out_image = sitk.GetImageFromArray(img)
    return out_image
    
    
def preprocess_dataset(Dataset_folder, out_folder):
    proc = psutil.Process(os.getpid())
    idx = 1
    for subject_folder in glob.glob(os.path.join(Dataset_folder, "*")):
        if os.path.isdir(subject_folder):
            subject = os.path.basename(subject_folder)

            resize = True
            
#            # Osaka
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
            
#            # Srr
#            image_file = get_image(subject_folder, "*_ART.nii.gz")
##            image_file = get_image(subject_folder, "*_NC.nii.gz")
##            image_file = get_image(subject_folder, "*_PV.nii.gz")
#            if image_file == None:
#                data_image = None
#            else:
#                data_image = read_image(image_file)
#            liver_file = get_image(subject_folder, "*_LiverMask.nii.gz")
#            data_liver = read_image(liver_file)
#            data_mask = None
            
            
            # Test
            image_file = get_image(subject_folder, "*-orig*.nii.gz")
            data_image = read_image(image_file)
            data_liver = None
            data_mask = None
            resize = True
            
            print("...Folder " + subject + " loaded")

            if data_mask == None:
                _image = data_image
            else:
                _image = maskImage(data_image, data_mask)
            
            if data_liver == None:
                _liver = None
            else:
                _liver = rescale(data_liver)

            del data_image, data_liver, data_mask
            
            newSize = [128,128,128]
            if not _liver == None:
                _image, _liver = ROI_from_mask(_image, _liver)
                _liver = resample_image(_liver)
                _liver = resize_image(_liver, newSize)
            
            if not _image == None:
                _image = smooth_image(_image)
                _image = window_intensities(_image)
                if resize == True:
#                    _image = zeropad_image(_image, newSize)
                    _image = resample_image(_image)
                    _image = resize_image(_image, newSize)
                if not _liver == None:
                    _liver_image = maskImage(_image, _liver)


            new_subject_folder = os.path.join(out_folder, subject)
            if not os.path.exists(new_subject_folder):
                os.makedirs(new_subject_folder)

            if not _liver == None:
#                mask_path = os.path.join(new_subject_folder, os.path.basename(liver_file))
                mask_path = os.path.join(new_subject_folder, 'img-liver_({}).nii.gz'.format(idx))
                write_image(_liver, mask_path)
                
                
            if not _image == None:
#                data_path = os.path.join(new_subject_folder, os.path.basename(image_file))
                data_path = os.path.join(new_subject_folder, 'img-patient_({}).nii.gz'.format(idx))
                write_image(_image, data_path)
                if not _liver == None:
#                    liver_image_filename = os.path.basename(liver_file)[:-7] + '_image' + os.path.basename(liver_file)[-7:]
                    liver_image_filename ='img-liverImage_({}).nii.gz'.format(idx)
                    liver_image_file = os.path.join(new_subject_folder, liver_image_filename)
                    write_image(_liver_image, liver_image_file)
                    del _liver, _liver_image
                del _image

            
            gc.collect()
            print("...Folder " + new_subject_folder + " saved")
            print("memory: " + str(proc.memory_info().rss))
            
            idx = idx+1

if __name__ == "__main__":
#    Dataset_folder = "Dataset_Osaka_Raw"
#    Dataset_folder = "Dataset_MICCAI2007_Raw"
#    Dataset_folder = "Dataset_3DirCab_Raw"
#    Dataset_folder = "Dataset_SRR_ART_Raw"
#    Dataset_folder = "Dataset_SRR_NC_Raw"
#    Dataset_folder = "Dataset_SRR_PV_Raw"
    Dataset_folder = "Dataset_Test_Raw"
    out_folder = Dataset_folder[:-3] + "Preprocessed"
    preprocess_dataset(Dataset_folder, out_folder)