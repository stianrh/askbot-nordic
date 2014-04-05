from optparse import make_option
from django.core.management.base import BaseCommand
from askbot.models import Post
import datetime


class Command(BaseCommand):
    help = 'Deletes unanswered posts with associated objects older than a given age.'
    option_list = BaseCommand.option_list + (
        make_option('--age',
            action = 'store',
            type = 'int',
            dest = 'age_in_days',
            default = None,
            help = 'An integer value for the age of posts to delete, in days'
        ),
    )

    def handle(self, *args, **options):
        age_in_days = options['age_in_days']
        if not age_in_days:
            print 'Please supply an --age <number of days>'

        limit_date = datetime.datetime.now() + datetime.timedelta(days=-age_in_days)

        unanswered_posts = Post.objects.filter(
            post_type='question'
        ).filter(
            thread__last_activity_at__lte=limit_date
        ).filter(
            thread__answer_count=0
        )

        count = unanswered_posts.count()
        unanswered_posts.delete()

        print '%i unanswered posts and associated objects deleted' % count
