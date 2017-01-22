import httpagentparser
from urlparse import urlparse

OTHER = 'Other'


def log_visit(db, request, url_id):
    """
    """
    try:
        browser_info = httpagentparser.detect(request.env.get('http_user_agent', ''))
    except:
        browser_info = {}

    browser_name = browser_info.get('browser', {}).get('name', OTHER)
    os_name = browser_info.get('os', {}).get('name', OTHER)

    try:
        import pdb; pdb.set_trace()
        parsed_uri = urlparse(request.env.get('http_referer', ''))
        referer_domain = parsed_uri.netloc or OTHER
    except:
        referer_domain = OTHER

    db.log_visit.insert(url=url_id, referer_url=referer_domain,
                        browser=browser_name, platform=os_name)


def date_in_words(time):
    """
    get date in words like just now, 2 minutes ago, 3 hours ago
    """
    from datetime import datetime
    now = datetime.now()
    diff = now - time

    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return time.strftime('%b %d, %Y')

    elif day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff / 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff / 3600) + " hours ago"
    elif day_diff == 1:
        return "Yesterday"
    elif day_diff < 7:
        return str(day_diff) + " days ago"
    elif day_diff == 7:
        return str(day_diff / 7) + "a week ago"

    return time.strftime('%b %d, %Y')
