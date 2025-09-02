Kolam Design and Recreation Project
This project is being developed for the Smart India Hackathon 2025. The goal is to create a web application that can identify the design principles of traditional Kolam art and recreate them programmatically.

Tech Stack
Backend: Python with Django

Core Logic: Python with Pillow

Analysis: Python with OpenCV, NumPy, and opencv-contrib-python for advanced vision tasks.

Frontend: HTML with Tailwind CSS

Project Phases
Phase 1-3: Foundation & Interactivity (Complete)
Core web app is set up, allowing users to generate simple, pre-defined Kolams.

Phase 4: Basic Analysis (Complete)
Implemented dot detection to estimate the grid size from an uploaded image.

Phase 5: Advanced Design Replication (Complete)
Dependencies Added: opencv-contrib-python.

Line Skeletonization: The analysis pipeline now uses a thinning algorithm to extract the 1-pixel-wide skeleton of the Kolam's lines.

Path Tracing: A new algorithm traces the skeleton to identify individual line segments.

Exact Recreation: A new drawing function uses the detected dots and traced paths to recreate a clean, digital version of the uploaded Kolam design.

How to Run the Full Application
Set up Virtual Environment and Activate it.

Install all dependencies:

pip install Django Pillow opencv-python numpy opencv-contrib-python

Navigate to the project root.

Run migrations: python manage.py migrate

Start the server: python manage.py runserver

Open your browser to http://127.0.0.1:8000/.
