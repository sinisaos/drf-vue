from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager

User = get_user_model()


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, verbose_name="question")
    content = models.TextField()
    slug = models.SlugField(default=slugify(title), unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Question, self).save(*args, **kwargs)

    def get_answer_count(self):
        return Question.objects.filter(answers__question=self).count()

    def get_accepted_answer(self):
        try:
            accepted_answer = Answer.objects.get(question=self, is_accepted=True)
            return accepted_answer
        except Answer.DoesNotExist:
            accepted_answer = None


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(
        Question, related_name="answers", on_delete=models.CASCADE
    )
    content = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_accepted = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]
