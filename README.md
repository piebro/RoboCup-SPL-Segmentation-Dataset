# RoboCup SPL Instance Segmentation Dataset

The RoboCup SPL Instance Segmentation Dataset is described and stored at [Kaggle](https://www.kaggle.com/pietbroemmel/naodevils-segmentation-upper-camera). 

## Usage

An Example NN training with the dataset on sematic segmentation can be found [here](example.ipynb). The dataset can also be used for instance segmentation to make a destinction between the robots.

## Data Preparation

At [data_preparation.ipynb](data_preparation.ipynb) is a Notebook with the steps needed to create this dataset from raw labeled  images.

## Prediction To COCO

At [data_preparation.ipynb](data_preparation.ipynb) are helper functiones to create your own automatic annotations and add them to the dataset.
