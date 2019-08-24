from flask import Flask, render_template, redirect, url_for
import datetime
import water

app = Flask('watering-system', static_folder='./templates')


def template(title='watering-system', text='', is_happy=''):
    time_string = datetime.datetime.now().strftime("%d %b %Y %H:%M:%S")
    template_date = {
        'title': title,
        'time': time_string,
        'last_watered': water.get_last_watered(0),
        'auto_watered': water.get_last_watered(1),
        'is_happy': 'red' if water.get_status() == 0 else 'green',
        'text': text
    }
    return template_date


@app.route('/')
def root():
    status = water.get_status()
    if status == 0:
        message = 'Water me please :''('
        is_happy = 'blink-red'
    else:
        message = 'I''m a happy plant :)'
        is_happy = 'blink-green'
    template_data = template(text=message, is_happy=is_happy)
    return render_template('main.html', **template_data)


@app.route('/clean_gpio')
def clean_gpio():
    water.clean_gpio()
    message = 'Rpi GPIO has been reset!'
    template_data = template(text=message)
    return render_template('main.html', **template_data)


@app.route('/sensor')
def action():
    status = water.get_status()
    if status == 0:
        message = 'Water me please :''('
        is_happy = 'blink-red'
    else:
        message = 'I''m a happy plant :)'
        is_happy = 'blink-green'
    template_data = template(text=message, is_happy=is_happy)
    return render_template('main.html', **template_data)


@app.route('/water')
def pump():
    water.pump_on()
    template_data = template(text='Watered Once')
    return render_template('main.html', **template_data)
