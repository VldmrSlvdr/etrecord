# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   @File Name:     data_integrator.py
   @Author:        Yifei LI
   @Date:          2023/11/08
   @Description:
-------------------------------------------------
"""
import ast  # For safely evaluating strings as tuples
import pandas as pd

class DataIntegrator:
    def __init__(self, config):
        self.input_path = config['input_path']
        self.output_path = config['output_path']
        self.filename_gaze = config['filename_gaze']
        self.filename_exp = config['filename_exp']
        self.ioa_df = pd.read_csv(self.output_path + 'AOI.csv')
        self.merged_data_df = pd.read_csv(self.output_path + 'merged_data_03.csv')

    def integrate_data(self):
        # Merge the dataframes
        aligned_df = pd.merge_asof(
            self.merged_data_df.sort_values('gaze_stamp'),
            self.ioa_df.sort_values('elapsed_time'),
            left_on='gaze_stamp', right_on='elapsed_time', direction='nearest'
        )

        # Apply the function to each row in the aligned DataFrame
        for idx, row in aligned_df.iterrows():
            # Obtain frame width - replace with your actual method to get frame width
            frame_width = get_frame_width()  # Placeholder function
            
            # Check each interest area
            in_ioa_1, ioa_id_1, position_1 = self.is_gaze_in_ioa(row['norm_x'], row['norm_y'], row['interest_area_1'], frame_width)
            in_ioa_2, ioa_id_2, position_2 = self.is_gaze_in_ioa(row['norm_x'], row['norm_y'], row['interest_area_2'], frame_width)
            
            aligned_df.at[idx, 'gaze_in_IOA_1'] = in_ioa_1
            aligned_df.at[idx, 'gaze_in_IOA_2'] = in_ioa_2
            aligned_df.at[idx, 'IOA_id_1'] = ioa_id_1
            aligned_df.at[idx, 'IOA_id_2'] = ioa_id_2
            aligned_df.at[idx, 'position_1'] = position_1
            aligned_df.at[idx, 'position_2'] = position_2

        # Now you can save the aligned DataFrame to a new CSV
        aligned_df.to_csv(self.output_path + 'aligned_data.csv', index=False)

    def is_gaze_in_aoi(self, norm_x, norm_y, area_str, frame_width):
        area = self.parse_area(area_str)
        if area:
            # Adjust this line to unpack correctly according to your actual data structure
            id, x, y, w, h = area
            if x <= norm_x <= x + w and y <= norm_y <= y + h:
                aoi_position = 'left' if (x + w / 2) < (frame_width / 2) else 'right'
                return (True, id, aoi_position)
        return (False, None, None)

    
    def parse_area(self, area_str):
        try:
            return ast.literal_eval(area_str)
        except ValueError:
            return None