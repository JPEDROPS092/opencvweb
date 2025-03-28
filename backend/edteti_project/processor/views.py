from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import ProcessedFile, ROI, VideoSegment
from .serializers import ProcessedFileSerializer, ROISerializer, VideoSegmentSerializer
import cv2
import numpy as np
from PIL import Image
import os
from django.conf import settings
import tempfile
from django.core.files import File
import json

@api_view(['GET'])
def api_root(request, format=None):
    """API root endpoint com links para os principais endpoints"""
    return Response({
        'upload': reverse('upload_file', request=request, format=format),
        'files': reverse('file_list', request=request, format=format),
    })

# Variáveis para controle do YOLO
yolo_available = False
YOLO_MODEL_PATH = None

# Função para carregar o modelo YOLO quando necessário
def load_yolo_model():
    global yolo_available, YOLO_MODEL_PATH
    
    if yolo_available:
        # Se já verificamos que o YOLO está disponível, retorne True
        return True
        
    try:
        # Importa o YOLO apenas quando necessário
        from ultralytics import YOLO
        import os.path
        
        # Verificar se existe um modelo personalizado
        model_path = os.path.join(settings.BASE_DIR, 'models', 'modelo_personalizado.pt')
        default_model_path = "yolov8n.pt"  # Modelo padrão caso não exista um personalizado
        
        if os.path.exists(model_path):
            YOLO_MODEL_PATH = model_path
        else:
            YOLO_MODEL_PATH = default_model_path
            
        # Testa se consegue criar uma instância do modelo
        # Isso vai falhar se houver problemas com o PyTorch
        try:
            _ = YOLO(YOLO_MODEL_PATH)
            yolo_available = True
            return True
        except Exception as e:
            print(f"Erro ao carregar o modelo YOLO: {e}")
            yolo_available = False
            return False
            
    except ImportError as e:
        print(f"Erro ao importar YOLO: {e}")
        yolo_available = False
        return False

