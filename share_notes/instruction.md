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

# lib

conda install pytorch torchvision -c pytorch
conda install ffmpeg -c conda-forge
conda install pandas
