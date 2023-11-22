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
            # Check each interest area and consider special logic for area 3
            in_ioa_1, position_1 = self.is_gaze_in_ioa(row['norm_x'], row['norm_y'], row.get('interest_area_1'))
            in_ioa_2, position_2 = self.is_gaze_in_ioa(row['norm_x'], row['norm_y'], row.get('interest_area_2'))
            in_ioa_3, position_3 = self.is_gaze_in_ioa(row['norm_x'], row['norm_y'], row.get('interest_area_3'), is_area_3=True)

            # Update the DataFrame with the results
            aligned_df.at[idx, 'gaze_in_IOA_1'] = in_ioa_1
            aligned_df.at[idx, 'gaze_in_IOA_2'] = in_ioa_2
            aligned_df.at[idx, 'gaze_in_IOA_3'] = in_ioa_3
            aligned_df.at[idx, 'position_1'] = position_1
            aligned_df.at[idx, 'position_2'] = position_2
            aligned_df.at[idx, 'position_3'] = position_3

        # Now you can save the aligned DataFrame to a new CSV
        aligned_df.to_csv(self.output_path + 'aligned_data.csv', index=False)

        # Filter the DataFrame to only keep rows within the 2 to 5 seconds interval of each loop
        filtered_df = aligned_df[(aligned_df['elapsed_time'] % 6 >= 2) & 
                                    (aligned_df['elapsed_time'] % 6 < 5)]
        
        filtered_df.to_csv(self.output_path + 'aligned_filtered_data.csv', index=False)

    def is_gaze_in_ioa(self, norm_x, norm_y, area_str, is_area_3=False):
        area = self.parse_area(area_str)
        if area:
            _, x, y, w, h = area
            if x <= norm_x <= x + w and y <= norm_y <= y + h:
                if is_area_3:
                    # For area 3, check if gaze is in the left or right 50% of the area
                    aoi_position = 'left' if norm_x < x + (w / 2) else 'right'
                else:
                    # For other areas, consider position relative to screen center
                    aoi_position = 'left' if (x + w / 2) < 0.5 else 'right'
                return True, aoi_position
        return False, None

    
    def parse_area(self, area_str):
        try:
            return ast.literal_eval(area_str)
        except ValueError:
            return None