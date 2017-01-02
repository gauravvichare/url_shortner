# -*- coding: utf-8 -*-
from base62 import encode
NO_RECORD = -1


def index():
    short_link = session.get('short_link')
    if short_link:
        del session.short_link
    submit = INPUT(_class="btn btn-primary", _type="Submit", _value="Shorten")

    form = SQLFORM(db.url, buttons=[submit],hideerror=True)
    form.elements('input')[0]['_placeholder'] = "Enter your long url here"
    form.elements('input')[0]['_autocomplete'] = "off"
    form.elements('.control-label', replace=None)

    if form.process().accepted:
        if not auth.is_logged_in():
            anon_id = _get_anon_uid()
        else:
            anon_id = None
        update_dict = dict(short_code="TeSt4", created_by_anon=anon_id)
        db(db.url.id == form.vars.id).update(**update_dict)

        # set short link in session and redirect to same page
        # Redirection is done to avoid following browser
        # warnings when page is reloaded or back button is clicked
        # 1. Confirm form resubmission
        # 2. Confirm form resubmission: ERR_CACHE_MISS
        session['short_link'] = "http://urlr.in/" + "TeSt4"
        session.flash = 'Short url created'
        redirect(URL('index'))
    elif form.errors:
        response.flash = ""

    grid = LOAD('default', 'url_grid.load', ajax=True)
    return dict(form=form, grid=grid, short_link=short_link)


def url_grid():
    """
    """
    anon_id = _get_anon_uid()
    # grid variables
    fields = [db.url.long_url, db.url.created_on, db.url.short_code]
    db.url.short_code.readable = True
    db.url.created_on.readable = True
    link = _get_analytics_link()

    if auth.is_logged_in():
        query = (db.url.created_by == auth.user.id)
    elif anon_id:
        query = (db.url.created_by_anon == anon_id)
    else:
        query = (db.url.id == NO_RECORD)

    grid = SQLFORM.grid(query, create=False, editable=False, searchable=False,
                        deletable=True, details=False, csv=False, paginate=10,
                        fields=fields, showbuttontext=False, user_signature=False,
                        _class="web2py_grid url_grid", links=link, maxtextlength=50)
    return dict(grid=grid)


def statistics():
    """
    """
    pass


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


def _get_analytics_link():
    """
    Return QR code link and statistics link.
    """

    link = [lambda row: SPAN(A(SPAN(_class="icon glyphicon glyphicon-qrcode"),
                               _href='javascript:void(0)',
                               _class='button btn btn-default qr_code',
                               _title='QR Code'),
                             A(SPAN(_class="icon glyphicon glyphicon-stats"),
                               _href=URL('default', 'statistics', args=row.id),
                               _class='button btn btn-default statistics',
                               _title='Statistics'))]
    return link


def _get_anon_uid():
    """
    """
    if 'anon_user_uid' in request.cookies:
        return request.cookies['anon_user_uid'].value
#