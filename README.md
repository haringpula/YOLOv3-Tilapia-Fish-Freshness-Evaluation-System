# YOLOv3 - Tilapia

## Features
- Graphical interface for ease of access
- YOLOv3 for gill identification
- GrabCut algorithm for gill segmentation
- RGB channels for feature extraction

## Prerequisites
- Python version used: `python 3.8.8`
- Recommended python package versions:
  - `opencv-python` - version 4.5.3.56
  - `numpy` - version 1.21.4
  - `Pillow` - version 8.4.0

## Installation
- `git clone https://github.com/Evrouin/yolov3-tilapia.git`
- Download the [data](https://drive.google.com/drive/folders/10jHceX5oWSkUvNIrLch0MGXo0zh2iUJp?usp=sharing) folder that includes:
  - yolov3_tilapia.weights
  - yolov3_tilapia.cfg
  - obj.names
- Extract the `data.zip` to root folder

## Deployment
To deploy this project run `tilapia-fish-freshness-evaluation-system.py` from the root folder, or through the terminal with
```bash
  python tilapia-fish-freshness-evaluation-system.py
```

## Authors
- [@John Elway Cortez](https://github.com/Evrouin)
- [@Dustin Uriel Obispo]()
- [@King Red Sanchez](https://github.com/haringpula)
- [@Briel Aldous Viola]()