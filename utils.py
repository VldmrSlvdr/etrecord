import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def etdata_visualizer():
# Load your gaze data and timestamps from your DataFrame
    merged_df = merged_df.copy()

    # Define the list of seconds you want to display
    display_second = 4  # Adjust this list as needed

    range_init = display_second * 120
    range_over = range_init + 120

    # Extract relevant columns
    timestamps = merged_df['gaze_stamp']

    x_data = merged_df['norm_x'][range_init:range_over+1]
    y_data = merged_df['norm_y'][range_init:range_over+1]

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(8, 4.5))

    # Set the background color
    ax.set_facecolor('#f0f0f0')

    # Add gridlines
    ax.grid(True, linestyle='--', alpha=0.7)

    # Set axis labels
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')

    # Set plot title
    ax.set_title('My Plot Background')

    # Set fixed X-axis and Y-axis limits (adjust as needed)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Scatter plot your gaze data
    ax.scatter(x_data, y_data, label='Eye Tracking Data', color='blue', marker='o')

    for i, (x, y) in enumerate(zip(x_data, y_data)):
        ax.text(x, y, str(i+1), ha='center', va='bottom', fontsize=10, color='black')

    # Load and overlay images based on selected seconds
    opacity = 0.6
    image_directory = output_frame_dir  # Directory containing your saved images

    frame_start = display_second * 10  # Assuming 10 frames per second
    frame_end = frame_start + 10
            
    display_frame = display_second * 10
    image_filename = os.path.join(image_directory, f'frame_{display_frame:04d}.jpg')
    if os.path.exists(image_filename):
        # Load and display the image as a background with lower opacity
        img = mpimg.imread(image_filename)
        ax.imshow(img, extent=(0, 1, 0, 1), aspect='auto', zorder=-1, alpha=opacity)

    # Show the plot
    plt.show()

