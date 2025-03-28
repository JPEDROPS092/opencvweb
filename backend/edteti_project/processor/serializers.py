from rest_framework import serializers
from .models import ProcessedFile, ROI, VideoSegment
from django.conf import settings


class ROISerializer(serializers.ModelSerializer):
    roi_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ROI
        fields = ['id', 'roi_image', 'roi_image_url', 'x1', 'y1', 'x2', 'y2', 'created_at']
    
    def get_roi_image_url(self, obj):
        if obj.roi_image and hasattr(obj.roi_image, 'url'):
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.roi_image.url)
            return obj.roi_image.url
        return None


class VideoSegmentSerializer(serializers.ModelSerializer):
    segment_file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = VideoSegment
        fields = ['id', 'segment_file', 'segment_file_url', 'start_time', 'end_time', 'created_at']
    
    def get_segment_file_url(self, obj):
        if obj.segment_file and hasattr(obj.segment_file, 'url'):
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.segment_file.url)
            return obj.segment_file.url
        return None


class ProcessedFileSerializer(serializers.ModelSerializer):
    rois = ROISerializer(many=True, read_only=True)
    segments = VideoSegmentSerializer(many=True, read_only=True)
    original_file_url = serializers.SerializerMethodField()
    processed_file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProcessedFile
        fields = ['id', 'original_file', 'original_file_url', 'processed_file', 'processed_file_url', 'file_type', 'created_at', 'rois', 'segments']
    
    def get_original_file_url(self, obj):
        if obj.original_file and hasattr(obj.original_file, 'url'):
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.original_file.url)
            return obj.original_file.url
        return None
    
    def get_processed_file_url(self, obj):
        if obj.processed_file and hasattr(obj.processed_file, 'url'):
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.processed_file.url)
            return obj.processed_file.url
        return None
