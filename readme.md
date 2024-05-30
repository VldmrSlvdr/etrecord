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

Also, you could just process the video files by using:

```
python process_video.py
```

And you could also modify `config_sample.yaml` to process your own data.

## Outputs 

The outputs which contain the participants' eyetracking data and critical behavioral info during the experiment are recorded in following files:
- 00x_exp.csv
- 00x_gaze.csv 
- 00x_video_analysis.csv (do not function well)
- 00x_integ.csv
- xxxxxx_rating_data.csv
- xxxxxx_combined_exp_data.csv

The outputs of `process_video.py` are stored in following folders and 2 session files each participant:

```
outputs
    |- 999999(6 digits participant id)
        |- session_001_output.csv
        |- session_002_output.csv
    |- ...
```

And the outputs should be like

|session|frame|elapsed_time_ms|trial_num|trial_phase|gaze_position|area_info|in_area|left_or_right|
|---|---|---|---|---|---|---|---|---|
|001|0|0.0|1|fixation|"(0.783691689087273, 0.2346680635019017)"|"{'interest_area_1': (0, 0.5078125, 0.5055555555555555, 0.01484375, 0.025), 'interest_area_2': None, 'interest_area_3': None}"|False|right|
|001|1|33.500320826810935|1|fixation|"(0.783691689087273, 0.2346680635019017)"|"{'interest_area_1': (1, 0.5078125, 0.5055555555555555, 0.015625, 0.025), 'interest_area_2': None, 'interest_area_3': None}"|False|right|
|...|...|...|...|...|...|...|...|...|