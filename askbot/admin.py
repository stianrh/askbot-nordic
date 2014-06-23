# -*- coding: utf-8 -*-
"""
:synopsis: connector to standard Django admin interface

To make more models accessible in the Django admin interface, add more classes subclassing ``django.contrib.admin.Model``

Names of the classes must be like `SomeModelAdmin`, where `SomeModel` must
exactly match name of the model used in the project
"""
from django.contrib import admin
from askbot import models

class PostAdmin(admin.ModelAdmin):
    """Post admin class"""
    list_display = [
        'post_type',
        'author',
        'added_at',
        'excerpt',
        'parent_excerpt',
        'points',
        'approved',
        'deleted',
        'locked',
        'comment_count',
        'offensive_flag_count',
        'last_edited_at',
        'last_edited_by',
    ]
    search_fields = ['author__username', 'text', 'parent__text']

    def excerpt(self, obj):
        return obj.text[:50] + '...'

    def parent_excerpt(self, obj):
        if obj.parent:
            return obj.parent.text[:50] + '...'
        return None

class TagAdmin(admin.ModelAdmin):
    """Tag admin class"""
    list_display = [
        'name',
        'created_by',
        'status',
        'used_count'
    ]

class VoteAdmin(admin.ModelAdmin):
    """Vote admin class"""

class FavoriteQuestionAdmin(admin.ModelAdmin):
    """FavoriteQuestion admin class"""

class PostRevisionAdmin(admin.ModelAdmin):
    """PostRevision admin class"""

class AwardAdmin(admin.ModelAdmin):
    """AwardAdmin admin class"""

class ReputeAdmin(admin.ModelAdmin):
    """ReputeAdmin admin class"""

class ActivityAdmin(admin.ModelAdmin):
    """ActivityAdmin admin class"""

class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['filename', 'filehash']
    search_fields = ['filehash']

admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Vote, VoteAdmin)
admin.site.register(models.FavoriteQuestion, FavoriteQuestionAdmin)
admin.site.register(models.PostRevision, PostRevisionAdmin)
admin.site.register(models.Award, AwardAdmin)
admin.site.register(models.Repute, ReputeAdmin)
admin.site.register(models.Activity, ActivityAdmin)
admin.site.register(models.Attachment, AttachmentAdmin)

admin.site.register(models.BulkTagSubscription)
