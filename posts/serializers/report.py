from rest_framework.serializers import ModelSerializer
from posts.models import Report


class ReportSerializer(ModelSerializer):

    class Meta:
        model = Report
        fields = ('description',)
        read_only_fields = ('post', )

    def create(self, validated_data):
        return Report.objects.create(**validated_data)
