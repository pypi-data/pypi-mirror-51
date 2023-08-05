"""
Utils
-----

Helper functions.
"""

from .. import MessageFactory as _
from decorator import decorator
from email.Header import Header
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from euphorie.client import model
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.content.utils import StripMarkup
from five import grok
from json import dumps
from PIL.ImageColor import getrgb
from plone import api
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from Products.CMFCore.utils import getToolByName
from sqlalchemy import sql
from z3c.saconfig import Session
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface

import colorsys
import email.Utils as emailutils
import htmllib
import logging
import random
import simplejson
import threading


locals = threading.local()
log = logging.getLogger(__name__)

grok.templatedir('templates')
pl_message = MessageFactory('plonelocales')


def setRequest(request):
    locals.request = request


def getRequest():
    return getattr(locals, 'request', None)


def getSecret():
    try:
        site = api.portal.get()
    except api.exc.CannotGetPortalError:
        site = None
    return getattr(site, 'euphorie_secret', 'secret')


def randomString(length=16):
    """Return 32 bytes of random data. Only characters which do not require
    special escaping in HTML or URLs are generated."""
    safe_characters = (
        'abcdefghijklmnopqrstuvwxyz'
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        '1234567890-'
    )
    return ''.join(random.choice(safe_characters) for idx in range(length))


@decorator
def jsonify(func, *args, **kwargs):
    request = getattr(args[0], "request")
    request.response.setHeader("Content-Type", "application/json")
    data = func(*args, **kwargs)
    return simplejson.dumps(data)


def get_translated_custom_risks_title(request):
    lang = getattr(request, 'LANGUAGE', 'en')
    if "-" in lang:
        elems = lang.split("-")
        lang = "{0}_{1}".format(elems[0], elems[1].upper())
    title = translate(_(
        'title_other_risks', default=u'Added risks (by you)'),
        target_language=lang)
    return title


def HasText(html):
    """Determine if a HTML fragment contains text.
    """
    if not html:
        return False
    text = StripMarkup(html).replace(' ', '').replace('&nbsp;', '')
    return bool(text)


def CreateEmailTo(sender_name, sender_email, recipient, subject, body):
    mail = MIMEMultipart('alternative')
    mail['From'] = emailutils.formataddr((sender_name, sender_email))
    mail['To'] = recipient
    mail['Subject'] = Header(subject.encode('utf-8'), 'utf-8')
    mail['Message-Id'] = emailutils.make_msgid()
    mail['Date'] = emailutils.formatdate(localtime=True)
    mail.set_param('charset', 'utf-8')
    if isinstance(body, unicode):
        mail.attach(MIMEText(body.encode('utf-8'), 'plain', 'utf-8'))
    else:
        mail.attach(MIMEText(body))

    return mail


def setLanguage(request, context, lang=None):
    """Switch Plone to another language. If no language is given via the
    `lang` parameter the language is taken from a `language`
    request parameter. If a dialect was chosen but is not available the main
    language is used instead. If the main language is also unavailable switch
    back to English.
    """
    if lang is None:
        lang = request.form.get('language')
    if not lang:
        return

    lang = lang.lower()
    lt = getToolByName(context, 'portal_languages')
    res = lt.setLanguageCookie(lang=lang, request=request)
    if res is None and '-' in lang:
        lang = lang.split('-')[0]
        res = lt.setLanguageCookie(lang=lang, request=request)
        if res is None:
            log.warn('Failed to switch language to %s', lang)
            lt.setLanguageCookie(lang='en', request=request)
            lang = 'en'

    # In addition to setting the cookie also update the PTS language.
    # This effectively switches Plone over to the new language without
    # requiring a new HTTP request.
    request['LANGUAGE'] = lang
    binding = request.get('LANGUAGE_TOOL', None)
    if binding is not None:
        binding.LANGUAGE = lang


