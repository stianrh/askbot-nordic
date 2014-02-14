# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class EfsqtDiscussAttachments(models.Model):
    uid = models.IntegerField()
    title = models.TextField()
    type = models.CharField(max_length=200L)
    path = models.TextField()
    created = models.DateTimeField()
    published = models.IntegerField()
    mime = models.TextField()
    size = models.TextField()
    class Meta:
        db_table = 'efsqt_discuss_attachments'

class EfsqtDiscussCaptcha(models.Model):
    response = models.CharField(max_length=5L)
    created = models.DateTimeField()
    class Meta:
        db_table = 'efsqt_discuss_captcha'

class EfsqtDiscussCategory(models.Model):
    created_by = models.IntegerField()
    title = models.CharField(max_length=255L)
    description = models.TextField()
    alias = models.CharField(max_length=255L, blank=True)
    created = models.DateTimeField()
    status = models.IntegerField()
    published = models.IntegerField()
    ordering = models.IntegerField()
    avatar = models.CharField(max_length=255L, blank=True)
    parent_id = models.IntegerField(null=True, blank=True)
    private = models.IntegerField()
    default = models.IntegerField()
    level = models.IntegerField(null=True, blank=True)
    lft = models.IntegerField(null=True, blank=True)
    rgt = models.IntegerField(null=True, blank=True)
    params = models.TextField()
    container = models.IntegerField()
    class Meta:
        db_table = 'efsqt_discuss_category'

class EfsqtDiscussComments(models.Model):
    comment = models.TextField(blank=True)
    name = models.CharField(max_length=255L)
    title = models.CharField(max_length=255L)
    email = models.CharField(max_length=255L, blank=True)
    url = models.CharField(max_length=255L, blank=True)
    ip = models.CharField(max_length=255L, blank=True)
    created = models.DateTimeField()
    modified = models.DateTimeField(null=True, blank=True)
    published = models.IntegerField(null=True, blank=True)
    ordering = models.IntegerField(null=True, blank=True)
    post_id = models.BigIntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    sent = models.IntegerField()
    lft = models.IntegerField()
    class Meta:
        db_table = 'efsqt_discuss_comments'

class EfsqtDiscussConversations(models.Model):
    created = models.DateTimeField()
    created_by = models.BigIntegerField()
    lastreplied = models.DateTimeField()
    class Meta:
        db_table = 'efsqt_discuss_conversations'

class EfsqtDiscussConversationsParticipants(models.Model):
    conversation_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    class Meta:
        db_table = 'efsqt_discuss_conversations_participants'

class EfsqtDiscussFavourites(models.Model):
    created_by = models.BigIntegerField()
    post_id = models.BigIntegerField()
    type = models.CharField(max_length=20L)
    created = models.DateTimeField()
    class Meta:
        db_table = 'efsqt_discuss_favourites'

class EfsqtDiscussHashkeys(models.Model):
    uid = models.BigIntegerField()
    type = models.CharField(max_length=255L)
    key = models.TextField()
    class Meta:
        db_table = 'efsqt_discuss_hashkeys'

class EfsqtDiscussLikes(models.Model):
    type = models.CharField(max_length=20L)
    content_id = models.IntegerField()
    created_by = models.BigIntegerField(null=True, blank=True)
    created = models.DateTimeField()
    class Meta:
        db_table = 'efsqt_discuss_likes'

class EfsqtDiscussOauth(models.Model):
    type = models.CharField(max_length=255L)
    request_token = models.TextField()
    access_token = models.TextField()
    message = models.TextField()
    params = models.TextField()
    class Meta:
        db_table = 'efsqt_discuss_oauth'

class EfsqtDiscussOauthPosts(models.Model):
    post_id = models.BigIntegerField()
    oauth_id = models.BigIntegerField()
    class Meta:
        db_table = 'efsqt_discuss_oauth_posts'

class EfsqtDiscussPostTypes(models.Model):
    title = models.TextField()
    suffix = models.CharField(max_length=50L)
    created = models.DateTimeField()
    published = models.IntegerField()
    alias = models.CharField(max_length=255L)
    class Meta:
        db_table = 'efsqt_discuss_post_types'

class EfsqtDiscussPosts(models.Model):
    title = models.TextField(blank=True)
    alias = models.TextField()
    created = models.DateTimeField()
    modified = models.DateTimeField(null=True, blank=True)
    replied = models.DateTimeField()
    content = models.TextField()
    published = models.IntegerField()
    ordering = models.IntegerField()
    vote = models.IntegerField(null=True, blank=True)
    hits = models.IntegerField(null=True, blank=True)
    islock = models.IntegerField(null=True, blank=True)
    lockdate = models.DateTimeField()
    featured = models.IntegerField(null=True, blank=True)
    isresolve = models.IntegerField(null=True, blank=True)
    isreport = models.IntegerField(null=True, blank=True)
    answered = models.IntegerField(null=True, blank=True)
    user_id = models.BigIntegerField(null=True, blank=True)
    parent_id = models.BigIntegerField(null=True, blank=True)
    user_type = models.CharField(max_length=255L)
    poster_name = models.CharField(max_length=255L)
    poster_email = models.CharField(max_length=255L)
    num_likes = models.IntegerField(null=True, blank=True)
    num_negvote = models.IntegerField(null=True, blank=True)
    sum_totalvote = models.IntegerField(null=True, blank=True)
    category_id = models.BigIntegerField()
    params = models.TextField()
    password = models.TextField(blank=True)
    legacy = models.IntegerField(null=True, blank=True)
    address = models.TextField(blank=True)
    latitude = models.CharField(max_length=255L, blank=True)
    longitude = models.CharField(max_length=255L, blank=True)
    content_type = models.CharField(max_length=25L, blank=True)
    post_status = models.IntegerField()
    post_type = models.CharField(max_length=100L)
    ip = models.CharField(max_length=255L)
    class Meta:
        db_table = 'efsqt_discuss_posts'

