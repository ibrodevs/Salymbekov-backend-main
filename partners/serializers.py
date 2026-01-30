from rest_framework import serializers
from .models import Partner

class PartnerSerializer(serializers.ModelSerializer):
	name = serializers.SerializerMethodField()
	description = serializers.SerializerMethodField()

	class Meta:
		model = Partner
		fields = ['logo', 'name', 'description' 'coord1', 'coord2']

	def get_name(self, obj):
		obj.get_name(lang=self.context.get('lang', 'ru'))

	def get_description(self, obj):
		obj.get_description(lang=self.context.get('lang', 'ru'))
