from flask import Flask, render_template
import water
from dict_en import dict_en

app = Flask('watering-system', static_folder='./templates')
html_template = 'main.html'


def template(title='H.U.E. watering-system', text=''):
    return {
        'title': title,
        'text': text,
        'time': water.datetime_now_str(),
        'is_happy': 'red' if water.get_status() == 0 else 'green',
        'auto_watered': water.read_file(1),
        'last_watered': dict_en['watered_at'].format(
            water.read_file(0), water.time_diff()['hours'], water.time_diff()['minutes'])
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
    watered = water.pump_on()
    template_data = template(text=dict_en['pump_msg'] if watered == 0 else dict_en['not_pump_msg'])
    return render_template(html_template, **template_data)
