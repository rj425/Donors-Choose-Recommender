# Donors-Choose-Recommender

- **Source -** [Kaggle](https://www.kaggle.com/)
- **Dataset -** [Data Science for Good: DonorsChoose.org](https://www.kaggle.com/donorschoose/io)
- **Solution -** [Python Notebook](https://nbviewer.jupyter.org/github/rj425/Donors-Choose-Recommender/blob/master/models.ipynb)

This repository contains all the required files used to run the recommendation engine as a localhost server. Tree structure of CODE directory looks something like this:
    
    ├── data
    │   └── uscities.csv
    ├── images
    │   └── cover.png
    ├── recommender.py
    ├── requirements.txt
    └── scripts
        ├── data_ingestion.py
        ├── 
        ├──     
        ├── 

- `data_ingestion.py` : This script loads the data from csv files and exports them to the recommendation engine.
- `recommender.py` : This is the main script that runs the streamlit server on localhost and port 8501.

## Installation Instructions

0. Change the directory to CODE directory.

        cd CODE

1. Download all the dataset files in `./data` directory from [here](https://www.kaggle.com/donorschoose/io/download).

2. Install all the required python packages mentioned in requirements.txt
file using pip manager.

        pip install -r requirements.txt

3. Before running the recommendation engine, we will first have 
to create the recommendation engine using create_reco_engine.py 
script present in 'scripts' directory. This will generate two 
important files 'reco_engine.csv' and 'categories.csv' in 'data' 
directory.

        cd scripts
        python create_reco_engine.py

4. Next few commands are OPTIONAL as they only deletes the intermediary
compressed files into 'data' directory.

        cd ..
        cd data
        del compressed_reco_engine_* engine.csv  # For windows
        rm compressed_reco_engine_* engine.csv # For linux

After running the installation instructions from step 0 to 4,
'data' directory would look something like this:

    data
    ├── Donations.csv
    ├── Donors.csv
    ├── Projects.csv
    ├── Resources.csv
    ├── Schools.csv
    ├── Teachers.csv
    ├── categories.csv
    ├── reco_engine.csv
    └── uscities.csv


## Execution Instructions

Running the recommendation engine on localhost is very simple.
Just execute :

    cd ..
    streamlit run recommender.py

This will run the streamlit server (our app) on http://localhost:8501.