class EfsqtDiscussPostsTags(models.Model):
    post_id = models.BigIntegerField(null=True, blank=True)
    tag_id = models.BigIntegerField(null=True, blank=True)
    class Meta:
        db_table = 'efsqt_discuss_posts_tags'

class EfsqtDiscussSubscription(models.Model):
    userid = models.BigIntegerField()
    member = models.IntegerField()
    type = models.CharField(max_length=100L)
    cid = models.BigIntegerField()
    email = models.CharField(max_length=100L)
    fullname = models.CharField(max_length=255L)
    interval = models.CharField(max_length=100L)
    created = models.DateTimeField()
    sent_out = models.DateTimeField()
    class Meta:
        db_table = 'efsqt_discuss_subscription'

class EfsqtDiscussTags(models.Model):
    title = models.CharField(max_length=100L)
    alias = models.CharField(max_length=100L)
    created = models.DateTimeField()
    published = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'efsqt_discuss_tags'

class EfsqtDiscussUsers(models.Model):
    nickname = models.CharField(max_length=255L, blank=True)
    avatar = models.CharField(max_length=255L, blank=True)
    description = models.TextField(blank=True)
    url = models.CharField(max_length=255L, blank=True)
    params = models.TextField(blank=True)
    alias = models.CharField(max_length=255L, blank=True)
    points = models.BigIntegerField()
    latitude = models.CharField(max_length=255L, blank=True)
    longitude = models.CharField(max_length=255L, blank=True)
    location = models.TextField()
    signature = models.TextField()
    edited = models.IntegerField()
    posts_read = models.TextField(blank=True)
    site = models.TextField(blank=True)
    class Meta:
        db_table = 'efsqt_discuss_users'

class EfsqtDiscussViews(models.Model):
    user_id = models.BigIntegerField(unique=True)
    hash = models.CharField(max_length=255L)
    created = models.DateTimeField()
    ip = models.CharField(max_length=20L)
    class Meta:
        db_table = 'efsqt_discuss_views'

class EfsqtDiscussVotes(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    post_id = models.BigIntegerField(null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    ipaddress = models.CharField(max_length=15L, blank=True)
    value = models.IntegerField(null=True, blank=True)
    session_id = models.CharField(max_length=200L, blank=True)
    class Meta:
        db_table = 'efsqt_discuss_votes'

class EfsqtUserNotes(models.Model):
    user_id = models.IntegerField()
    catid = models.IntegerField()
    subject = models.CharField(max_length=100L)
    body = models.TextField()
    state = models.IntegerField()
    checked_out = models.IntegerField()
    checked_out_time = models.DateTimeField()
    created_user_id = models.IntegerField()
    created_time = models.DateTimeField()
    modified_user_id = models.IntegerField()
    modified_time = models.DateTimeField()
    review_time = models.DateTimeField()
    publish_up = models.DateTimeField()
    publish_down = models.DateTimeField()
    class Meta:
        db_table = 'efsqt_user_notes'

class EfsqtUserProfiles(models.Model):
    user_id = models.IntegerField()
    profile_key = models.CharField(max_length=100L)
    profile_value = models.CharField(max_length=255L)
    ordering = models.IntegerField()
    class Meta:
        db_table = 'efsqt_user_profiles'

class EfsqtUserUsergroupMap(models.Model):
    user_id = models.IntegerField()
    group_id = models.IntegerField()
    class Meta:
        db_table = 'efsqt_user_usergroup_map'

class EfsqtUsergroups(models.Model):
    parent_id = models.IntegerField()
    lft = models.IntegerField()
    rgt = models.IntegerField()
    title = models.CharField(max_length=100L)
    class Meta:
        db_table = 'efsqt_usergroups'

class EfsqtUsers(models.Model):
    name = models.CharField(max_length=255L)
    username = models.CharField(max_length=150L)
    email = models.CharField(max_length=100L)
    password = models.CharField(max_length=100L)
    usertype = models.CharField(max_length=25L)
    block = models.IntegerField()
    sendemail = models.IntegerField(null=True, db_column='sendEmail', blank=True) # Field name made lowercase.
    registerdate = models.DateTimeField(db_column='registerDate') # Field name made lowercase.
    lastvisitdate = models.DateTimeField(db_column='lastvisitDate') # Field name made lowercase.
    activation = models.CharField(max_length=100L)
    params = models.TextField()
    lastresettime = models.DateTimeField(db_column='lastResetTime') # Field name made lowercase.
    resetcount = models.IntegerField(db_column='resetCount') # Field name made lowercase.
    class Meta:
        db_table = 'efsqt_users'
