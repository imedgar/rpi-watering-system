from flask import Flask, render_template, redirect, url_for
import psutil
import datetime
import water
import os

app = Flask(__name__)


def template(title='watering_system', text=''):
    time_string = datetime.datetime.now().strftime("%d %b %Y %H:%M:%S")
    template_date = {
        'title': title,
        'time': time_string,
        'text': text
    }
    return template_date


@app.route('/')
def hello():
    template_data = template()
    return render_template('main.html', **template_data)


@app.route('/clean_gpio')
def clean_gpio():
    water.clean_gpio()
    message = 'Rpi GPIO has been reset!'
    template_data = template(text=message)
    return render_template('main.html', **template_data)


@app.route('/last_watered')
def check_last_watered():
    template_data = template(text=water.get_last_watered(0))
    return render_template('main.html', **template_data)

@app.route('/last_bot')
def check_last_bot():
    template_data = template(text=water.get_last_watered(1))
    return render_template('main.html', **template_data)


@app.route('/sensor')
def action():
    status = water.get_status()
    if status == 0:
        message = 'Water me please!'
    else:
        message = 'I''m a happy plant'

    template_data = template(text=message)
    return render_template('main.html', **template_data)


@app.route('/water')
def action2():
    water.pump_on()
    template_data = template(text='Watered Once')
    return render_template('main.html', **template_data)


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=80, debug=True)
    except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
        water.clean_gpio()  # cleanup all GPI