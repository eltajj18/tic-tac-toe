# Tic-tac-toe board state detection with OpenCV and Keras

### A fully functional project of processing the input image of tic-tac-toe game and outputting the array representing the locations of "X" "O" and "Blank" and sending the output through HTTP_POST to the server. 
## Flow Chart
![Flow_Chart](https://github.com/eltajj18/tic-tac-toe/assets/100543589/fb7e8018-7b36-4df3-9d66-00b81a4f8474)

## Capabilities
### 0.Once you input the image file:

![received_image2_20240410_205202](https://github.com/eltajj18/tic-tac-toe/assets/100543589/56155f52-b70b-4071-b431-1c895b832901)

### 1.The program first creates grayscale version of that:

![paper_gray](https://github.com/eltajj18/tic-tac-toe/assets/100543589/0f07ee32-4672-4b8f-b808-330403a5db9f)

### 2.From that it applies blur and edge detection:

![paper_edged](https://github.com/eltajj18/tic-tac-toe/assets/100543589/d881f4ea-8dfc-446e-80e9-b1d67264de79)

### 3.Then by using edge detected image, outline of the paper is achieved:
 
![paper_outline](https://github.com/eltajj18/tic-tac-toe/assets/100543589/a5d505ee-db8e-4b66-b5d8-d7d9c1098232)

### 4.Then by applying four point transform, we obtain a top-down bird's-eye view of the paper:
 
![paper_final](https://github.com/eltajj18/tic-tac-toe/assets/100543589/c85e0542-4517-4f49-b420-4103ed58837b)

### 5.After getting top-down bird's-eye view of the paper, we again grayscale it and find the threshold of the paper:

![thresh_paper](https://github.com/eltajj18/tic-tac-toe/assets/100543589/30e93210-0bde-426b-816a-09314071e675)

### 6.Then finally the program puts a grid over the "top-down bird's-eye view of the paper":

![griddy_paper](https://github.com/eltajj18/tic-tac-toe/assets/100543589/0915b7b9-c1ad-4a02-946a-af35619f9965)


## Limitations

1) Wait 5-10 sec after starting the program due to tensorflow
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
