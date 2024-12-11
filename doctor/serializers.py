from rest_framework import serializers
from .models import Doctor, Designation, Specialization, AvailableTime, Review

class DoctorSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    specialization = serializers.StringRelatedField(many=True)
    designation = serializers.StringRelatedField(many=True)
    # available_time = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='availabletime-detail')
    available_time = serializers.StringRelatedField(many=True)
    class Meta:
        model = Doctor
        fields = '__all__'

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'

class AvailableTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableTime
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'