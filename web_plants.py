from flask import Flask, render_template, request
import water
from dict_en import dict_en
from sendgrid_utils import send_email

app = Flask('watering-system', static_folder='./templates')
html_template = 'main.html'

moisture = {
    'VW': "blue",
    'W': "green",
    'D': "red",
}

is_happy = 'green'
last_check = water.datetime_now_str()
last_watered = water.datetime_now_str()

def template(title='H.U.E. watering-system', text=''):
    return {
        'title': title,
        'text': text,
        'time': water.datetime_now_str(),
        'is_happy': is_happy,
        'last_watered': dict_en['HUE_watered'].format(last_watered),
        'last_check': dict_en['HUE_checked'].format(last_check),
        'time_diff': dict_en['time_diff'].format(water.time_diff(last_watered)['hours'], water.time_diff(last_watered)['minutes'])
    }


@app.route('/')
def root():
    template_data = template(text=dict_en['not_need_water_msg'])
    return render_template(html_template, **template_data)


@app.route('/clean_gpio')
def clean_gpio():
    water.clean_gpio()
    template_data = template(text=dict_en['gpio_reset_msg'])
    return render_template(html_template, **template_data)


@app.route('/auto_water')
def auto_water():
    global last_watered
    last_watered = water.datetime_now_str()
    send_email(
        'edgaru90@gmail.com',
        'edgaru90@gmail.com',
        'HUE watered your plant',
        'HUE watered your plant @ ' + water.datetime_now_str()
    )
    template_data = template()
    return render_template(html_template, **template_data)


@app.route('/soil')
def soil():
    global is_happy
    status = request.args.get('moisture')
    is_happy = moisture[status]
    global last_check
    last_check = water.datetime_now_str()
    template_data = template(text=dict_en['need_water_msg'] if status == 'D' else dict_en['not_need_water_msg'])
    return render_template(html_template, **template_data)
