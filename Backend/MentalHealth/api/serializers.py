from rest_framework import serializers
from .models import Assessment, Article, ArticleLike, ArticleRating, ArticleView

from rest_framework import serializers
from .models import Assessment, UserScore

class AssessmentSerializer(serializers.ModelSerializer):
    captured_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Assessment
        fields = ['id', 'user', 'mood', 'sleep_quality', 'expression_analysis', 'captured_image', 'captured_image_url', 'created_at']
        read_only_fields = ['id', 'created_at', 'captured_image_url']
    
    def get_captured_image_url(self, obj):
        if obj.captured_image:
            return obj.captured_image.url
        return None


class UserScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserScore
        fields = '__all__'


from .models import CustomUser   # ya jo tumhara user model hai

class UserMiniSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["id", "full_name", "profile_image"]

    def get_profile_image(self, obj):
        request = self.context.get("request")
        if obj.profile_image:
            return request.build_absolute_uri(obj.profile_image.url)
        return None




from rest_framework import serializers
from .models import AudioAnalysis

class AudioAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioAnalysis
        fields = ['id', 'user', 'audio_file', 'timestamp', 'status', 'analysis_result']
        read_only_fields = ['user', 'timestamp', 'status', 'analysis_result']



class ArticleSerializer(serializers.ModelSerializer):
    author = UserMiniSerializer(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    total_likes = serializers.IntegerField(read_only=True)
    total_views = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "content",
            "category",
            "author",
            "image",
            "created_at",
            "average_rating",
            "total_likes",
            "total_views",
            "is_liked",  # Add this field
        ]

    def get_is_liked(self, obj):
        # Get the current user from request context
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ArticleLike.objects.filter(
                article=obj, 
                user=request.user
            ).exists()
        return False







from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    video_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'video_url']

    def get_video_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.video.url)
