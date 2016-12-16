# -*- coding: utf-8 -*-


def index():
    # form = FORM(DIV(TEXTAREA(), SPAN(BUTTON('Shorten url', _class='btn btn-default', _type='submit', _value='submit')), _class=''))
    submit = INPUT(_class="btn btn-primary", _type="Submit", _value="Shorten")

    form = SQLFORM(db.url, buttons=[submit])
    form.elements('input')[0]['_placeholder'] = "Enter your long url here"
    form.elements('.control-label', replace=None)
    if form.process().accepted:
        response.flash = 'form accepted'

    fields = [db.url.long_url, db.url.created_on]
    db.url.created_on.readable = True
    link = _get_analytics_link()
    grid = SQLFORM.grid(db.url.created_by, create=False, editable=False, searchable=False,
                        deletable=True, details=False, csv=False, paginate=10,
                        fields=fields, showbuttontext=False,
                        sorter_icons=(XML('&#x2191;'), XML('&#x2193;')),
                        _class="web2py_grid url_grid", links=link)

    return dict(form=form, grid=grid)


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

