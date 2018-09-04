import preprocessing
from preprocessing import DataPath
from preprocessing import split_name
import os

UNZIP_DATASET = 1
EXTRACT_DATA = 1
EXTRACT_FRAME = 1
MERGE_COMMAND = 1
SYNC_FRAMES = 1
CSV_ADDLR = 1


rawDataPath = 'raw_data'
datasetPath = 'dataset'
tempPath = os.path.join(rawDataPath, 'temp')
rawdata = DataPath(rawDataPath)
dataset = DataPath(datasetPath)

# ==========================================================================
# Unzip Dataset:
#   unzip file to clock_data folder as in the car
# ==========================================================================
if UNZIP_DATASET:
    print('==========================')
    print('Unzip dataset')
    print('==========================')
    for classnum in rawdata.category:
        print('Processing Class:' + str(classnum) + ' data...')
        temp = os.path.join(tempPath, str(classnum))
        preprocessing.unzip_dataset(temp)
    print('Finish unzip dataset')
# ==========================================================================
# Extract all data:
#  from rawdata/temp folder to rawdata/video/class & rawdata/command/class
# ==========================================================================
if EXTRACT_DATA:
    print('==========================')
    print('Extract all data')
    print('==========================')
    for classnum in rawdata.category:
        print('Processing Class:' + str(classnum) + ' data...', end='  :')
        video_arch_root = os.path.join(rawdata.video_list['root'][classnum], 'archieve')
        index_start = preprocessing.get_start_index(video_arch_root)
        print('Class:' + str(classnum) + " already has " + str(index_start - 1) + " videos")
        preprocessing.extract_data(index_start, rawDataPath, classnum)
    print('Finish extract data')
# ==========================================================================
# Extract all FRAME
#   from rawdata/video to dataset/video
# ==========================================================================
rawdata.update()
dataset.update()
if EXTRACT_FRAME:
    print('==========================')
    print('Extract all frames')
    print('==========================')
    for classnum in rawdata.category:
        print('Processing Class:' + str(classnum) + ' data...')
        if len(rawdata.video_list[classnum]) > 0:
            for index, video in enumerate(rawdata.video_list[classnum]):
                print("{:10} size(MB): {:>8.2f}".format(split_name(video), os.path.getsize(video) / 1000000))
                dest_name = os.path.join(dataset.video_list['root'][classnum], split_name(video))
                archieve_path = os.path.join(
                    rawdata.video_list['root'][classnum], 'archieve/' + split_name(video) + '.avi')
                preprocessing.extract_frames(video, dest_name)
                os.rename(video, archieve_path)
    print('Finish extract frames')
    dataset.update()
# ==========================================================================
# Merge all command
#   merge command from each video together
# ==========================================================================
if MERGE_COMMAND:
    print('==========================')
    print('Merge command')
    print('==========================')
    for classnum in rawdata.category:
        if len(rawdata.command_list[classnum]) > 0:
            print('Processing Class:' + str(classnum) + ' data...', end='  ')
            original_file_list = rawdata.command_list[classnum]
            print('merge {:2} files'.format(len(original_file_list)))
            merged_file = os.path.join(dataset.command_list['root'][classnum], 'center.csv')
            preprocessing.csv_merge(original_file_list, merged_file)
    print('Finish merge command')
    dataset.update()
# ==========================================================================
# Synchronize all the FRAMES
#   keep frame number from three cameras same
# ==========================================================================
dataset.update()
if SYNC_FRAMES:
    print('==========================')
    print('Synchronize frames')
    print('==========================')
    for classnum in dataset.category:
        print('Processing Class:' + str(classnum) + ' data...')
        frame_path = dataset.video_list['root'][classnum]
        if os.path.isdir(frame_path):
            preprocessing.sync_frame(frame_path)
    print('Finish sync frames')
# ==========================================================================
# Add left and right command to merged file
#   keep frame number from three cameras same
# ==========================================================================
if CSV_ADDLR:
    for classnum in dataset.category:
        if len(dataset.command_list[classnum]) > 0:
            print('Finsih Add Left&Right Class:' + str(classnum) + ' data...')
            original_file = os.path.join(dataset.command_list['root'][classnum], 'center.csv')
            changed_file = os.path.join(dataset.command_list['root'][classnum], 'all_three.csv')
            preprocessing.csv_addlr(original_file,changed_file, 300)
