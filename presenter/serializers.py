from rest_framework import serializers
from .models import GoLive

class GoLiveSerializer(serializers.ModelSerializer):

	class Meta:
		model = GoLive
		fields = ('current_slide',)

