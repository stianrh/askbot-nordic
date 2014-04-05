from optparse import make_option
from django.core.management.base import BaseCommand
from askbot.models import Post
import datetime


class Command(BaseCommand):
    help = 'Deletes threads with no activity for a given number of days (or older).'
    option_list = BaseCommand.option_list + (
        make_option('--age',
            action = 'store',
            type = 'int',
            dest = 'age_in_days',
            default = None,
            help = 'An integer value for the age of threads to delete, in days'
        ),
    )

    def handle(self, *args, **options):
        age_in_days = options['age_in_days']
        if not age_in_days:
            print 'Please supply an --age <number of days>'

        limit_date = datetime.datetime.now() + datetime.timedelta(days=-age_in_days)

        dead_threads = Post.objects.filter(
            post_type='question'
        ).filter(
            thread__last_activity_at__lte=limit_date
        )

        count = dead_threads.count()
        dead_threads.delete()

        print '%i dead threads and associated objects deleted' % count
