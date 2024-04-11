# Tic-tac-toe board state detection with OpenCV and Keras


## A fully functional project of processing the input image of tic-tac-toe game and outputting the array representing the locations of "X" "O" and "Blank" and sending the output through HTTP_POST to the server. 


## Flow Chart
<img src =""/>


## Limitations

1) Wait 5-10 sec after starting the program due to tenserflow
2) The input format of image is JPG
3) The corners of the paper should be visible in the image.
4) Standard sizes of paper work better, eg.A4,A3
5) The grid that is drawn should be ~small - medium size compared to the paper
6) "X" and "O" should be drawn small-medium size compared to the cell of the grid

## How to use

1. clone this project
2. install all the dependencies with - 'pip install -r requirements.txt' (it is recommended to install it in your virtual environment to avoid conflicts)
3. you can change the monitored image directory (currently it is /active_images_repo)
4. start the program with - 'python play_new.py'
5. drop an image in the monitored directory 

## Recourses
- All the credits for the ML model and shape detection goes to <a href = "https://github.com/tempdata73/tic-tac-toe?tab=readme-ov-file">tempdate73</a>
- To better understand the concepts, you can visit <a href="https://pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/">pyimagesearch's blogs</a>