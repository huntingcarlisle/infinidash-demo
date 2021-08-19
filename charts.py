from io import BytesIO
from flask.helpers import make_response
import matplotlib
from matplotlib.image import BboxImage
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random
import pandas as pd
from flask import send_file

plt.style.use('dark_background')
plt.style.use('seaborn-dark-palette')

chart_df = pd.read_csv('./data/marvel_spotify_clean.csv')

categorical_columns = chart_df.select_dtypes(exclude='number').columns
numeric_columns = chart_df.select_dtypes(include='number').columns
chart_types = ['line','bar','barh','hist','box','kde','area','pie', 'scatter']

def add_line_breaks(title: str):
    splits = title.split(' ')
    orig_len = len(splits)
    for i in range(orig_len):
        if i % (orig_len // 2) == 0:
            splits = splits[:i] + ['\n'] + splits[i:]
    return ' '.join(splits)

def random_agg(exclude: list = None):
    exclude = exclude or []
    aggs = [agg for agg in ['count', 'min', 'max', 'mean', 'median', 'sum'] if agg not in exclude]
    return random.choice(aggs)

def get_bar():
    plt.figure()
    chart_choice = 'bar'
    x_choice = random.choice(categorical_columns)
    filter_choice = random.choice(['Appearance', 'Superhero'])
    y_choice = list(set([random.choice([col for col in numeric_columns if filter_choice not in col]) for _ in range(random.randint(1, 2))]))
    my_agg = random_agg(exclude=['count'])
    plot_df = chart_df.groupby(x_choice).aggregate(func=my_agg)[y_choice]

    while len(set(plot_df[y_choice[0]])) <= 1:
        x_choice = random.choice(categorical_columns)
        y_choice = list(set([random.choice([col for col in numeric_columns if filter_choice not in col]) for _ in range(random.randint(1, 2))]))
        my_agg = random_agg(exclude=['count'])
        plot_df = chart_df.groupby(x_choice).aggregate(func=my_agg)[y_choice]

    if len(y_choice) > 1:
        stacked = random.choice([True, False])
    else:
        stacked = False

    if len(plot_df) > 15:
        plot_df = plot_df.sample(n=15).sort_index()

    chart = plot_df.plot(
        kind=chart_choice,
        rot=90 if len(plot_df) > 4 else 0,
        stacked=stacked,
        grid=False,
    )
    plt.title(add_line_breaks(f'{chart_choice.title()}: {x_choice} v. {", ".join(y_choice)}'))
    plt.xlabel(x_choice, wrap=True)
    plt.ylabel(add_line_breaks(f'{", ".join(y_choice)} \n ({my_agg.title()})'))
    
    return chart.get_figure()

def get_barh():
    plt.figure()
    chart_choice = 'barh'
    x_choice = random.choice(categorical_columns)
    y_choice = random.choice(numeric_columns)
    my_agg = random_agg()
    plot_df = chart_df.groupby(x_choice).aggregate(func=my_agg)[y_choice]
    if len(plot_df) > 15:
        plot_df = plot_df.sample(n=15).sort_index()

    chart = plot_df.plot(
        kind=chart_choice,
        legend=False,
        grid=False
    )
    plt.title(add_line_breaks(f'Horizontal Bar: {x_choice} v. {y_choice}'))
    plt.ylabel(x_choice, wrap=True)
    plt.xlabel(add_line_breaks(f'{y_choice} \n ({my_agg.title()})'))
    
    return chart.get_figure()

def get_line():
    plt.figure()
    chart_choice = 'line'
    x_choice = 'Superhero First Appearance Date'
    filter_choice = random.choice(['Appearance', 'Superhero'])
    selected_columns = list(set([random.choice([col for col in numeric_columns if filter_choice not in col]) for _ in range(random.randint(1, 2))]))
    if len(selected_columns) == 2:
        secondary_y = random.choice([True, False])
    else:
        secondary_y = False
    my_agg = random_agg()
    plot_df = chart_df.groupby(x_choice).aggregate(func=my_agg)[selected_columns]
    if len(plot_df) > 15:
        plot_df = plot_df.sample(n=15).sort_index()

    if secondary_y:
        chart = plot_df.plot(
            kind=chart_choice,
            rot=90 if len(plot_df) > 4 else 0,
            secondary_y=selected_columns[1],
            grid=False
        )
        chart.set_ylabel(f'{add_line_breaks(selected_columns[0])} \n ({my_agg.title()})')
        chart.right_ax.set_ylabel(f'{add_line_breaks(selected_columns[1])} \n ({my_agg.title()})')
        chart.set_title(add_line_breaks(f'{chart_choice.title()}: {x_choice} v. {", ".join(selected_columns)}'))
        chart.set_xlabel(x_choice, wrap=True)
        if len(selected_columns) > 1:
            chart.legend(loc='upper left')
    else:
        chart = plot_df.plot(
            kind=chart_choice,
            rot=90 if len(plot_df) > 4 else 0,
            grid=False
        )
        plt.ylabel(add_line_breaks(f'{", ".join(selected_columns)} \n ({my_agg.title()})'))

        plt.title(add_line_breaks(f'{chart_choice.title()}: {x_choice} v. {", ".join(selected_columns)}'))
        plt.xlabel(x_choice, wrap=True)
        if len(selected_columns) > 1:
            plt.legend(loc='upper left')

    return chart.get_figure()

def get_hist():
    plt.figure()
    chart_choice = 'hist'
    y_choice = random.choice(numeric_columns)
    plot_df = chart_df[[y_choice]]
    chart = plot_df.plot(
        kind=chart_choice,
        bins=random.randint(8,50),
        grid=False
    )
    plt.title(add_line_breaks(f'{chart_choice.title()}ogram: {y_choice}'))
    plt.xlabel(y_choice, wrap=True)
    plt.ylabel('Frequency')

    return chart.get_figure()    

def get_box():
    # TODO: Fix label length
    plt.figure()
    chart_choice = 'box'
    selected_columns = list(set([random.choice(numeric_columns) for _ in range(random.randint(2,6))]))
    plot_df = chart_df[selected_columns]

    chart = plot_df.plot(
        kind=chart_choice,
        rot=90 if len(plot_df) > 4 else 0,
        logy=True,
        grid=False
    )
    plt.title(add_line_breaks(f'{chart_choice.title()}: {", ".join(selected_columns)}'))
    plt.ylabel('Value')
    
    return chart.get_figure()

def get_kde():
    plt.figure()
    chart_choice = 'kde'
    filter_choice = random.choice(['Appearance', 'Superhero'])
    selected_columns = list(set([random.choice([col for col in numeric_columns if filter_choice not in col]) for _ in range(random.randint(1, 2))]))
    plot_df = chart_df[selected_columns]

    chart = plot_df.plot(
        kind=chart_choice,
        rot=90 if len(plot_df) > 4 else 0,
        grid=False
    )
    plt.title(add_line_breaks(f'Kernel Density Estimation: {", ".join(selected_columns)}'))
    if len(selected_columns) > 1:
        plt.legend(loc='upper left')
    
    return chart.get_figure()

def get_area():
    plt.figure()
    chart_choice = 'area'
    x_choice = 'Superhero First Appearance Date'
    y_choice = list(set([random.choice(numeric_columns) for _ in range(random.randint(2,4))]))
    my_agg = random_agg()
    plot_df = chart_df.groupby(x_choice).aggregate(func=my_agg)[y_choice]
    if len(plot_df) > 15:
        plot_df = plot_df.sample(n=15).sort_index()

    chart = plot_df.plot(
        kind=chart_choice,
        rot=90 if len(plot_df) > 4 else 0,
        legend=False,
        grid=False
    )
    plt.title(add_line_breaks(f'{chart_choice.title()}: {", ".join(y_choice)}'))
    plt.xlabel(x_choice, wrap=True)
    plt.ylabel(f'{add_line_breaks(", ".join(y_choice))} \n ({my_agg.title()})')
    
    return chart.get_figure()

def get_pie():
    plt.figure()
    chart_choice = 'pie'
    x_choice = random.choice(categorical_columns)
    y_choice = random.choice(numeric_columns)
    while 'Superhero' not in y_choice:
        y_choice = random.choice(numeric_columns)

    my_agg = random_agg(exclude=['count', 'sum'])
    plot_df = chart_df.groupby(x_choice).aggregate(func=my_agg)[y_choice]
    if len(plot_df) > 15:
        plot_df = plot_df.sample(n=15).sort_index()


    chart = plot_df.plot(
        kind=chart_choice,
        grid=False
    )
    plt.title(add_line_breaks(f'{chart_choice.title()}: {my_agg.title()} {y_choice} for {x_choice}'))
    plt.xlabel(x_choice, wrap=True)
    plt.ylabel(f'{y_choice} \n ({my_agg.title()})')
    
    return chart.get_figure()

def get_scatter():
    plt.figure()
    chart_choice = 'scatter'
    x_choice = random.choice(numeric_columns)
    while ('Superhero' not in x_choice):
        x_choice = random.choice(numeric_columns)

    y_choice = random.choice(numeric_columns)
    while ('Superhero' not in y_choice):
        y_choice = random.choice(numeric_columns)

    if random.randint(0,1):
        c_choice = random.choice(numeric_columns)
    else:
        c_choice = None

    chart = chart_df.plot(
        x=x_choice,
        y=y_choice,
        c=c_choice,
        kind=chart_choice,
        grid=False
    )

    plt.title(add_line_breaks(f'{chart_choice.title()}: {x_choice} v. {y_choice} {("- Colored by " + c_choice) if c_choice else ""}'))
    plt.xlabel(x_choice, wrap=True)
    plt.ylabel(f'{y_choice}')

    return chart.get_figure()

def get_chart(chart_choice: str) -> None:
    chart_funcs = {
        'bar': get_bar,
        'barh': get_barh,
        'line': get_line,
        'hist': get_hist,
        'box': get_box,
        'kde': get_kde,
        'area': get_area,
        'pie': get_pie,
        'scatter': get_scatter,
    }
    
    return chart_funcs[chart_choice]()

def try_get_chart(chart_choice):
    try:
        chart = get_chart(chart_choice)
    except Exception as e:
        print(f'Failed - {chart_choice}: {e}')
        chart = None
        successful = False
    else:
        successful = True
        plt.close('all')
    return chart, successful

def get_random_chart(chart_choice=None):
    chart_choice = random.choice(chart_types) if chart_choice is None else chart_choice
    successful = False
    while not successful:
        chart, successful = try_get_chart(chart_choice) 
    return chart   

import base64
from flask import jsonify

def serve_chart():
    chart = get_random_chart()
    img_io = BytesIO()
    chart.savefig(img_io, format='PNG', bbox_inches="tight")
    # plt.close(chart)
    data64 = base64.b64encode(img_io.getvalue())
    data = {'message': u'data:img/jpeg;base64,'+data64.decode('utf-8')}
    return data