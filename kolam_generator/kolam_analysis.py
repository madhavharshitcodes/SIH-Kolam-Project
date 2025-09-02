import cv2
import numpy as np
from PIL import Image
import io
import math
import base64

def _trace_path(skeleton, start_point, visited):
    """A helper function to trace a single path from a starting point."""
    path = [start_point]
    visited[start_point[1], start_point[0]] = 255
    
    # Directions to check for neighboring pixels (8-connectivity)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    current_point = start_point
    while True:
        found_next = False
        for dx, dy in directions:
            next_x, next_y = current_point[0] + dx, current_point[1] + dy
            
            # Check bounds
            if 0 <= next_y < skeleton.shape[0] and 0 <= next_x < skeleton.shape[1]:
                if skeleton[next_y, next_x] == 255 and visited[next_y, next_x] == 0:
                    current_point = (next_x, next_y)
                    path.append(current_point)
                    visited[current_point[1], current_point[0]] = 255
                    found_next = True
                    break # Move to the next point in the path
        
        if not found_next:
            break # End of path
            
    return path

def _find_paths_from_skeleton(skeleton):
    """
    Traces all the distinct line paths from a skeleton image.
    NOTE: This is a simplified path tracing algorithm for demonstration. It works best
    on non-looping lines. A full solution would require more complex graph traversal
    to handle junctions and closed loops perfectly.
    """
    paths = []
    # Create a mask to keep track of visited pixels
    visited = np.zeros(skeleton.shape, dtype=np.uint8)
    
    # Find all white pixels (potential path points)
    white_pixels = np.argwhere(skeleton == 255)
    
    for pixel in white_pixels:
        # The pixel coordinates are returned as (row, col) which is (y, x)
        y, x = pixel
        if visited[y, x] == 0:
            # If we haven't visited this pixel, it's the start of a new path
            new_path = _trace_path(skeleton, (x, y), visited)
            if len(new_path) > 10: # Only consider paths of a certain length
                paths.append(new_path)
                
    return paths

def _estimate_grid_from_dots(dot_coords, tolerance_factor=0.5):
    """
    A more robust method to estimate grid size by clustering dot coordinates.
    """
    if len(dot_coords) < 2:
        return 1 if dot_coords else 0

    coords = np.array(dot_coords)
    
    # Estimate a reasonable clustering tolerance based on median dot spacing
    sorted_x = np.sort(coords[:, 0])
    sorted_y = np.sort(coords[:, 1])
    diff_x = np.diff(sorted_x)
    diff_y = np.diff(sorted_y)
    
    # Use non-zero differences to avoid issues with dots on the same line
    median_gap_x = np.median(diff_x[diff_x > 0]) if len(diff_x[diff_x > 0]) > 0 else 10
    median_gap_y = np.median(diff_y[diff_y > 0]) if len(diff_y[diff_y > 0]) > 0 else 10
    
    tolerance_x = median_gap_x * tolerance_factor
    tolerance_y = median_gap_y * tolerance_factor
    
    # Cluster X coordinates to find columns
    clusters_x = []
    if len(sorted_x) > 0:
        current_cluster = [sorted_x[0]]
        for x in sorted_x[1:]:
            if x - current_cluster[-1] < tolerance_x:
                current_cluster.append(x)
            else:
                clusters_x.append(current_cluster)
                current_cluster = [x]
        clusters_x.append(current_cluster)
    num_cols = len(clusters_x)
    
    # Cluster Y coordinates to find rows
    clusters_y = []
    if len(sorted_y) > 0:
        current_cluster = [sorted_y[0]]
        for y in sorted_y[1:]:
            if y - current_cluster[-1] < tolerance_y:
                current_cluster.append(y)
            else:
                clusters_y.append(current_cluster)
                current_cluster = [y]
        clusters_y.append(current_cluster)
    num_rows = len(clusters_y)
    
    grid_size = max(num_rows, num_cols)
    
    # Our simple generator only handles odd grids
    if grid_size % 2 == 0 and grid_size > 0:
        grid_size += 1
    if grid_size == 0 and len(dot_coords) > 0:
        grid_size = 1
    if grid_size < 3 and grid_size > 0:
        grid_size = 3

    return grid_size

def analyze_kolam_image(image_file_bytes):
    """
    Analyzes an uploaded Kolam image to detect dots, find the line skeleton, trace the paths,
    and estimate the grid size.
    """
    pil_image = Image.open(io.BytesIO(image_file_bytes)).convert('RGB')
    open_cv_image = np.array(pil_image)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    
    # === 1. DOT DETECTION (Tuned Parameters) ===
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 1) # Reduced blur for sharper dots
    circles = cv2.HoughCircles(
        blurred, 
        cv2.HOUGH_GRADIENT, 
        dp=1, 
        minDist=15, # Lowered to detect closer dots
        param1=50, 
        param2=12, # Lowered threshold to detect more potential circles
        minRadius=2, 
        maxRadius=15 # Lowered max radius
    )
    
    dot_coords = []
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            dot_coords.append((x, y))
            cv2.circle(open_cv_image, (x, y), r, (0, 255, 0), 4)

    # === 2. LINE SKELETONIZATION ===
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    skeleton = cv2.ximgproc.thinning(thresh)

    # === 3. PATH TRACING ===
    traced_paths = _find_paths_from_skeleton(skeleton)

    # For visualization, draw the traced paths onto the original image
    for path in traced_paths:
        for i in range(len(path) - 1):
            cv2.line(open_cv_image, path[i], path[i+1], (255, 0, 0), 2) # Draw blue lines

    # === 4. GRID ESTIMATION (Upgraded Logic) ===
    grid_size = _estimate_grid_from_dots(dot_coords)

    # === 5. RETURN RESULTS ===
    _, buffer = cv2.imencode('.png', open_cv_image)
    processed_image_b64 = base64.b64encode(buffer).decode('utf-8')

    return grid_size, dot_coords, traced_paths, processed_image_b64

