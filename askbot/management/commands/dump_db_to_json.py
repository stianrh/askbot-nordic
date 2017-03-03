from django.core.management.base import BaseCommand, CommandError
from askbot.models import Thread, Post, User
from cases.models import Case
import datetime
import time
import json
import avatar
from askbot.const import CLOSE_REASONS
from collections import OrderedDict

DATETIME_FORMAT = "%H:%M:%S,%d.%m.%y"
def format_datetime(dt):
    #return dt.strftime(DATETIME_FORMAT)
    try:
        return int(time.mktime(dt.timetuple()))
    except:
        return None

class Command(BaseCommand):
    help = 'Dump JSON data for all of devzone. \nEx: dump_db_to_json 01.01.2015 31.12.2016 desc'
    args = '[date_from date_to desc]'

    def __init__(self, *args, **options):
        super(Command, self).__init__(*args, **options)
        self.t_dict = {'threads':[], 'users':[], 'close_reasons': {}}
        self.t_dict_desc = {'threads': "list of THREAD_DICT", 'users': "list of USER_DICT", 'close_reasons': "CLOSE_REASONS_DICT"}
        self.relevant_users = set() 

    def get_users(self):
        self.users = User.objects.all()

    def create_user_dict(self, u, desc=False):
        try:
            av = u.avatar_set.order_by("-primary", "-date_uploaded")[0]
            av_url = av.avatar.url
        except:
            av_url = None
        d = {
            'u_id': u.id if not desc else "this USER_DICT id",
            'username': u.username if not desc else "string",
            'email': u.email if not desc else "string",
            'reputation': u.reputation if not desc else "int",
            'screen_name': u.real_name if not desc else "string",
            #'password_hash': u.password,
            'is_nordic_employee': u.is_nordic_employee() if not desc else "bool",
            'is_moderator': u.is_moderator() if not desc else "bool",
            'date_joined': format_datetime(u.date_joined) if not desc else "unix timestamp",
            'last_seen': format_datetime(u.last_seen) if not desc else "unix timestamp",
            'avatar_url': av_url if not desc else "avatar url string",
            'company': (u.company if u.company else None) if not desc else "string",
            'website': (u.website if u.website else None) if not desc else "url string",
            'twitter': (u.twitter_handle if u.twitter_handle else None) if not desc else "string",
            'linkedin': (u.linkedin_profile if u.linkedin_profile else None) if not desc else "url string",
            'country': (u.country.code if u.show_country else None) if not desc else "country code string",
            'city': (u.location if u.location else None) if not desc else "string",
            'date_of_birth': format_datetime(u.date_of_birth) if not desc else "unix timestamp",
            'about': (u.about if u.about else None) if not desc else "string"

        }
        sort_order = ['u_id', 'username', 'screen_name', 'email', 'reputation', 'is_nordic_employee', 'is_moderator', 'date_joined', 'last_seen', 'avatar_url', 'company', 'website', 'twitter', 'linkedin', 'country', 'city', 'date_of_birth', 'about']
        self.t_dict['users'].append(OrderedDict(sorted(d.iteritems(), key=lambda (k,v): sort_order.index(k))))

    def create_close_reason_dict(self):
        for cr in CLOSE_REASONS:
            self.t_dict['close_reasons'].update({
                cr[0]: unicode(cr[1])
            })

    def get_threads(self, *args, **options):
        date_from = args[0].split('.')
        date_from = datetime.datetime(int(date_from[2]), int(date_from[1]), int(date_from[0]))
        date_to = args[1].split('.')
        date_to = datetime.datetime(int(date_to[2]), int(date_to[1]), int(date_to[0]))
        self.threads = Thread.objects.filter(added_at__lte=date_to, added_at__gte=date_from).order_by('added_at')
    def create_post_dict(self, q, desc=False):
        if not desc:
            c = Post.objects.get_comments().filter(parent=q)
            self.relevant_users.add(q.author_id)
            self.relevant_users.add(q.last_edited_by_id) if q.last_edited_by_id else None
        d = {
            'p_id': q.id if not desc else "this POST_DICT id",
            'author': q.author_id if not desc else "USER_DICT id",
            'added_at': format_datetime(q.added_at) if not desc else "unix timestamp",
            'last_edited_at': (format_datetime(q.last_edited_at) if q.last_edited_at else None) if not desc else "unix timestamp",
            'last_edited_by': q.last_edited_by_id if not desc else "USER_DICT id",
            #'deleted': q.deleted,
            'vote_up_count': q.vote_up_count if not desc else "int",
            'vote_down_count': q.vote_down_count if not desc else "int",
            'text': q.text if not desc else "post content markdown string"
        }
        if desc:
            d.update({'comments': "list of POST_DICT (not included if post is comment)"})
        elif not q.is_comment():
            d.update({'comments': ([self.create_post_dict(x) for x in c] if c else None) if not desc else "list of POST_DICT"})

        sort_order = ['p_id', 'author', 'added_at', 'last_edited_at', 'last_edited_by', 'vote_up_count', 'vote_down_count', 'text', 'comments']
        ordered_dict = OrderedDict(sorted(d.iteritems(), key=lambda (k,v): sort_order.index(k)))

        return ordered_dict 

    def get_case_object(self, t):
        c_set = t.case_set.all()
        c = None
        if c_set.count() == 1:
            c = c_set[0]
        elif c_set.count() > 1:
            print "More than one case object pointing to a single thread"
            raise
        return c

    def create_case_dict(self, t, desc=False):
        if not desc:
            c = self.get_case_object(t)
            try:
                self.relevant_users.add(c.assigned_to.user.id)
            except:
                pass
        else:
            c = True
        if c:
            d = {
                'c_id': c.id if not desc else "this CASE_DICT id",
                'assigned_to': (c.assigned_to.user.id if c.assigned_to else None) if not desc else "USER_DICT id",
                'wait_for_response': c.wait_for_response if not desc else "bool",
                'comment': (c.comment if c.comment else None) if not desc else "string",
            }
            sort_order = ['c_id', 'assigned_to', 'wait_for_response', 'comment']
            ordered_dict = OrderedDict(sorted(d.iteritems(), key=lambda (k,v): sort_order.index(k)))
            return ordered_dict
        else:
            return None
    def get_case_followers(self, t):
        c = self.get_case_object(t)
        if c:
            l = list(c.follow_caseuser.values_list('user_id', flat=True))
            return l
        else:
            return []

    def create_thread_dict(self, t, desc=False):
        if not desc:
            q = t._question_post()
            a = t.get_answers()
            ff = list(t.followed_by.values_list('id', flat=True))
            cf = self.get_case_followers(t)
            f = list(set(ff + cf))
            self.relevant_users.update(f)
            self.relevant_users.add(q.deleted_by_id) if q.deleted_by_id else None
            self.relevant_users.add(t.closed_by_id) if t.closed_by_id else None

        d = {
            't_id': t.id if not desc else "this THREAD_DICT id",
            'deleted': t.deleted if not desc else "bool",
            'deleted_at': format_datetime(q.deleted_at) if not desc else "unix timestamp",
            'deleted_by': q.deleted_by_id if not desc else "USER_DICT id",
            'closed': t.closed if not desc else "bool",
            'closed_by': t.closed_by_id if not desc else "USER_DICT id",
            'closed_at': format_datetime(t.closed_at) if not desc else "unix timestamp",
            #'closed_reason': t.get_close_reason_display(),
            'closed_reason': t.close_reason if not desc else "CLOSE_REASONS_DICT key",
            'accepted_answer': t.accepted_answer_id if not desc else "POST_DICT id",
            'accepted_answer_at': format_datetime(t.answer_accepted_at) if not desc else "unix timestamp",
            'tags': (t.tagnames.split(', ') if t.tagnames else None) if not desc else "list of strings of tags",
            'question': self.create_post_dict(q) if not desc else "POST_DICT",
            'answers': ([self.create_post_dict(x) for x in a ] if a else None) if not desc else "list of POST_DICT",
            'followed_by': (f if f else None) if not desc else "list of USER_DICT id",
            'case': self.create_case_dict(t) if not desc else "CASE_DICT",
            'title': t.title if not desc else "string",
        }
        sort_order = ['t_id', 'deleted', 'deleted_at', 'deleted_by', 'closed', 'closed_at', 'closed_reason', 'closed_by', 'accepted_answer', 'accepted_answer_at', 'tags', 'followed_by', 'case', 'title', 'question', 'answers']
        self.t_dict['threads'].append(OrderedDict(sorted(d.iteritems(), key=lambda (k,v): sort_order.index(k))))

    def handle(self, *args, **options): 
        sort_order = ['threads', 'users', 'close_reasons']
        desc = False
        all_users = False
        try:
            if args[2] == "desc":
                desc = True
            if args[2] == "all":
                all_users = True
        except:
            pass

        if not desc:
            self.get_threads(*args, **options)
            for t in self.threads:
                self.create_thread_dict(t)


            if all_users:
                self.get_users()
                for u in self.users:
                    self.create_user_dict(u)
            else:
                for u in self.relevant_users:
                    self.create_user_dict(User.objects.get(id=u))

            self.create_close_reason_dict()

            ordered_dict = OrderedDict(sorted(self.t_dict.iteritems(), key=lambda (k,v): sort_order.index(k)))

            j = json.dumps(ordered_dict, indent=2)
            print j

        else:
            ordered_t_dict = OrderedDict(sorted(self.t_dict_desc.iteritems(), key=lambda (k,v): sort_order.index(k)))
            self.create_thread_dict(desc=True, t=None) 
            ordered_p_dict = self.create_post_dict(desc=True, q=None)
            ordered_c_dict = self.create_case_dict(desc=True, t=None)
            self.create_user_dict(desc=True, u=None)
            print "MAIN_DICT ="
            print json.dumps(ordered_t_dict, indent=2)
            print "THREAD_DICT ="
            print json.dumps(self.t_dict['threads'][0], indent=2)
            print "POST_DICT ="
            print json.dumps(ordered_p_dict, indent=2) 
            print "CASE_DICT = "
            print json.dumps(ordered_c_dict, indent=2)
            print "USER_DICT = "
            print json.dumps(self.t_dict['users'][0], indent=2)
            print "CLOSE_REASONS_DICT ="
            print json.dumps({"id": "string"}, indent=2)
