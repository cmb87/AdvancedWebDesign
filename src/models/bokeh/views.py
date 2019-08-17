from flask import Flask, render_template, jsonify, request, Blueprint, make_response
from bokeh.plotting import figure, show
from bokeh.models import AjaxDataSource, CustomJS
from bokeh.embed import components
import numpy as np

bokeh_blueprint = Blueprint('bokeh', __name__)


x = list(np.arange(0, 6, 0.1))
y = list(np.sin(x) + np.random.random(len(x)))

@bokeh_blueprint.route('/data', methods=['POST'])
def data():
    x.append(x[-1]+0.1)
    y.append(np.sin(x[-1])+np.random.random())
    #return jsonify(points=list(zip(x,y)))
    return jsonify(x=x, y=y)




@bokeh_blueprint.route('/')
def show_dashboard():

    plots=[]
    plots.append(make_plot_ajax())
    plots.append(make_plot_ajax())
    return render_template('bokeh/plot.html', plots=plots)



def make_plot_ajax():
    source = AjaxDataSource(data_url=request.url_root+'bokeh/data', polling_interval=100)

    p = figure(plot_height=300, plot_width=800, background_fill_color="lightgrey",
               title="Streaming Noisy sin(x) via Ajax")
    p.circle('x', 'y', source=source)

    p.x_range.follow = "end"
    p.x_range.follow_interval = 10
    script, div = components(p)

    return script, div

def make_plot():
    plot = figure(plot_height=300, sizing_mode='scale_width')

    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    y = [2**v for v in x]

    plot.line(x, y, line_width=4)

    script, div = components(plot)
    return script, div