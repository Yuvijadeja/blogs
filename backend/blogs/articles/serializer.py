from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Article
        fields = "__all__"

    def validate_banner_image(self, value):
        if value.size > 5 * 1024 * 1024:  # 5 MB
            raise serializers.ValidationError("Image file too large ( > 5MB )")
        if not value.name.lower().endswith((".jpg", ".jpeg", ".png")):
            raise serializers.ValidationError("Only JPG and PNG images are allowed.")
        return value