def RelativePath(start, end):
    """Determine the relative path between two items in the ZODB."""
    if start is end:
        return ''

    start = start.getPhysicalPath()
    end = end.getPhysicalPath()
    while start and end and start[0] == end[0]:
        start = start[1:]
        end = end[1:]

    if start:
        return '%s/%s' % ('/'.join(len(start) * ['..']), '/'.join(end))
    else:
        return '/'.join(end)


def MatchColour(colour, low_l=0.2, high_l=0.65, s_factor=1):
    """Determine a colour that contrasts with a given colour. The resulting
    colour pair can be used as foreground and background, guaranteeing
    readable text.

    The match colour is determined by flipping the luminisoty to 10% or 90%,
    while keeping the hue and saturation stable. The only exception are
    yellowish colours, for those the luminosity is always set to 10%.
    """
    (r, g, b) = getrgb(colour)
    (h, l, s) = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    if 0.16 < h < 0.33:
        l = low_l
    elif l > 0.49:
        l = low_l
    else:
        l = high_l
    s *= s_factor
    (r, g, b) = colorsys.hls_to_rgb(h, l, s)
    return '#%02x%02x%02x' % (r * 255, g * 255, b * 255)


def IsBright(colour):
    """Check if a (RGB) colour is a bright colour."""
    (r, g, b) = getrgb(colour)
    (h, l, s) = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    return l > 0.50


class I18nJSONView(grok.View):
    """ Provide the translated month and weekday names for pat-datepicker
    """
    grok.context(Interface)
    grok.layer(IClientSkinLayer)
    grok.name('date-picker-i18n.json')

    def render(self):
        lang = getattr(self.request, 'LANGUAGE', 'en')
        if "-" in lang:
            lang = lang.split("-")[0]
        json = dumps({
            "months": [
                translate(
                    pl_message(month),
                    target_language=lang) for month in [
                        "month_jan",
                        "month_feb",
                        "month_mar",
                        "month_apr",
                        "month_may",
                        "month_jun",
                        "month_jul",
                        "month_aug",
                        "month_sep",
                        "month_oct",
                        "month_nov",
                        "month_dec",
                ]
            ],
            "weekdays": [
                translate(
                    pl_message(weekday),
                    target_language=lang) for weekday in [
                        "weekday_sun",
                        "weekday_mon",
                        "weekday_tue",
                        "weekday_wed",
                        "weekday_thu",
                        "weekday_fri",
                        "weekday_sat",
                ]
            ],
            "weekdaysShort": [
                translate(
                    pl_message(weekday_abbr),
                    target_language=lang) for weekday_abbr in [
                        "weekday_sun_abbr",
                        "weekday_mon_abbr",
                        "weekday_tue_abbr",
                        "weekday_wed_abbr",
                        "weekday_thu_abbr",
                        "weekday_fri_abbr",
                        "weekday_sat_abbr",
                ]
            ],
        })

        return json


class DefaultIntroduction(grok.View):
    """
        Browser view that displays the default introduction text for a Suvey.
        It is used when the Survey does not define its own introduction
    """
    grok.context(Interface)
    grok.layer(IClientSkinLayer)
    grok.name('default_introduction')
    grok.template('default_introduction')


class ContentDefaultIntroduction(grok.View):
    """
        Browser view that displays the default introduction text for a Suvey.
        It is used when the Survey does not define its own introduction
    """
    grok.context(Interface)
    grok.layer(NuPloneSkin)
    grok.name('default_introduction')
    grok.template('default_introduction')


def html_unescape(s):
    p = htmllib.HTMLParser(None)
    p.save_bgn()
    p.feed(s)
    return p.save_end()


