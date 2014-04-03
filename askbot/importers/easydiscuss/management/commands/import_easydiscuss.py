from __future__ import unicode_literals

import traceback
import json
from datetime import datetime

from django.db import transaction
from django.core.management.base import BaseCommand
from askbot.utils.console import ProgressBar

from askbot.models import User, tag, post, question, user
from askbot.importers.easydiscuss.models import *
from askbot.importers.easydiscuss import bbcode2markdown

class Command(BaseCommand):

    @transaction.commit_manually
    def handle(self, *args, **kwargs):
        try:
            LANGUAGE = 'en'

            nordic_group = user.Group.objects.get_or_create(
                name='Nordic employees',
                openness=user.Group.CLOSED,
            )

            ed_users = EfsqtDiscussUsers.objects.using('devzone').all()
            count = ed_users.count()
            message = 'Importing %i users' % count
            for ed_user in ProgressBar(ed_users.iterator(), count, message):
                jm_user = EfsqtUsers.objects.using('devzone').get(id=ed_user.id)
                jm_usergroups = EfsqtUserUsergroupMap.objects.using('devzone').filter(user_id=ed_user.id)

                ab_user = User()
                ab_user.id = ed_user.id
                ab_user.save()

                for ug in jm_usergroups:
                    if ug.group_id in [7, 8]:
                        ab_user.is_staff = True
                    if ug.group_id == 8:
                        ab_user.is_superuser = True

                if ed_user.edited == 1 and ed_user.params:
                    params = json.loads(ed_user.params)
                    if 'show_twitter' in params and params['show_twitter'] == '1':
                        ab_user.twitter_handle = params['twitter']
                    if 'show_linkedin' in params and params['show_linkedin'] == '1':
                        ab_user.linkedin_profile = params['linkedin']
                    if 'show_website' in params and params['show_website'] == '1':
                        ab_user.website = params['website']

                ab_user.username = jm_user.username
                ab_user.real_name = jm_user.name or jm_user.username
                ab_user.email = jm_user.email
                ab_user.password = jm_user.password
                ab_user.about = ed_user.description
                ab_user.date_joined = jm_user.registerdate or datetime.now()
                ab_user.last_login = jm_user.lastvisitdate or datetime.now()
                ab_user.last_seen = jm_user.lastvisitdate or datetime.now()
                #ab_user.status
                #ab_user.last_name
                #ab_user.gold
                #ab_user.social_sharing_mode
                #ab_user.interesting_tags
                #ab_user.subscribed_tags
                #ab_user.email_key
                #ab_user.first_name
                #ab_user.email_isvalid
                #ab_user.is_fake
                #ab_user.languages
                #ab_user.date_of_birth
                #ab_user.location
                #ab_user.new_response_count
                #ab_user.company
                #ab_user.is_active
                #ab_user.consecutive_days_visit_count
                #ab_user.email_tag_filter_strategy
                #ab_user.silver
                #ab_user.bronze
                #ab_user.questions_per_page
                #ab_user.email_signature
                #ab_user.show_country
                #ab_user.show_marked_tags
                #ab_user.twitter_access_token
                #ab_user.country
                #ab_user.display_tag_filter_strategy
                #ab_user.seen_response_count
                #ab_user.ignored_tags
                #ab_user.reputation
                #ab_user.gravatar
                #ab_user.avatar_type
                ab_user.save()

                for ug in jm_usergroups:
                    if ug.group_id == 13:
                        user.GroupMembership.objects.get_or_create(
                            user=ab_user, group=nordic_group, level=user.GroupMembership.FULL
                        )

            transaction.commit()

            # ed_post_tags = EfsqtDiscussPostsTags.objects.using('devzone').all()
            # count = ed_post_tags.count()
            # message = 'Importing %i post-tag relationships' % count
            # for ed_post_tag in ProgressBar(ed_post_tags.iterator(), count, message):
            #     try:
            #         ab_post_tag = question.Thread.tags.through()
            #         ab_post_tag.thread_id = ed_post_tag.post_id
            #         ab_post_tag.tag_id = ed_post_tag.tag_id
            #         ab_post_tag.save()
            #     except:
            #         pass

            # transaction.commit()

            # ed_tags = EfsqtDiscussTags.objects.using('devzone').all()
            # count = ed_tags.count()
            # message = 'Importing %i tags' % count
            # for ed_tag in ProgressBar(ed_tags.iterator(), count, message):
            #     ab_tag = tag.Tag()
            #     ab_tag.id = ed_tag.id
            #     ab_tag.name = ed_tag.title.lower()
            #     ab_tag.created_by_id = ed_tag.user_id
            #     ab_tag.used_count = question.Thread.tags.through.objects.filter(tag_id=ab_tag.id).count()
            #     ab_tag.save()

            # transaction.commit()

            everyone = user.Group.objects.get_global_group()
            admin = User.objects.filter(is_staff=True)[0]

            ed_posts = EfsqtDiscussPosts.objects.using('devzone').filter(parent_id=0)
            count = ed_posts.count()
            message = 'Importing %i threads' % count
            for ed_post in ProgressBar(ed_posts.iterator(), count, message):
                ab_thread = question.Thread()
                ab_thread.id = ed_post.id
                ab_thread.title = ed_post.title
                ab_thread.view_count = ed_post.hits
                ab_thread.last_activity_at = ed_post.modified

                try:
                    author = User.objects.get(id=ed_post.user_id)
                    ab_thread.last_activity_by_id = author.id
                except:
                    if not '@' in ed_post.poster_email:
                        ed_post.poster_email = 'noreply@nordicsemi.no'
                    ab_thread.last_activity_by_id = admin.get_or_create_fake_user(ed_post.poster_name, ed_post.poster_email).id

                ab_thread.language_code = LANGUAGE
                ab_thread.closed = ed_post.islock
                ab_thread.closed_at = ed_post.lockdate
                ab_thread.added_at = ed_post.created
                ab_thread.points = ed_post.sum_totalvote
                #ab_thread.favourite_count = 0
                #ab_thread.answer_count = 0
                #ab_thread.followed_by =
                #ab_thread.favourited_by =
                #ab_thread.accepted_answer =
                #ab_thread.answer_accepted_at =
                #ab_thread.tagnames = ', '.join()
                ab_thread.save()
                ab_thread.add_to_groups([everyone])

            transaction.commit()

            ed_posts = EfsqtDiscussPosts.objects.using('devzone').filter(parent_id=0)
            count = ed_posts.count()
            message = 'Importing %i questions' % count
            for ed_post in ProgressBar(ed_posts.iterator(), count, message):
                ab_post = post.Post()
                ab_post.id = ed_post.id
                ab_post.post_type = 'question'
                ab_post.parent_id = None 
                ab_post.thread_id = ed_post.id

                try:
                    author = User.objects.get(id=ed_post.user_id)
                    ab_post.author = author
                except:
                    if not '@' in ed_post.poster_email:
                        ed_post.poster_email = 'anonymous@askbot.org'
                    ab_post.author = admin.get_or_create_fake_user(ed_post.poster_name, ed_post.poster_email)

                ab_post.added_at = ed_post.created
                ab_post.locked = ed_post.islock
                ab_post.locked_at = ed_post.lockdate
                ab_post.points = ed_post.sum_totalvote
                ab_post.vote_up_count = ed_post.num_likes
                ab_post.vote_down_count = ed_post.num_negvote
                ab_post.last_edited_at = ed_post.modified
                ab_post.last_edited_by_id = ed_post.user_id or None
                ab_post.text = bbcode2markdown.convert(ed_post.content)
                ab_post.html = ab_post.parse_post_text()['html']
                ab_post.summary = ab_post.get_snippet()
                ab_post.language_code = LANGUAGE
                ab_post.is_anonymous = (ed_post.user_id == 0)
                ab_post.save()
                ab_post.add_to_groups([everyone])
                revision = ab_post.add_revision(author=ab_post.author, text=ab_post.text, revised_at=ab_post.last_edited_at)
                revision.save()

                post_tags = EfsqtDiscussPostsTags.objects.using('devzone').filter(post_id=ab_post.id).values_list('tag_id', flat=True)
                tags = EfsqtDiscussTags.objects.using('devzone').filter(id__in=post_tags).values_list('title', flat=True)
                tagnames = ', '.join(tags)
                ab_post.thread.update_tags(tagnames.lower(), admin)

            transaction.commit()

            ed_posts = EfsqtDiscussPosts.objects.using('devzone').exclude(parent_id=0)
            count = ed_posts.count()
            message = 'Importing %i answers' % count
            for ed_post in ProgressBar(ed_posts.iterator(), count, message):
                ab_post = post.Post()
                ab_post.id = ed_post.id
                ab_post.post_type = 'answer'
                ab_post.parent_id = ed_post.parent_id
                ab_post.thread_id = ed_post.parent_id

                try:
                    author = User.objects.get(id=ed_post.user_id)
                    ab_post.author = author
                except:
                    if not '@' in ed_post.poster_email:
                        ed_post.poster_email = 'anonymous@askbot.org'
                    ab_post.author = admin.get_or_create_fake_user(ed_post.poster_name, ed_post.poster_email)

                ab_post.added_at = ed_post.created
                ab_post.locked = ed_post.islock
                ab_post.locked_at = ed_post.lockdate
                ab_post.points = ed_post.sum_totalvote
                ab_post.vote_up_count = ed_post.num_likes
                ab_post.vote_down_count = ed_post.num_negvote
                ab_post.last_edited_at = ed_post.modified
                ab_post.last_edited_by_id = ed_post.user_id or ab_post.author.id
                ab_post.text = bbcode2markdown.convert(ed_post.content)
                ab_post.html = ab_post.parse_post_text()['html']
                ab_post.summary = ab_post.get_snippet()
                ab_post.language_code = LANGUAGE
                ab_post.is_anonymous = (ed_post.user_id == 0)
                ab_post.save()
                ab_post.add_to_groups([everyone])
                if ed_post.answered:
                    ab_post.thread.accepted_answer_id = ab_post.id
                    ab_post.thread.save()

                revision = ab_post.add_revision(author=ab_post.author, text=ab_post.text, revised_at=ab_post.last_edited_at)
                revision.save()

            transaction.commit()

            ed_comments = EfsqtDiscussComments.objects.using('devzone').all()
            count = ed_comments.count()
            message = 'Importing %i comments' % count
            for ed_comment in ProgressBar(ed_comments.iterator(), count, message):
                ab_post = post.Post()
                ab_post.post_type = 'comment'
                ab_post.parent_id = ed_comment.post_id

                try:
                    ab_post.thread = post.Post.objects.get(id=ed_comment.post_id).thread
                except:
                    pass

                try:
                    author = User.objects.get(id=ed_comment.user_id)
                    ab_post.author = author
                except:
                    if not '@' in ed_comment.email:
                        ed_comment.email = 'anonymous@askbot.org'
                    ab_post.author = admin.get_or_create_fake_user(ed_comment.name, ed_comment.email)

                ab_post.added_at = ed_comment.created
                ab_post.last_edited_at = ed_comment.modified
                ab_post.text = ed_comment.comment
                ab_post.html = ab_post.parse_post_text()['html']
                ab_post.summary = ab_post.get_snippet()
                ab_post.language_code = LANGUAGE
                ab_post.is_anonymous = (ed_comment.user_id == 0)
                ab_post.save()
                ab_post.add_to_groups([everyone])
                revision = ab_post.add_revision(author=ab_post.author, text=ab_post.text, revised_at=ab_post.last_edited_at)
                revision.save()

            transaction.commit()

        except:
            print
            print traceback.format_exc()
            transaction.rollback()
            print 'Exception. Pending transaction rolled back.'
            raise
