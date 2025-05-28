# Fish Freshness Evaluator (YOLOv3 Tilapia Fish Freshness Evaluation System)

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

- `git clone https://github.com/haringpula/YOLOv3-Tilapia-Fish-Freshness-Evaluation-System`
- Download the [data](https://drive.google.com/drive/folders/13HtjeKef48g6G3THhFDoh-xxKX5PUzbo?usp=drive_link) folder that includes:
  - yolov3_tilapia.weights
  - yolov3_tilapia.cfg
  - obj.names
  - A copy of the Dataset used in the study
- Extract the `data.zip` to root folder

## Deployment

To deploy this project run `tilapia-fish-freshness-evaluation-system.py` from the root folder, or through the terminal with

```bash
  python tilapia-fish-freshness-evaluation-system.py
```

## Documentation

The thesis paper can be found [here](Thesis-Manuscript.pdf) titled *Tilapia Fish Freshness Evaluation by Gill Color Using YOLOv3 and GrabCut Algorithm for Image Segmentation and Utilization of RGB Channels for Feature Extraction*.

## Contributing

Contributions are welcome! Feel free to open a pull request or something.

Please adhere to this project's [code of conduct](CODE_OF_CONDUCT.md).

## Authors

- [@John Elway Cortez](https://github.com/Evrouin)
- [@Dustin Uriel Obispo](https://github.com/haringpula/YOLOv3-Tilapia-Fish-Freshness-Evaluation-System)
- [@King Red Sanchez](https://github.com/haringpula)
- [@Briel Aldous Viola](https://github.com/haringpula/YOLOv3-Tilapia-Fish-Freshness-Evaluation-System)

## Citation

If you use this software or study as a reference, please cite it as [follows](CITATION.cff).

## License

The project is distributed under the MIT License. See [License](LICENSE.txt) for more details.
