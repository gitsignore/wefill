from __future__ import print_function
from __future__ import print_function
import locale
from django import template
from datetime import date
from itertools import groupby
import datetime
import calendar

register = template.Library()


DAY_SCHEDULES = (
    '09:00 - 10:00',
    '10:00 - 11:00',
    '11:00 - 12:00',
    '12:00 - 13:00',
    '13:00 - 14:00',
    '14:00 - 15:00',
    '15:00 - 16:00',
    '16:00 - 17:00',
    '17:00 - 18:00',
    '18:00 - 19:00',
    '19:00 - 20:00',
    '20:00 - 21:00',
)


def do_events(parser, token):
    """
    The template tag's syntax is {% event_calendar year month event_list %}
    """
    # Force French locale
    locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
    try:
        tag_name, year, month, event_list = token.split_contents()
    except ValueError:
        raise Exception("tag requires three arguments")
    return EventCalendarNode(year, month, event_list)


class EventCalendarNode(template.Node):
    """
    Process a particular node in the template. Fail silently.
    """

    def __init__(self, year, month, event_list):
        try:
            self.year = template.Variable(year)
            self.month = template.Variable(month)
            self.event_list = template.Variable(event_list)
        except ValueError:
            raise template.TemplateSyntaxError

    def render(self, context):
        try:
            # Get the variables from the context so the method is thread-safe.
            my_event_list = self.event_list.resolve(context)
            my_year = self.year.resolve(context)
            my_month = self.month.resolve(context)
            events = self.group_by_day(my_event_list)
            num_days = calendar.monthrange(my_year, my_month)[1]
            days = [datetime.date(my_year, my_month, day) for day in range(1, num_days + 1)]
            body = ''

            for day in days:
                day_events = list()
                if str(day) in events:
                    for event in events[str(day)]:
                        day_events.append(event)
                body += self.formatday(str(day), day_events)

            return body
        except ValueError:
            return
        except template.VariableDoesNotExist:
            return

    def formatday(self, full_date, events):
        day = full_date[-2:]
        today = date.today()
        if str(today)[-2:] == day:
            display = 'show'
        else:
            display = 'hide'
        if day != 0:
            body = '<div class="list-group {0} {2}" data-src={1}>'.format(day, full_date, display)
            for schedule in DAY_SCHEDULES:
                if events:
                    for key, event in enumerate(events):
                        if schedule[:2] != event['date_refill'][11:13]:
                            body += '<button type="button" class="list-group-item" data-src={0}>{1}</button>'.format(
                                schedule[:5],
                                schedule,
                            )
                            break
                        else:
                            del events[key]
                            break
                else:
                    body += '<button type="button" class="list-group-item" data-src={0}>{1}</button>'.format(schedule[:5], schedule)
            body += '</div>'

            return body
        return

    def group_by_day(self, events):
        groups = {}
        events = sorted(events, key=lambda x: x['date_refill'])

        for key, group in groupby(events, lambda x: x['date_refill'][:10]):
            list_of = []
            for thing in group:
                list_of.append(thing)
            groups.update({key: list_of})

        return groups

# Register the template tag so it is available to templates
register.tag("events", do_events)
