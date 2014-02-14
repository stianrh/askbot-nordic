from django.core.management.base import BaseCommand
from askbot.utils.console import ProgressBar

from askbot.models import tag, post, question
from askbot.importers.easydiscuss.models import *

class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        LANGUAGE = 'en'

        ed_tags = EfsqtDiscussTags.objects.using('devzone').all()
        count = ed_tags.count()
        message = 'Importing %i tags' % count
        for ed_tag in ProgressBar(ed_tags.iterator(), count, message):
            ab_tag = tag.Tag()
            ab_tag.id = ed_tag.id
            ab_tag.name = ed_tag.title
            ab_tag.created_by_id = ed_tag.user_id
            ab_tag.save()

        ed_post_tags = EfsqtDiscussPostsTags.objects.using('devzone').all()
        count = ed_post_tags.count()
        message = 'Importing %i post-tag relationships' % count
        for ed_post_tag in ProgressBar(ed_post_tags.iterator(), count, message):
            ab_post_tag = question.Thread.tags.through()
            ab_post_tag.thread_id = ed_post_tag.post_id
            ab_post_tag.tag_id = ed_post_tag.tag_id
            ab_post_tag.save()

        ed_posts = EfsqtDiscussPosts.objects.using('devzone').all()
        count = ed_posts.count()
        message = 'Importing %i posts' % count
        for ed_post in ProgressBar(ed_posts.iterator(), count, message):
            ab_thread_id = ed_post.id
            if ed_post.parent_id == 0:
                ab_thread = question.Thread()
                ab_thread.title = ed_post.title
                ab_thread.tagnames =
                ab_thread.view_count = ed_post.hits
                ab_thread.favourite_count =
                ab_thread.answer_count =
                ab_thread.last_activity_at =
                ab_thread.last_activity_by =
                ab_thread.language_code = LANGUAGE
                ab_thread.followed_by =
                ab_thread.favourited_by =
                ab_thread.closed = ed_post.is_lock
                ab_thread.closed_at = ed_post.lockdate
                ab_thread.accepted_answer =
                ab_thread.answer_accepted_at =
                ab_thread.added_at = ed_post.created
                ab_thread.points = ed_post.sum_totalvote

                ab_thread.id = ed_post.id
                ab_thread.save()
                post_type = 'question'
            else:
                ab_thread_id = ed_post.parent_id
                post_type = 'answer'

            ab_post = post.Post()
            ab_post.id = ed_post.id
            ab_post.post_type = post_type
            ab_post.parent_id = ed_post.parent_id
            ab_post.thread = ab_thread_id
            ab_post.author_id = ed_post.user_id
            ab_post.added_at = ed_post.created
            ab_post.locked = ed_post.is_lock
            ab_post.locked_at = ed_post.lockdate
            ab_post.points = ed_post.sum_totalvote
            ab_post.vote_up_count = ed_post.num_likes
            ab_post.vote_down_count = ed_post.num_negvote
            ab_post.last_edited_at = ed_post.modified
            ab_post.last_edited_by_id = ed_post.user_id
            ab_post.html =
            ab_post.text = ed_post.content
            ab_post.language_code = LANGUAGE
            ab_post.summary =
            ab_post.is_anonymous =
            ab_post.save()

        ed_comments = EfsqtDiscussComments.objects.using('devzone').all()
        count = ed_comments.count()
        message = 'Importing %i comments' % count
        for ed_comment in ProgressBar(ed_comments.iterator(), count, message):
            ab_post = post.Post()
            ab_post.post_type = 'comment'
            ab_post.parent_id = ed_comment.post_id
            ab_post.thread =
            ab_post.author_id = ed_comment.user_id
            ab_post.added_at = ed_comment.created
            ab_post.last_edited_at = ed_comment.modified
            ab_post.html =
            ab_post.text = ed_comment.comment
            ab_post.language_code = LANGUAGE
            ab_post.summary =
            ab_post.is_anonymous =
            ab_post.save()
