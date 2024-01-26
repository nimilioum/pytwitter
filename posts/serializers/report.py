from rest_framework.serializers import ModelSerializer

from posts.models import Report


class ReportSerializer(ModelSerializer):

    class Meta:
        model = Report
        fields = ('post',)
