# A simple algorithm for processing eyetracking data
My motivation is to simply integrate the eyetracking data and the results of video detection algorithm for further analysis. 

## Enviornments 

You can run following code in the terminal under the target directory to run this tool.

```{shell}
# create and activate a new virtual environment first 
conda create -n etrecord
conda activate etrecord

# require the packages 
pip install -r requirements.txt

```

## Folder structure of the inputs
The input files should be structured as following:

```
inputs 
    |- 20231011
        |- 01_participant_id
            |- 000
                |- exports
                    |- 000
                        |- annotations.csv
                        |- export_info.csv
                        |- gaze_positions.csv
                        |- pupil_positions.csv
                        |- ...
                |- offline_data
                |- world.mp4
                |- ...
            |- 001
            |- experiment_file_session1.csv
            |- experiment_file_session2.csv
        |- 02_participant_id
        |- ...
    |- 20231018
    |- ...
``` 

## How to use this tool

After you compose the forlder sturcture of inputs as above then you could simply excute this tool by using: 

```
python mian.py
```

And you could also change the context in `config.yaml` to use your own data.

## Outputs 

The outputs which contain the participants' eyetracking data and critical behavioral info during the experiment should be like:

| participant_id  | session  | trial  | ...  | AOI_interval  |
|---|---|---|---|---|
| 000000  | 1  | 1  | ...  | 1214  |
| 000000  | 1  | 2  | ...  |  883 |
| ...  | ...  | ...  | ...  | ...  |