from django.db import models
import os
from django.utils import timezone


class ProcessedFile(models.Model):
    FILE_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )
    
    original_file = models.FileField(upload_to='uploads/')
    processed_file = models.FileField(upload_to='processed/', null=True, blank=True)
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return os.path.basename(self.original_file.name)


class ROI(models.Model):
    processed_file = models.ForeignKey(ProcessedFile, on_delete=models.CASCADE, related_name='rois')
    roi_image = models.ImageField(upload_to='rois/')
    x1 = models.IntegerField()
    y1 = models.IntegerField()
    x2 = models.IntegerField()
    y2 = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"ROI for {self.processed_file} at ({self.x1},{self.y1})-({self.x2},{self.y2})"


class VideoSegment(models.Model):
    processed_file = models.ForeignKey(ProcessedFile, on_delete=models.CASCADE, related_name='segments')
    segment_file = models.FileField(upload_to='segments/')
    start_time = models.FloatField()  # in seconds
    end_time = models.FloatField()    # in seconds
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Segment for {self.processed_file} from {self.start_time}s to {self.end_time}s"
