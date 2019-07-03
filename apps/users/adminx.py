from django.utils.safestring import mark_safe

from users.models import NoteInfo, UserProfile, FeedBackInfo
from xadmin.views import CommAdminView
import xadmin


class ComSetting(object):
    site_title = '石井社'
    site_footer = '管理系统'


class NoteInfoXadmin(object):
    list_display = ['id', 'content', 'add_time']
    model_icon='fa fa-bullhorn'

class XadminXadmin(object):
    list_display = ['id', 'name', 'mobile', 'group', 'work', 'is_active', 'add_time']
    list_display_links = ['id', 'name', 'mobile']
    list_editable = ['name', 'mobile', 'is_active']
    exclude = ['password', 'last_login', 'groups', 'username', 'first_name', 'last_name', 'email', 'is_staff',
               'date_joined', 'user_permissions', 'is_superuser']

    readonly_fields = ['openid']


class FeedBackInfoXadmin(object):
    list_display = ['id', 'content', 'add_time', 'user']


xadmin.site.register(NoteInfo, NoteInfoXadmin)
xadmin.site.register(CommAdminView, ComSetting)
xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile, XadminXadmin)
xadmin.site.register(FeedBackInfo, FeedBackInfoXadmin)
