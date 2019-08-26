from flask import Flask, render_template, redirect, url_for
from datetime import datetime
import water
from dict_en import dict_en

app = Flask('watering-system', static_folder='./templates')
html_template = 'main.html'
happy = 'green'
not_happy = 'red'


def template(title='watering-system', text=''):
    return {
        'title': title,
        'text': text,
        'time': water.datetime_now_str(),
        'is_happy': not_happy if water.get_status() == 0 else happy,
        'auto_watered': water.read_file(1),
        'last_watered': water.read_file(0) + ' ' + dict_en['time_since'].format(
            water.time_diff()['hours'],
            water.time_diff()['minutes'])
    }


@app.route('/')
def root():
    template_data = template(
        text=dict_en['need_water_msg'] if water.get_status() == 0
        else dict_en['not_need_water_msg'])
    return render_template(html_template, **template_data)


@app.route('/clean_gpio')
def clean_gpio():
    water.clean_gpio()
    template_data = template(text=dict_en['gpio_reset_msg'])
    return render_template(html_template, **template_data)


@app.route('/water')
def pump():
    water.pump_on()
    template_data = template(text=dict_en['watered_msg'])
    return render_template(html_template, **template_data)
