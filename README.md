# YOLOv3 - Tilapia

## Features
- Graphical interface for ease of access
- YOLOv3 for gill identification
- GrabCut algorithm for gill segmentation
- RGB channels for feature extraction

## Prerequisites
- Python version used: `python 3.8.8` or higher

## Installation
- `git clone https://github.com/Evrouin/yolov3-tilapia.git`
- Download the [data](https://drive.google.com/drive/folders/10jHceX5oWSkUvNIrLch0MGXo0zh2iUJp?usp=sharing) folder that includes:
  - yolov3_tilapia.weights
  - yolov3_tilapia.cfg
  - obj.names
- Extract the `data.zip` to root folder
- The folder structure should be similar to this:
```
    ├── venv
    ├── data
    │   ├── yolov3_tilapia.weights
    │   ├── yolov3_tilapia.cfg
    │   ├── obj.names
    ├── images
    │   ├── ...
    ├── outputs
    │   ├── ...
    └── thesis-tool.py
```

## Deployment
- Running the virtual environment
  - Type and enter `.\venv\Scripts\activate` in the terminal
- To run the system, enter `python thesis-tool.py`

## Authors
- [@John Elway Cortez](https://github.com/Evrouin)
- [@Dustin Uriel Obispo]()
- [@King Red Sanchez](https://github.com/haringpula)
- [@Briel Aldous Viola]()