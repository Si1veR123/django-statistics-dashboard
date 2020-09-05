from django.db.models import *


class BrowserSession(Model):
    token = UUIDField(primary_key=True, unique=True)
    ip = GenericIPAddressField()
    agent = TextField()
    browser = CharField(max_length=50, null=True)
    device = CharField(max_length=50, null=True)
    start_time = DateTimeField(auto_now_add=True)


class PageSession(Model):
    page = TextField()
    browser_session = ForeignKey(BrowserSession, on_delete=CASCADE)
    new_to_website = BooleanField(default=None, null=True)
    referer = TextField(null=True)
    request_time = DateTimeField(auto_now_add=True)
    last_viewed = BooleanField(default=True)


class PageEvent(Model):
    page_session = ForeignKey(PageSession, on_delete=CASCADE)
    type = CharField(max_length=50)
    info = CharField(max_length=50)
