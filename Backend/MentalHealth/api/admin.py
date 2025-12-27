from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Assessment, Article, ArticleLike, ArticleRating, ArticleView

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'full_name', 'phone_number', 'gender', 'age', 'weight','has_completed_profile','has_completed_assessment')
    list_filter = ('gender', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('full_name', 'email', 'profile_image', 'phone_number', 'gender', 'date_of_birth', 'weight', 'has_completed_profile', 'has_completed_assessment')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'full_name', 'password1', 'password2', 'phone_number', 'gender', 'date_of_birth', 'weight')}
        ),
    )
    search_fields = ('username', 'email', 'full_name')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)




@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "mood",
        "sleep_quality",
        "captured_image",
        "created_at",
    )
    list_filter = ("mood", "sleep_quality",  "created_at")
    search_fields = ("user__username", "user__email", "mood")
    ordering = ("-created_at",)



from django.contrib import admin
from .models import AudioAnalysis

@admin.register(AudioAnalysis)
class AudioAnalysisAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'get_user_email', 
        'status', 
        'emotion', 
        'confidence', 
        'timestamp', 
        'processed_at'
    )
    list_filter = ('status', 'emotion', 'timestamp')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('timestamp', 'processed_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'audio_file', 'timestamp', 'processed_at', 'duration')
        }),
        ('Analysis Results', {
            'fields': ('status', 'emotion', 'confidence', 'analysis_result')
        }),
    )

    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'User Email'
    get_user_email.admin_order_field = 'user__email'







    # Media related models can be added here if needed


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "created_at", "average_rating", "total_likes", "total_views")
    list_filter = ("category", "created_at")
    search_fields = ("title", "content", "author__username")
    ordering = ("-created_at",)


@admin.register(ArticleLike)
class ArticleLikeAdmin(admin.ModelAdmin):
    list_display = ("article", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("article__title", "user__username")


@admin.register(ArticleRating)
class ArticleRatingAdmin(admin.ModelAdmin):
    list_display = ("article", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("article__title", "user__username")


@admin.register(ArticleView)
class ArticleViewAdmin(admin.ModelAdmin):
    list_display = ("article", "user", "viewed_at")
    list_filter = ("viewed_at",)
    search_fields = ("article__title", "user__username")




from django.contrib import admin
from .models import UserScore


@admin.register(UserScore)
class UserScoreAdmin(admin.ModelAdmin):

    # Columns shown in list view
    list_display = (
        'id', 'user', 'total_score', 'created_at'
    )

    # Search
    search_fields = (
        'user__username',
        'user__email',
        'mood_label',
    )

    # Filters in right sidebar
    list_filter = (
        'mood_label',
        'created_at'
    )

    # Read-only fields
    readonly_fields = (
        'created_at',
        'total_score',
    )

    # Form layout (fields arranged in groups)
    fieldsets = (
        ("User Information", {
            "fields": ("user",)
        }),

        ("Basic Information Scores (10 points)", {
            "fields": ("sleep_score",)
        }),

        ("Mood (10 points)", {
            "fields": ("mood_score", "mood_label")
        }),

        ("Text Emotion (25 points)", {
            "fields": (
                
                "text_sentiment_score",
                "text_emotion_score",
                "text_negative_keywords_score"
            )
        }),

        ("Image Emotion (25 points)", {
            "fields": (
                "image_expression_score",
                "image_fatigue_score",
                "image_darkcircles_score",
                "image_stressmicro_score"
            )
        }),

        ("Voice Emotion (30 points)", {
            "fields": (
                "voice_tone_score",
                "voice_pitch_score",
                "voice_speed_score",
                "voice_hesitation_score",
                "voice_stress_score"
            )
        }),

        ("Final Results", {
            "fields": ("total_score",)
        }),

        ("Timestamps", {
            "fields": ("created_at",)
        }),
    )

    # Ordering
    ordering = ('-created_at', '-total_score')
    
    # Date hierarchy for easy navigation
    date_hierarchy = 'created_at'











from django.contrib import admin
from .models import Video

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'video')
