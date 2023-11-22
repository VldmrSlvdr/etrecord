# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   @File Name:     data_processor.py
   @Author:        Yifei LI
   @Date:          2023/11/01
   @Description:
-------------------------------------------------
"""
import pandas as pd

class DataProcessor:
    def __init__(self, config):
        """
        Initialize the DataProcessor with file paths and filenames from the given configuration.
        """
        self.input_path = config['input_path']
        self.output_path = config['output_path']
        self.filename_exp = config['filename_exp']
        self.filename_gaze = config['filename_gaze']
        self.filename_position = config['filename_position']

    def process_data(self):
        """
        Process experimental and gaze data and merge them based on timestamps.
        """
        try:
            data_exp = pd.read_csv(self.input_path + self.filename_exp)
            data_gaze = pd.read_csv(self.input_path + self.filename_gaze)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return
        
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

        try:
            merged_df.to_csv(self.output_path + self.filename_position)
        except Exception as e:
            print(f"Error while saving the file: {e}")

    def select_columns(self):
        """
        Select and return specified columns from the input DataFrame.
        """
        data_exp = pd.read_csv(self.input_path + self.filename_exp)
        data_exp_exposure = data_exp[2:22]
        condition = data_exp['condition'][3]

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
        return data_exp_exposure[columns]

    def extract_rating_data(self):
        """
        Extract and reformat the rating data from the input DataFrame.
        """
        # Create an empty list to store the rows
        data_exp = pd.read_csv(self.input_path + self.filename_exp)
        session = data_exp['session'][3]
        if session == 1:
            pass
        else:
            data_exp_rating = data_exp[23:64]
            output = []

            # Iterate through the rows of the input DataFrame
            for index, row in data_exp_rating.iterrows():
                # Extract fixed columns
                participant = row['participant']
                # session = row['session']
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

    def load_gaze_data(self):
        """
        Load and preprocess gaze data from the CSV file.
        """
        try:
            gaze_data = pd.read_csv(self.input_path + self.filename_gaze)
            # Add preprocessing steps here...
            return gaze_data
        except Exception as e:
            print(f"Error loading gaze data: {e}")
            return None

    def load_exp_data(self):
        """
        Load and preprocess experimental data from the CSV file.
        """
        try:
            exp_data = pd.read_csv(self.input_path + self.filename_exp)
            # Add preprocessing steps here...
            return exp_data
        except Exception as e:
            print(f"Error loading experimental data: {e}")
            return None