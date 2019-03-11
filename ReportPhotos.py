# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 09:52:15 2019

@author: adam.rees
"""

"""
This script has been created to help with report writing,
It will take a directory full of photos from a phone, crop the photo to an
aspect ratio of 1:1, and re-size the photo to 5cm x 5cm (approx. 190x190 pixel)
"""

from PIL import Image
import sys
import os
import winshell
import logging
import time
import glob
import tkinter
import concurrent.futures
from tkinter import messagebox
from tqdm import tqdm

start = time.time()

def AdjustImage(file):
    """Compare the height and width of the image and crop the largest to the
    smallest size"""
    logging.debug("Beginning 'AdjustImage' function\n")
    SaveLocation = os.path.join(SubFolderLocation,file)
    logging.debug(f"Save Location: {SaveLocation}\n")
    try:
        image_obj = Image.open(file)
    except Exception as e:
        logging.critical("\nException in AdjustImage while opening image,\n"
                         f"Error: {e}.\n"
                         f"Tried to open: {file}\n")
    ImageSize = image_obj.size
    Largest = max(ImageSize)
    Smallest = min(ImageSize)
    Difference = Largest-Smallest

#   w is the difference to be applied to the width
#   h is the difference to be applied to the height     
    if Difference == 0:
        w = 0
        h = 0  
    if ImageSize[0] > ImageSize[1]:
        w = Difference/2
        h = 0   
    if ImageSize[0] < ImageSize[1]:
        h = Difference/2
        w = 0    
   
    NewArea = (w, h, ImageSize[0]-w, ImageSize[1]-h)
    CroppedImage = image_obj.crop(NewArea)
    logging.debug("\n-------------------------------\n"
                  "Aspect Crop Debug Report\n"
                  f"Filename: {file}, Save Location: {SaveLocation}\n"
                  f"Width: {ImageSize[0]}, Height: {ImageSize[1]}\n"
                  f"Smallest Value: {Smallest}\n"
                  f"Difference: {Difference}\n"
                  f"h: {h}, w: {w}\nNew Area: {NewArea}\n")
    
    """Now that we have 'squared off' the image and resaved it, we shall
    resize it to 5x5cm ready for report inclusion"""
    
#    CroppedImage is the new 'squared off' image
    
    NewImage = CroppedImage.resize([190,190],Image.ANTIALIAS)
    
    NewImage.save(SaveLocation)    

#Set-up for logging, includes time information and log file location
LogFolder = os.path.join(winshell.my_documents(),"HelperScripts\logs")
LogLocation = os.path.join(LogFolder,"ReportPhotos.log")

try:
    now = time.strftime("%c")
    os.makedirs(LogFolder,exist_ok=True)
    logging.basicConfig(filename=LogLocation,level=logging.INFO)
    
    logging.info('\nDate and Time:\n' + now + 
                 '\n-------------------------------\n')
except Exception as e:
    logging.critical("\n-------------------------------\n"
                     "Error with the set-up of the logging function"
                     f"Error: {e}"
                     "\n-------------------------------\n"
                     "Sys.exit(1), try/except block line 22"
                     "\n-------------------------------\n")
    sys.exit(1)

#Get parameters and variables for the shortcut name etc from the right click
#menu in windows sys.argv[1:], means fetch everything but
#the first item in the list which would be item 0...

ClickedOnFolderList = sys.argv[1:]

#DEBUG level logging
logging.debug("\n-------------------------------\n"
              f"sys.argv:\n{sys.argv}\n\n"
              "ClickedOnFolder Variable Value (List Form):\n"
              f"{ClickedOnFolderList}"
              "\n-------------------------------\n")

#Sort out the string, add the various bits of the folder name together with
#a space between them.

try:
    ClickedOnFolder = " ".join(ClickedOnFolderList)
    SubFolderLocation = os.path.join(ClickedOnFolder,"Report Images")
    
    #DEBUG level logging
    logging.debug("\n-------------------------------\n"
                  "Successful string manipulation\n\n"
                  "ClickedOnFolder Variable Value (Concatenated):"
                  f"\n{ClickedOnFolder}\n\n"
                  "ClickedOnFolder Variable Type:"
                  f"\n{type(ClickedOnFolder)}\n\n"
                  "SubFolderLocation Variable Value:"
                  f"\n{SubFolderLocation}"
                  "\n-------------------------------\n")

except Exception as e:
    logging.critical("\n-------------------------------\n"
                     "Problem with string manipulation\n\n"
                     "ClickedOnFolder Variable Value (Concatenated):"
                     f"\n{ClickedOnFolder}\n\n"
                     "SubFolderLocation Variable Value:"
                     f"\n{SubFolderLocation}\n"
                     f"Error Message: {e}"
                     "\n-------------------------------\n")
    sys.exit(2)

#Now create the subfolder that we will put the new images into
try:
    os.makedirs(SubFolderLocation,exist_ok=True)
    logging.debug("\n-------------------------------\n"
                  "Subfolder Created Successfully")
except Exception as e:
    logging.critical("os.getcwd()"
                     "Error creating subfolder for new images\n"
                     f"Error:\n{e}\n"
                     "Sys.exit(3), error with try/except loop line (83)\n\n"
                     "-------------------------------\n")
    sys.exit(3)

#Now we generate a list of all the images within the folder, creating an error
#and stopping if there aren't any images.  We're going to use glob for this
logging.debug("Line 139 - Looking for images\n")
os.chdir(ClickedOnFolder)
ImageList = []
logging.debug(f"Changed Directory to {os.getcwd()},\n"
              f"ClickedOnFolder: {ClickedOnFolder},\n"
              f"ImageList (Should be empty at this point): {ImageList}\n")

logging.debug("Starting glob\n")

for jpg in glob.glob("*.jpg"):
    ImageList.append(jpg)

for png in glob.glob("*.png"):
    ImageList.append(png)

for tiff in glob.glob("*.tiff"):
    ImageList.append(tiff)
    
NumberOfItems = len(ImageList)

logging.debug(f"ImageList (Should be full at this point):\n{ImageList}\n"
              f"Number of items in list: {NumberOfItems}\n")

if NumberOfItems == 0:
    root = tkinter.Tk()
    root.withdraw()
    messagebox.showinfo("Warning","No images found in folder")
    logging.critical("No images found, exiting (Sys.Exit(4))")
    sys.exit(4)

logging.debug("Calling 'AdjustImage' Function\n")

#Progress Bar
with concurrent.futures.ThreadPoolExecutor() as executor:
#    for image in tqdm(iterable=ImageList,unit="Photo"):
    executor.map(AdjustImage,ImageList)
        

end = time.time()    
logging.info(f"Completed, I adjusted {NumberOfItems} Images.  It took"
             f" {round(end-start,2)} seconds.\n"
             f"{round(round(end-start, 2)/NumberOfItems, 2)}"
             " seconds per photo.")

print(f"Done! It took {round(end-start,2)} seconds to process "
      f"{NumberOfItems} photographs. Quitting...")

time.sleep(3)
    
logging.info("\n\nEnd of Log Entry\n"
             "------------------------------\n")