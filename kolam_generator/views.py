from django.shortcuts import render
from .kolam_logic import create_kolam_b64, recreate_kolam_from_analysis
from .kolam_analysis import analyze_kolam_image

def index(request):
    context = {'dots': 5} 

    # Handle Manual Generation
    if request.method == 'POST' and 'generate' in request.POST:
        dots_str = request.POST.get('dots', '5')
        try:
            dots = int(dots_str)
            if dots % 2 == 0: dots += 1
            if dots < 3: dots = 3
            if dots > 15: dots = 15
        except ValueError:
            dots = 5
        
        context['dots'] = dots
        context['recreated_kolam_b64'] = create_kolam_b64(rows=dots, cols=dots)

    # Handle Image Analysis and Recreation
    elif request.method == 'POST' and 'analyze' in request.POST:
        uploaded_image = request.FILES.get('kolam_image')
        if uploaded_image:
            image_bytes = uploaded_image.read()
            
            # The analysis function now returns more data
            grid_size, dots, paths, processed_b64 = analyze_kolam_image(image_bytes)
            
            context['original_image_b64'] = processed_b64
            context['estimated_dots'] = grid_size
            
            if grid_size > 0:
                # Call the new recreation function
                context['recreated_kolam_b64'] = recreate_kolam_from_analysis(dots, paths, grid_size, grid_size)

    # Default GET request
    else:
        context['recreated_kolam_b64'] = create_kolam_b64(rows=5, cols=5)

    return render(request, 'kolam_generator/index.html', context)

