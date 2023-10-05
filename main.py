# main.py
from data_reshape import DataProcessor
from video_processor import extract_frames

if __name__ == '__main__':
    # You can still read configuration from config.yaml if needed

    with open('config/config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    input_path = config['input_path']
    output_path = config['output_path']
    filename_exp = config['filename_exp']
    filename_gaze = config['filename_gaze']
    filename_position = config['filename_position']
    time_interval = config['time_interval']
    filename_video = config['filename_video']
    timestamp = config['timestamp']

    # Process data
    processor = DataProcessor(input_path, output_path)
    processor.process_data(filename_exp, filename_gaze, filename_position, time_interval)

    # Extract frames
    extract_frames(input_path, output_path, filename_video, timestamp)

    # Detect Stimulus

    # Integrate data for outputs