def remove_empty_modules(nodes):
    """ Takes a list of modules and risks.

        Removes modules that don't have any risks in them.
        Modules with submodules (with risks) must however be kept.

        How it works:
        -------------
        Use the 'grow' method to create a tree datastructure that
        mirrors the actual layout of modules and risks.

        Then 'prune' it by removing all branches that end in modules.

        Lastly flatten the tree back into a list and use it to filter the
        original list.
    """
    tree = {}
    ids = []

    def grow(tree, nodes):
        for i in range(0, len(nodes)):
            node = nodes[i]
            inserted = False
            for k in tree.keys():
                if node.path.startswith(k[0]):
                    if tree[k]:
                        grow(tree[k], [node])
                    else:
                        tree[k] = {(node.path, node.type, node.id): {}}
                    inserted = True
                    break
            if not inserted:
                tree[(node.path, node.type, node.id)] = {}

    def prune(tree):
        for k in tree.keys():
            if tree[k]:
                prune(tree[k])

            if not tree[k] and k[1] == 'module':
                del tree[k]

    def flatten(tree):
        for k in tree.keys():
            ids.append(k[2])
            flatten(tree[k])

    grow(tree, nodes)
    prune(tree)
    flatten(tree)
    return [n for n in nodes if n.id in ids]


def get_unactioned_nodes(ls, filter_for_measures=False):
    """ Takes a list of modules and risks and removes all risks that have been
        actioned (i.e has at least one valid action plan).
        Also remove all modules that have lost all their risks in the process

        See https://syslab.com/proj/issues/2885
    """
    unactioned = []
    for n in ls:
        if n.type == 'module':
            unactioned.append(n)

        elif n.type == 'risk':
            if not n.action_plans:
                if filter_for_measures:
                    if getattr(n, "existing_measures", None):
                        unactioned.append(n)
                else:
                    unactioned.append(n)
            else:
                # It's possible that there is an action plan object, but
                # that it's not yet fully populated
                if n.action_plans[0] is None or \
                        n.action_plans[0].action_plan is None:
                    unactioned.append(n)

    return remove_empty_modules(unactioned)


def get_actioned_nodes(ls):
    """ Takes a list of modules and risks and removes all risks that are *not*
        actioned (i.e does not have at least one valid action plan)
        Also remove all modules that have lost all their risks in the process.

        See https://syslab.com/proj/issues/2885
    """
    actioned = []
    for n in ls:
        if n.type == 'module':
            actioned.append(n)

        if n.type == 'risk' and len(n.action_plans):
                # It's possible that there is an action plan object, but
                # it's not yet fully populated
                plans = [p.action_plan for p in n.action_plans]
                if plans[0] is not None:
                    actioned.append(n)

    return remove_empty_modules(actioned)


def get_unanswered_nodes(session):
    query = Session().query(model.SurveyTreeItem)\
        .filter(
            sql.and_(
                model.SurveyTreeItem.session == session,
                sql.or_(
                    model.MODULE_WITH_UNANSWERED_RISKS_FILTER,
                    model.UNANSWERED_RISKS_FILTER),
                sql.not_(model.SKIPPED_PARENTS)))\
        .order_by(model.SurveyTreeItem.path)
    return query.all()


def get_risk_not_present_nodes(session):
    query = Session().query(model.SurveyTreeItem)\
        .filter(
            sql.and_(
                model.SurveyTreeItem.session == session,
                sql.or_(
                    model.SKIPPED_PARENTS,
                    model.MODULE_WITH_RISKS_NOT_PRESENT_FILTER,
                    model.RISK_NOT_PRESENT_FILTER,
                    model.SKIPPED_MODULE,
                )))\
        .order_by(model.SurveyTreeItem.path)
    return query.all()


def get_italian_risk_not_present_nodes(session):
    query = Session().query(model.SurveyTreeItem)\
        .filter(
            sql.and_(
                model.SurveyTreeItem.session == session,
                sql.or_(
                    model.SKIPPED_PARENTS,
                    model.MODULE_WITH_RISKS_NOT_PRESENT_FILTER,
                    model.SKIPPED_MODULE,
                    model.UNANSWERED_RISKS_FILTER,
                )))\
        .order_by(model.SurveyTreeItem.path)
    return query.all()
