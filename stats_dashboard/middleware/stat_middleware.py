from django.middleware.common import MiddlewareMixin
from ..models import BrowserSession
import uuid


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def parse_user_agent(agent):
    browsers = {
        "edg": "Microsoft Edge",
        "chrome": "Chrome",
        "firefox": "Firefox",
        "op": "Opera",
        "opera": "Opera",
        "safari": "Safari",
        "instagram": "Instagram",
        "fban": "Facebook",
        "fbav": "Facebook",
        "msie": "Internet Explorer",
        "trident": "Internet Explorer",
        "snapchat": "Snapchat"
    }

    devices = {
        "iphone": "iPhone",
        "ipad": "iPad",
        "android": "Android",
        "windows": "Windows",
        "linux": "Linux",
        "macintosh": "Macintosh",
        "tesla": "Tesla"
    }

    agent = agent.lower()

    agent_info = {
        "browser": "",
        "device": "",
    }

    for browser in browsers.keys():
        if browser in agent:
            agent_info["browser"] = browsers[browser]
            break

    for device in devices.keys():
        if device in agent:
            agent_info["device"] = devices[device]
            break

    return agent_info


class StatMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # get stat token cookie
        token = request.COOKIES.get("statsid")

        # if token is available, try to find existing BrowserSession instance by uuid
        if token:
            try:
                session = BrowserSession.objects.get(token=token)
            except BrowserSession.DoesNotExist:
                token = None
            else:
                request.stat_session = session

        # create new session instance if session doesn't exist
        if not token:
            new_token = uuid.uuid4()
            ip = get_client_ip(request)
            agent = request.META.get("User-Agent", "") if "User-Agent" in request.META.keys() else request.META.get("HTTP_USER_AGENT", "")

            agent_info = parse_user_agent(agent)

            session = BrowserSession.objects.create(
                token=new_token,
                ip=ip,
                agent=agent,
                browser=agent_info["browser"],
                device=agent_info["device"],
            )
            request.stat_session = session

    def process_response(self, request, response):
        response.set_cookie("statsid", request.stat_session.token)
        return response
