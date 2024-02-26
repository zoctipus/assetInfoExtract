import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pathlib import Path
import numpy as np

OBJECT_ID = 10450
# Base directory where the images are located
base_path = Path(f'mobility/{OBJECT_ID}/parts_photograph')

# Image file names that we are interested in
image_files = ['right.png', 'left.png', 'top.png', 'bottom.png', 'back.png', 'front.png']

# Orientation configurations with explicit tick labels for correct direction
orientation_configs = {
    'right': {'x_legend': 'x', 'y_legend': 'z', 'x_labels': np.linspace(-1, 1, 9), 'y_labels': np.linspace(-1, 1, 9)},
    'left': {'x_legend': 'x', 'y_legend': 'z', 'x_labels': np.linspace(1, -1, 9), 'y_labels': np.linspace(-1, 1, 9)},
    'top': {'x_legend': 'y', 'y_legend': 'x', 'x_labels': np.linspace(1, -1, 9), 'y_labels': np.linspace(-1, 1, 9)},
    'bottom': {'x_legend': 'y', 'y_legend': 'x', 'x_labels': np.linspace(1, -1, 9), 'y_labels': np.linspace(1, -1, 9)},
    'front': {'x_legend': 'y', 'y_legend': 'z', 'x_labels': np.linspace(1, -1, 9), 'y_labels': np.linspace(-1, 1, 9)},
    'back': {'x_legend': 'y', 'y_legend': 'z', 'x_labels': np.linspace(-1, 1, 9), 'y_labels': np.linspace(-1, 1, 9)}
}

# Iterate over all subdirectories in the base_path
for parts_dir in base_path.glob('*'):
    # Check if all specified image_files exist in the current subdirectory
    if all((parts_dir / img_name).exists() for img_name in image_files):
        # Initialize a 2x3 grid for plotting with labels on the axes
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes_flat = axes.flatten()

        # Loop through the images and their respective axes
        for ax, img_name in zip(axes_flat, image_files):
            orientation = img_name.split('.')[0]  # Determine the orientation
            config = orientation_configs[orientation]

            img_path = parts_dir / img_name
            img = mpimg.imread(img_path)  # Load the image

            # Display the image
            ax.imshow(img, aspect='equal', extent=[-1, 1, -1, 1])
            ax.set_title(orientation.capitalize())

            # Set legends
            ax.set_xlabel(config['x_legend'])
            ax.set_ylabel(config['y_legend'])

            # Set x and y ticks based on orientation config
            ax.set_xticks(np.linspace(-1, 1, 9))
            ax.set_yticks(np.linspace(-1, 1, 9))

            # Explicitly set x and y tick labels to ensure correct order
            ax.set_xticklabels([f"{x:.1f}" for x in config['x_labels']])
            ax.set_yticklabels([f"{y:.1f}" for y in config['y_labels']])

            # Enable the grid, set the style to white dashed lines
            ax.grid(which='both', color='grey', linestyle='--', linewidth=0.5)

        # Adjust the layout to prevent overlapping and save the plot in the current subdirectory
        plt.tight_layout()
        plot_save_path = parts_dir / 'plot_image.png'
        plt.savefig(plot_save_path)
        plt.close()  # Close the plot to free memory
