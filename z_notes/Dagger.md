# Verfify
- Time_iter_{date_time}.csv
- 1. move Time_iter_{date_time}.csv to summer_research/z_note
# Dagger
## Files:
- Dagger_iter_{date_time}.avi
- Dagger_iter_command_{date_time}.csv
## Data processing
1. ffmpeg -y -i {Dagger_iter.avi} -qscale:v 2 dagger/0/video/iter_%06d.jpg
2. data/dagger_decay.py --{Dagger_command.csv}
    1. will move to dagger/0/command/{date_time}.csv
3. train

# merge one class
1. mergecsv
2. python3 DaggerArranger.py
3. cp dagger/0/video/*.jpg dataset/video/0  
4. train
