from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]

    # Remove first_name and last_name since we're using full_name
    first_name = None
    last_name = None

    full_name = models.CharField(_('full name'), max_length=150)
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True,
        default='profile_images/default.png'
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES, 
        blank=True, 
        null=True
    )
    date_of_birth = models.DateField(blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    # Existing fields for profile and assessment
    has_completed_profile = models.BooleanField(default=False)
    has_completed_assessment = models.BooleanField(default=False)

    # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name='customuser_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='customuser_set',
        related_query_name='user',
    )

    # Override get_full_name to use full_name field
    def get_full_name(self):
        """Return the full name."""
        return self.full_name

    def get_short_name(self):
        """Return the short name (same as full name in your case)."""
        return self.full_name

    # 🧩 Role Aliases (simple property wrappers)
    @property
    def is_user(self):
        """Normal user (not doctor or admin)"""
        return not self.is_staff and not self.is_superuser

    @property
    def is_doctor(self):
        """Doctors have staff privileges"""
        return self.is_staff and not self.is_superuser

    @property
    def is_admin(self):
        """Admins have superuser privileges"""
        return self.is_superuser

    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

    def __str__(self):
        return f"{self.full_name} ({self.username})"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

from django.db import models
from django.conf import settings

class Assessment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assessments"
    )
    mood = models.CharField(max_length=50, blank=True, null=True)  # Example: Happy, Sad
    sleep_quality = models.CharField(max_length=50, blank=True, null=True)  # Example: Good, Poor
    expression_analysis = models.TextField(blank=True, null=True)  # Can hold text/JSON
    

    # Add ImageField to store the captured image
    captured_image = models.ImageField(upload_to='assessments/', null=True, blank=True)
    
    # Optional: keep the path field if you need it
    captured_image_path = models.CharField(max_length=500, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Assessment for {self.user} at {self.created_at.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = 'Assessment'
        verbose_name_plural = 'Assessments'




import os
from django.db import models
from django.conf import settings



def user_audio_path(instance, filename):
    # instance.user refers to the logged-in user assigned when saving the model
    return os.path.join("sound", str(instance.user.id), filename)

class AudioAnalysis(models.Model):
    STATUS_CHOICES = [
        ('uploaded', 'Uploaded'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ]
    
    EMOTION_CHOICES = [
        ('neutral', 'Neutral'),
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('angry', 'Angry'),
        ('fearful', 'Fearful'),
        ('disgusted', 'Disgusted'),
        ('surprised', 'Surprised'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Dynamic path: sound/<user_id>/<filename>
    audio_file = models.FileField(upload_to=user_audio_path)
    timestamp = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    analysis_result = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploaded')
    emotion = models.CharField(max_length=20, choices=EMOTION_CHOICES, null=True, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    duration = models.FloatField(null=True, blank=True, help_text="Duration in seconds")

    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Audio Analysis {self.id} - {self.user.username}"
    


class Article(models.Model):
    CATEGORY_CHOICES = [
        ('stress', 'Stress'),
        ('depression', 'Depression'),
        ('anxiety', 'Anxiety'),
        ('ptsd', 'PTSD'),
        ('meditation', 'Meditation'),
        ('selfcare', 'Self Care'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles")
    image = models.ImageField(upload_to="articles/", blank=True, null=True)  # optional
    created_at = models.DateTimeField(auto_now_add=True)

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.rating for r in ratings) / ratings.count(), 1)
        return 0

    def total_likes(self):
        return self.likes.count()

    def total_views(self):
        return self.views.count()

    def __str__(self):
        return self.title


class ArticleLike(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="liked_articles")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("article", "user")

    def __str__(self):
        return f"{self.user.username} liked {self.article.title}"


class ArticleRating(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rated_articles")
    rating = models.PositiveIntegerField(default=0)  # 1–5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("article", "user")

    def __str__(self):
        return f"{self.user.username} rated {self.article.title} {self.rating} stars"


class ArticleView(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="views")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"View on {self.article.title}"




class UserScore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # ==== Basic Info (10 points) ====
    age_score = models.FloatField(default=0)
    bmi_score = models.FloatField(default=0)
    sleep_score = models.FloatField(default=0)

    # ==== Mood (10 points) ====
    mood_score = models.FloatField(default=0)
    mood_label = models.CharField(max_length=20, blank=True, null=True)

    # ==== Text Emotion (25 points) ====
    text_label = models.CharField(max_length=20, blank=True, null=True)
    text_sentiment_score = models.FloatField(default=0)
    text_emotion_score = models.FloatField(default=0)
    text_negative_keywords_score = models.FloatField(default=0)

    # ==== Image Emotion (25 points) ====
    image_expression_score = models.FloatField(default=0)
    image_fatigue_score = models.FloatField(default=0)
    image_darkcircles_score = models.FloatField(default=0)
    image_stressmicro_score = models.FloatField(default=0)

    # ==== Voice Emotion (30 points) ====
    voice_tone_score = models.FloatField(default=0)
    voice_pitch_score = models.FloatField(default=0)
    voice_speed_score = models.FloatField(default=0)
    voice_hesitation_score = models.FloatField(default=0)
    voice_stress_score = models.FloatField(default=0)

    # ==== Final Combined Score ====
    total_score = models.FloatField(default=0)

    

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mental Health Assessment - User {self.user_id} - Score {self.total_score}"
    











from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
