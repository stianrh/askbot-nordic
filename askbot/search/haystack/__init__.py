from django.conf import settings
from django.utils.translation import get_language

from haystack import indexes
from celery_haystack.indexes import CelerySearchIndex

from askbot.models import Thread, Post, User


class ThreadIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    added_at = indexes.DateTimeField(model_attr='added_at')
    last_activity_at = indexes.DateTimeField(model_attr='last_activity_at')
    answer_count = indexes.IntegerField(model_attr='answer_count')
    points = indexes.IntegerField(model_attr='points')
    #tags = indexes.MultiValueField()
    closed = indexes.BooleanField(model_attr='closed')
    has_accepted_answer = indexes.BooleanField()
    followed_by = indexes.MultiValueField()

    def get_model(self):
        return Thread

    def index_queryset(self, using=None):
        if getattr(settings, 'ASKBOT_MULTILINGUAL', True):
            lang_code = get_language()[:2]
            return self.get_model().objects.filter(language_code__startswith=lang_code,
                                                   deleted=False)
        else:
            return self.get_model().objects.filter(deleted=False)

    def prepare_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def prepare_followed_by(self, obj):
        return [user.id for user in obj.followed_by.all()]

    def prepare_has_accepted_answer(self, obj):
        return obj.has_accepted_answer()


class UserIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return User

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
