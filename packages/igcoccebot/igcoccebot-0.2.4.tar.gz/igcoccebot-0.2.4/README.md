# Welcome!

This is a package to navigate and grab data from Instagram easily.
It is built on Selenium and it uses Chrome driver.


# Step 1
Install the last stable release of Chromedriver here (v76) for you OS (macOS, Win or Linux): https://chromedriver.chromium.org/

# Step 2 (optional)
If you want to use YOLOv3 embedded for object detection you must download coco.data, coco.names, libdarknet.so, yolov3.cfg and yolov3.weights and place them in the working dir

# Step 3
pip (or pip3) install igcoccebot on the terminal

# Step 4
Use it in your scripts -> 'import igcoccebot as ig'

# Step 5
Initialize an IGCocceBot with path to chrome driver: remember that 'chromedriver' doesn't work you must type './chromedriver' if you want to use the current dir

Example:

import igcoccebot as ig

bot = ig.IGCocceBot('./chromedriver')

Lorenzo Coacci