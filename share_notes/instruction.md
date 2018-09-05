## recording (TX2)
 ```
./camera.sh
```

## zip data (TX2)
```
./archieve
```
## prepare dataset (G7) 

1. select data and compress as either one of these:
```
├── data.zip
│   ├── [folder 1]
│   ├── [folder 2]
│   └── ...

```
```
├── category.zip
│   ├── data1.zip
│   │   ├── [folder 1]
│   │   ├── [folder 2]
│   │   └── ...
│   ├── data1.zip
│   │   ├── [folder 1]
│   │   ├── [folder 2]
│   │   └── ...
│   └── ...
```


1. move from download to /g7_workspace/dataset/raw_data/temp/classnum
   
2. python3 Arranger.py

## train process
```
$ python train.py --muiltGPU 0 1  --classnum 0 --batch_size 128
```
```
$ python train.py --single 0  --classnum 0 --batch_size 128
```
## prepare dagger data (G7)
```
ffmpeg -y -i 0.avi -qscale:v 2 dagger/0/video/center_%06d.jpg
```


# TESTS
## model test
```
cd /summer-research/g7_workspace/test
python infer_test.py --model 0_225_50.pth.tar
```
## camera test
## control test


# lib

conda install pytorch torchvision -c pytorch
conda install ffmpeg -c conda-forge
conda install pandas
