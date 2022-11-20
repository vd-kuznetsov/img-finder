## About 

The project was based on developments from participation in one school where the emphasis was more on research.

The product goal is possibility to help users to quickly finding the right images. 

![](https://github.com/vd-kuznetsov/img-finder/blob/main/assets/app_gif.gif)

## System operation

* Image search;  
* Search by text query (Russian/English);

## Correct file structure

    .
    ├── ...
    ├── assets
    ├── indexes                    
    │   ├── trip          
    │   ├── trailer         
    │   └── traffic                
    └── main.py

## Usage 

This project was tested on python 3.8 and requires docker and docker-compose installed.
1. Clone this repository.
2. Download indexers.zip: https://drive.google.com/file/d/1FW5BvI0q_4QsrMeUjkNzbs-yy6Mv5XID/view?usp=sharing
3. Unzip to the project folder.
4. Go to the next paragraph in this README.md.

## Docker Build

For running in Docker run these commands:

* `docker-compose build`
* `docker-compose up`

The address at which the application will be available will be displayed in the terminal under the name Network URL

Usually it is http://172.18.0.3:8501/ or http://172.18.0.2:8501/
