<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Kolam Design and Recreation - README</title>
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }
    h1, h2, h3 { color: #333; }
    code { background: #f4f4f4; padding: 2px 4px; border-radius: 4px; }
    pre { background: #f4f4f4; padding: 10px; border-radius: 6px; overflow-x: auto; }
  </style>
</head>
<body>
  <h1>Kolam Design and Recreation Project</h1>
  <p><strong>Smart India Hackathon 2025</strong> project to identify design principles of traditional Kolam art and recreate them programmatically.</p>

  <h2>Tech Stack</h2>
  <ul>
    <li><strong>Backend:</strong> Python with Django</li>
    <li><strong>Core Logic:</strong> Python with Pillow</li>
    <li><strong>Analysis:</strong> OpenCV, NumPy, opencv-contrib-python</li>
    <li><strong>Frontend:</strong> HTML with Tailwind CSS</li>
  </ul>

  <h2>Project Phases</h2>
  <ol>
    <li><strong>Phase 1–3: Foundation & Interactivity</strong> – Core web app set up with simple, pre-defined Kolams. ✅</li>
    <li><strong>Phase 4: Basic Analysis</strong> – Dot detection to estimate grid size from uploaded image. ✅</li>
    <li><strong>Phase 5: Advanced Design Replication</strong> – Skeletonization, path tracing, and exact recreation. ✅</li>
  </ol>

  <h2>How to Run</h2>
  <ol>
    <li>Set up and activate a virtual environment.</li>
    <li>Install dependencies:
      <pre><code>pip install Django Pillow opencv-python numpy opencv-contrib-python</code></pre>
    </li>
    <li>Navigate to the project root.</li>
    <li>Run migrations:
      <pre><code>python manage.py migrate</code></pre>
    </li>
    <li>Start the server:
      <pre><code>python manage.py runserver</code></pre>
    </li>
    <li>Open in browser: <code>http://127.0.0.1:8000/</code></li>
  </ol>

  <h2>License</h2>
  <p>This project is released under the MIT License.</p>
</body>
</html>
