from django.db.models import Sum

import pygal
from pygal.style import BlueStyle as Style

from .models import BigFish, Day, Year


DAY_LABELS = [x[1] for x in Day.DAYS]


def _year_compare_data():
    result = []
    for year in Year.objects.all():
        data = []
        for day in year.days.order_by("day"):
            data.append(day.total)
        result.append((str(year), data))
    return result


def year_compare_bar():
    chart = pygal.Bar(style=Style)
    chart.x_labels = DAY_LABELS
    for year, datum in _year_compare_data():
        chart.add(year, datum)
    return chart.render(is_unicode=True)


def year_compare_punchcard():
    chart = pygal.Dot(style=Style)
    chart.x_labels = DAY_LABELS
    for year, datum in _year_compare_data():
        chart.add(year, datum)
    return chart.render(is_unicode=True)


def year_compare_line():
    line_chart = pygal.Line(style=Style)
    years = Year.objects.order_by('year').annotate(
        total_bass=Sum('days__bass'),
        total_crappie=Sum('days__crappie'),
        total_walleye=Sum('days__walleye'),
        total_northern=Sum('days__northern'),
    )
    line_chart.x_labels = [str(y) for y in years]
    line_chart.add('Bass', [y.total_bass for y in years])
    line_chart.add('Crappie', [y.total_crappie for y in years])
    line_chart.add('Northern', [y.total_northern for y in years])
    line_chart.add('Walleye', [y.total_walleye for y in years])
    return line_chart.render(is_unicode=True)


def daily_species_chart(year, chart_type="Dot"):
    chart = {
        "Dot": pygal.Dot,
        "Pie": pygal.Pie,
        "StackedBar": pygal.StackedBar,
    }[chart_type](style=Style)
    chart.x_labels = DAY_LABELS
    bass, crappie, northern, walleye = [], [], [], []
    for day in year.days.order_by("day"):
        bass.append(day.bass)
        crappie.append(day.crappie)
        northern.append(day.northern)
        walleye.append(day.walleye)
    chart.add("Bass", bass)
    chart.add("Crappie", crappie)
    chart.add("Northern", northern)
    chart.add("Walleye", walleye)
    return chart.render(is_unicode=True)


def year_size_scatter(year):
    chart = pygal.XY(
        stroke=False,
        style=Style,
        dots_size=7
    )
    chart.x_label = ["Weight (pounds)"]
    chart.y_label = ["Length (inches)"]
    chart.add("Bass", year.bass)
    chart.add("Northern", year.northern)
    chart.add("Walleye", year.walleye)
    return chart.render(is_unicode=True)


def all_years_scatter():
    fish = BigFish.objects.all()
    chart = pygal.XY(
        stroke=False,
        style=Style,
        dots_size=7,
    )
    chart.x_label = ["Weight (pounds)"]
    chart.y_label = ["Length (inches)"]
    chart.add("Bass", [f.stats for f in fish.filter(species=BigFish.BASS)])
    chart.add("Northern", [f.stats for f in fish.filter(species=BigFish.NORTHERN)])
    chart.add("Walleye", [f.stats for f in fish.filter(species=BigFish.WALLEYE)])
    return chart.render(is_unicode=True)
