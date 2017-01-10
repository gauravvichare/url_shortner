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

    browser = browser_info.get('browser', {}).get('name', OTHER)
    os_name = browser_info.get('os', {}).get('name', OTHER)

    try:
        parsed_uri = urlparse(request.env.get('http_referer', ''))
        referer_domain = parsed_uri.netloc or OTHER
    except:
        referer_domain = OTHER

    db.log_visit.insert(url=url_id, referer_url=referer_domain,
                        browser=browser_name, platform=os_name)
