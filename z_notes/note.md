
# Resources
### Model-based
1. http://rail.eecs.berkeley.edu/deeprlcourse-fa17/f17docs/lecture_9_model_based_rl.pdf
2. 
### model-free
1. http://cs231n.stanford.edu/reports/2017/pdfs/604.pdf

# Finished
1. __model__
    - model-free method
    - hard to learn transition probability
2. __state__
    - feature vector
3. __policy__
    - encoder + lstm = $\pi(a,s_t,s_{t-1},s_{t-2},s_{t-3})$ 
4. __dataset structure__
    - Video
        - Center
            - Index_center_time
        - Left
            - Index_left_time
        - Right
            - Index_right_time
    - Command
        - Index
            - {frame,steering,speed,category}
5. __Precedure__ 
    1. ./camera.sh
    2. go outside and record
    3. ./archieve
    4. repeat 1-3 several time
    5. copy all to dataset/temp && python3 file_arranger.py
  



# Architecture

basic policy + refine 

# Training

1. define command from left and right
1. propregate the error to n sec time


# Next
## Idea

## To do
1. LSTM imitaiton learning paper --  architecture

2. berkely social + hongkong city -- people model

3. berkely rc car -- how to train in real time


# Dagger process
1. run by itself
2. if adjust back change 40 commands
3. train with dagger data
4. measure time without intervention



https://arxiv.org/pdf/1710.02543.pdf








find . -name .DS_Store -print0 | xargs -0 git rm -f --ignore-unmatch
find . -name .idea -print0 | xargs -0 git rm -rf --ignore-unmatch
find . -name __pycache__ -print0 | xargs -0 git rm -rf --ignore-unmatch

You can do it in Pycharm -> Preferences -> Project: XYZ -> Project Structure

Select your working folder and mark it as Sources. Then Pycharm recognize the working folder as a Source folder for the project and you will be able to simply add other files within that folder by using