from rest_framework import serializers
from .models import Partner

class PartnerSerializer(serializers.ModelSerializer):
	name = serializers.SerializerMethodField()
	description = serializers.SerializerMethodField()

	class Meta:
		model = Partner
		fields = ['logo', 'name', 'description', 'coord1', 'coord2']

	def get_name(self, obj):
		return obj.get_name(language=self.context.get('language', 'ru'))

	def get_description(self, obj):
		return obj.get_description(language=self.context.get('language', 'ru'))
