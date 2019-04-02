from markdown import serializers

from shop.models import Category


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')