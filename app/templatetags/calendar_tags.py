from __future__ import print_function
from __future__ import print_function
import locale
from calendar import HTMLCalendar
from django import template
from datetime import date, timedelta


register = template.Library()


def do_calendar(parser, token):
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
            my_year = self.year.resolve(context)
            my_month = self.month.resolve(context)
            cal = EventCalendar()
            return cal.formatmonth(int(my_year), int(my_month))
        except ValueError:
            return
        except template.VariableDoesNotExist:
            return


class EventCalendar(HTMLCalendar):
    """
    Overload Python's calendar.HTMLCalendar to add the appropriate events to
    each day's table cell.
    """

    def __init__(self):
        super(EventCalendar, self).__init__()

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            cssclass += ' day'
            if date.today() == date(self.year, self.month, day):
                cssclass = 'noday today'
            if (date.today() + timedelta(days=1)) == date(self.year, self.month, day):
                cssclass += ' active'
            if date.today() > date(self.year, self.month, day):
                cssclass = 'noday'
            return self.day_cell(cssclass, '<span class="dayNumberNoEvents">%d</span>' % (day))
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(EventCalendar, self).formatmonth(year, month)

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

# Register the template tag so it is available to templates
register.tag("calendar", do_calendar)
