# data_reshape.py
import pandas as pd
import datetime

class DataProcessor:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        input_path = './inputs/'
        filename_exp = 'data_exp_03.csv'
        filename_gaze = 'data_gaze_03.csv'
        filename_video = '20230913_02.mp4'

        output_path = './outputs/'
        filename_position = f'position_{timestamp}.csv'
        output_frame_dir = './outputs/frames/'

        data_exp = pd.read_csv(input_path + filename_exp)
        data_gaze = pd.read_csv(input_path + filename_gaze)

        exp_timestamp = data_exp['etRecord_3.started']
        exp_timestamp_clean = exp_timestamp.dropna()

        first_value = exp_timestamp_clean.iloc[0]  # Get the first value
        adjusted_value = [value - first_value for value in exp_timestamp_clean]
        new_data = pd.DataFrame({'exp_index': adjusted_value})

        gaze_timestamp = data_gaze['gaze_timestamp']
        first_value = gaze_timestamp.iloc[0]
        adjusted_value = [value - first_value for value in gaze_timestamp]
        new_data2 = pd.DataFrame({'gaze_stamp': adjusted_value})

        new_data2['norm_x'] = data_gaze['norm_pos_x']
        new_data2['norm_y'] = data_gaze['norm_pos_y']

        # Define the time interval for merging (e.g., +/- 1 second)
        time_interval = 5.999

        # Merge based on time intervals
        merged_df = pd.merge_asof(
            new_data2,
            new_data,
            left_on='gaze_stamp',
            right_on='exp_index',
            direction='backward',  # Use 'backward' if you want to find the nearest exp_index value before gaze_stamp
            tolerance=time_interval
        )

        merged_df.to_csv(output_path+filename_position) 


def extract_exposure_data(input_df):
    condition = input_df['condition'][3]

    if condition == 1:
        columns = ['participant', 'condition', 'session', 'picture1', 'picture2', 'statement1', 'statement2', 'Category', 'etRecord_3.started', 'arrow_list1']
    elif condition == 2:
        columns = ['participant', 'condition', 'session', 'picture4', 'picture1', 'statement4', 'statement1', 'Category', 'etRecord_3.started', 'arrow_list1']
    elif condition == 3:
        columns = ['participant', 'condition', 'session', 'picture3', 'picture4', 'statement3', 'statement4', 'Category', 'etRecord_3.started', 'arrow_list1']
    elif condition == 4:
        columns = ['participant', 'condition', 'session', 'picture2', 'picture3', 'statement2', 'statement3', 'Category', 'etRecord_3.started', 'arrow_list1']
    else:
        return None  # Handle invalid condition

    # Extract and return the selected columns
    return input_df[columns]

def extract_rating_data(input_df):
    # Create an empty list to store the rows
    output = []

    # Iterate through the rows of the input DataFrame
    for index, row in input_df.iterrows():
        # Extract fixed columns
        participant = row['participant']
        session = row['session']
        evaluation = row['evaluation']
        Category = row['Category']
        set_num = row['set_num']

        # Determine target_image and target_statement based on set_num
        if set_num == 1:
            target_image = row['picture1']
            target_statement = row['statement1']
        elif set_num == 2:
            target_image = row['picture2']
            target_statement = row['statement2']
        elif set_num == 3:
            target_image = row['picture3']
            target_statement = row['statement3']
        elif set_num == 4:
            target_image = row['picture4']
            target_statement = row['statement4']
        else:
            # Handle the case when set_num is not 1, 2, or 3
            target_image = None
            target_statement = None

        # Create a dictionary for the row
        row_dict = {
            'participant': participant,
            'session': session,
            'Category': Category,
            'set_num': set_num,
            'target_image': target_image,
            'target_statement': target_statement,
            'evaluation': evaluation,
        }

        # Append the row dictionary to the list
        output.append(row_dict)

    # Create a DataFrame from the list of row dictionaries
    output_target = pd.DataFrame(output)

    return output_target