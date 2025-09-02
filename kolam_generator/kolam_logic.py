from PIL import Image, ImageDraw
import io
import base64
import numpy as np

def create_kolam_b64(rows=5, cols=5):
    """Generates our PRE-DEFINED Kolam for manual generation."""
    # This function is now only for the manual generator
    image, draw, dot_coords = _setup_canvas_and_dots(rows, cols)
    
    # Draw a pre-defined pattern
    line_color = 'red'
    if rows > 1 and cols > 1:
        all_paths = []
        mid = (rows -1) // 2
        path1 = [(0,mid)]
        for i in range(1, rows):
            if i <= mid: path1.append((i, mid+i))
            else: path1.append((i, mid + (rows-1-i)))
        all_paths.append(path1)
        path2 = [(rows-1,mid)]
        for i in range(1, rows):
            if i <= mid: path2.append((rows-1-i, mid-i))
            else: path2.append((rows-1-i, mid - (rows-1-i)))
        all_paths.append(path2)
        
        for p in all_paths:
            pixel_path = [dot_coords[r][c] for r, c in p]
            draw.line(pixel_path, fill=line_color, width=4, joint='curve')
            
    return _image_to_b64(image)

def recreate_kolam_from_analysis(original_dot_coords, traced_paths, estimated_rows, estimated_cols):
    """
    Recreates a Kolam on a fresh canvas by transforming the traced paths from the
    original image's coordinate space to the new canvas's coordinate space.
    """
    # 1. Setup a clean canvas and a new, perfectly aligned dot grid
    image, draw, new_dot_grid = _setup_canvas_and_dots(estimated_rows, estimated_cols)
    
    if not original_dot_coords or not traced_paths:
        return _image_to_b64(image)

    # 2. Define source (original image) and destination (new canvas) bounding boxes
    original_coords = np.array(original_dot_coords)
    src_min_x, src_min_y = np.min(original_coords, axis=0)
    src_max_x, src_max_y = np.max(original_coords, axis=0)
    src_width = src_max_x - src_min_x
    src_height = src_max_y - src_min_y
    
    # Handle cases to avoid division by zero
    if src_width == 0: src_width = 1
    if src_height == 0: src_height = 1
    
    new_grid_flat = [item for sublist in new_dot_grid for item in sublist]
    dest_coords = np.array(new_grid_flat)
    dest_min_x, dest_min_y = np.min(dest_coords, axis=0)
    dest_max_x, dest_max_y = np.max(dest_coords, axis=0)
    dest_width = dest_max_x - dest_min_x
    dest_height = dest_max_y - dest_min_y

    # 3. Transform and draw each traced path onto the new canvas
    for path in traced_paths:
        transformed_path = []
        for (x, y) in path:
            # Normalize original coordinates to a 0-1 scale
            norm_x = (x - src_min_x) / src_width
            norm_y = (y - src_min_y) / src_height
            
            # Apply the normalized coordinates to the destination bounding box
            new_x = dest_min_x + (norm_x * dest_width)
            new_y = dest_min_y + (norm_y * dest_height)
            
            transformed_path.append((new_x, new_y))
        
        if len(transformed_path) > 1:
            draw.line(transformed_path, fill='blue', width=4, joint='curve')

    return _image_to_b64(image)

# --- Helper Functions ---

def _setup_canvas_and_dots(rows, cols, image_size=(500, 500), dot_color='black'):
    image = Image.new('RGB', image_size, 'white')
    draw = ImageDraw.Draw(image)
    padding = 50
    dot_radius = max(2, min(8, int(250 / (rows * 2))))
    
    cell_width = (image_size[0] - 2 * padding) / (cols - 1) if cols > 1 else 0
    cell_height = (image_size[1] - 2 * padding) / (rows - 1) if rows > 1 else 0
    
    dot_grid = []
    for r in range(rows):
        row_coords = []
        for c in range(cols):
            x = padding + c * cell_width
            y = padding + r * cell_height
            row_coords.append((x, y))
            draw.ellipse((x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius), fill=dot_color)
        dot_grid.append(row_coords)
        
    return image, draw, dot_grid

def _image_to_b64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