@api_view(['POST'])
def upload_file(request):
    file_obj = request.FILES.get('file')
    file_type = request.data.get('file_type')
    
    if not file_obj or not file_type:
        return Response({'error': 'File and file type are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    processed_file = ProcessedFile(
        original_file=file_obj,
        file_type=file_type
    )
    processed_file.save()
    
    serializer = ProcessedFileSerializer(processed_file, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def file_list(request):
    files = ProcessedFile.objects.all().order_by('-created_at')
    serializer = ProcessedFileSerializer(files, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET', 'DELETE'])
def file_detail(request, pk):
    processed_file = get_object_or_404(ProcessedFile, pk=pk)
    
    if request.method == 'DELETE':
        processed_file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    serializer = ProcessedFileSerializer(processed_file, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
def apply_filter(request, pk, filter_type):
    processed_file = get_object_or_404(ProcessedFile, pk=pk)
    
    # Read the image or video
    file_path = processed_file.original_file.path
    
    if processed_file.file_type == 'image':
        # Process image
        img = cv2.imread(file_path)
        
        if filter_type == 'blur':
            result = cv2.GaussianBlur(img, (5, 5), 0)
        elif filter_type == 'sharpen':
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            result = cv2.filter2D(img, -1, kernel)
        elif filter_type == 'emboss':
            kernel = np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]])
            result = cv2.filter2D(img, -1, kernel)
        elif filter_type == 'laplacian':
            result = cv2.Laplacian(img, cv2.CV_64F).astype(np.uint8)
        elif filter_type == 'canny':
            result = cv2.Canny(img, 100, 200)
            result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
        elif filter_type == 'sobel':
            grad_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
            grad_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
            abs_grad_x = cv2.convertScaleAbs(grad_x)
            abs_grad_y = cv2.convertScaleAbs(grad_y)
            result = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
        elif filter_type == 'grayscale':
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            result = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        elif filter_type == 'binary':
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, result = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
        elif filter_type == 'detect_objects':
            if load_yolo_model():
                # Importa o YOLO apenas quando necessário
                from ultralytics import YOLO
                model = YOLO(YOLO_MODEL_PATH)
                results = model(img, conf=0.5)
                result = results[0].plot()
            else:
                return Response({'error': 'YOLOv8 não está disponível ou ocorreu um erro ao carregar o modelo'}, 
                              status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': f'Filter type {filter_type} not supported'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Save the processed image
        output_path = os.path.join(settings.MEDIA_ROOT, 'processed', f'processed_{processed_file.id}.jpg')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, result)
        
        with open(output_path, 'rb') as f:
            processed_file.processed_file.save(f'processed_{processed_file.id}.jpg', File(f), save=True)
        
    elif processed_file.file_type == 'video':
        # For video processing, we'll need more complex logic
        cap = cv2.VideoCapture(file_path)
        
        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        # Create output video writer
        output_path = os.path.join(settings.MEDIA_ROOT, 'processed', f'processed_{processed_file.id}.mp4')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Apply filter to each frame
            if filter_type == 'blur':
                frame = cv2.GaussianBlur(frame, (5, 5), 0)
            elif filter_type == 'sharpen':
                kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
                frame = cv2.filter2D(frame, -1, kernel)
            elif filter_type == 'emboss':
                kernel = np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]])
                frame = cv2.filter2D(frame, -1, kernel)
            elif filter_type == 'laplacian':
                frame = cv2.Laplacian(frame, cv2.CV_64F).astype(np.uint8)
            elif filter_type == 'canny':
                frame = cv2.Canny(frame, 100, 200)
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            elif filter_type == 'sobel':
                grad_x = cv2.Sobel(frame, cv2.CV_64F, 1, 0, ksize=3)
                grad_y = cv2.Sobel(frame, cv2.CV_64F, 0, 1, ksize=3)
                abs_grad_x = cv2.convertScaleAbs(grad_x)
                abs_grad_y = cv2.convertScaleAbs(grad_y)
                frame = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
            elif filter_type == 'grayscale':
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            elif filter_type == 'binary':
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                _, frame = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            elif filter_type == 'detect_objects':
                if load_yolo_model():
                    # Importa o YOLO apenas quando necessário
                    from ultralytics import YOLO
                    model = YOLO(YOLO_MODEL_PATH)
                    results = model(frame, conf=0.5)
                    frame = results[0].plot()
                else:
                    return Response({'error': 'YOLOv8 não está disponível ou ocorreu um erro ao carregar o modelo'}, 
                                  status=status.HTTP_400_BAD_REQUEST)
                
            out.write(frame)
            
        cap.release()
        out.release()
        
        with open(output_path, 'rb') as f:
            processed_file.processed_file.save(f'processed_{processed_file.id}.mp4', File(f), save=True)
    
    serializer = ProcessedFileSerializer(processed_file, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
def extract_roi(request, pk):
    processed_file = get_object_or_404(ProcessedFile, pk=pk)
    
    # Get ROI coordinates from request
    try:
        data = request.data
        x1 = int(data.get('x1'))
        y1 = int(data.get('y1'))
        x2 = int(data.get('x2'))
        y2 = int(data.get('y2'))
    except (TypeError, ValueError):
        return Response({'error': 'Invalid ROI coordinates'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Read the image
    if processed_file.file_type != 'image':
        return Response({'error': 'ROI extraction only supported for images'}, 
                      status=status.HTTP_400_BAD_REQUEST)
    
    img = cv2.imread(processed_file.original_file.path)
    
    # Extract ROI
    roi_img = img[min(y1,y2):max(y1,y2), min(x1,x2):max(x1,x2)]
    
    # Save ROI
    output_path = os.path.join(settings.MEDIA_ROOT, 'rois', f'roi_{processed_file.id}_{len(processed_file.rois.all())}.jpg')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, roi_img)
    
    # Create ROI object
    roi = ROI(
        processed_file=processed_file,
        x1=min(x1, x2),
        y1=min(y1, y2),
        x2=max(x1, x2),
        y2=max(y1, y2)
    )
    
    with open(output_path, 'rb') as f:
        roi.roi_image.save(f'roi_{processed_file.id}_{len(processed_file.rois.all())}.jpg', File(f), save=True)
    
    serializer = ROISerializer(roi)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def create_video_segment(request, pk):
    processed_file = get_object_or_404(ProcessedFile, pk=pk)
    
    # Check if it's a video
    if processed_file.file_type != 'video':
        return Response({'error': 'Video segmentation only supported for videos'}, 
                      status=status.HTTP_400_BAD_REQUEST)
    
    # Get segment times from request
    try:
        data = request.data
        start_time = float(data.get('start_time'))
        end_time = float(data.get('end_time'))
    except (TypeError, ValueError):
        return Response({'error': 'Invalid segment times'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Open the video
    cap = cv2.VideoCapture(processed_file.original_file.path)
    
    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Create output video writer
    output_path = os.path.join(settings.MEDIA_ROOT, 'segments', 
                             f'segment_{processed_file.id}_{len(processed_file.segments.all())}.mp4')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Set position to start time
    cap.set(cv2.CAP_PROP_POS_MSEC, start_time * 1000)
    
    # Read and write frames until end time
    while cap.get(cv2.CAP_PROP_POS_MSEC) < end_time * 1000:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
    
    cap.release()
    out.release()
    
    # Create segment object
    segment = VideoSegment(
        processed_file=processed_file,
        start_time=start_time,
        end_time=end_time
    )
    
    with open(output_path, 'rb') as f:
        segment.segment_file.save(
            f'segment_{processed_file.id}_{len(processed_file.segments.all())}.mp4', 
            File(f), save=True
        )
    
    serializer = VideoSegmentSerializer(segment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
