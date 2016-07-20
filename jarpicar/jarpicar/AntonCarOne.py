#!/usr/bin/python
# -*- coding: utf-8 -*-

# imports, globals
# --------------------------------------------------------------

import l298nBoard
import time

Steer = None
Engine = None

from flask import Flask, render_template, flash, session, Response, redirect, url_for
import os
from camera_pi import Camera

app = Flask(__name__)
app.secret_key = os.urandom(24)

sessionlog = []
template_dict = {}
template_dict['sessionlog'] = sessionlog


# user exeptions
# --------------------------------------------------------------


# classes, defs
# --------------------------------------------------------------

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# flask routes
# --------------------------------------------------------------
@app.route('/')
def index():
    global template_dict
    if 'uuid' in session:
        return redirect(url_for('controller'))
    else:
        return render_template('index.html', data=template_dict)

@app.route('/controller')
def controller():
    global template_dict
    if 'uuid' in session:
        #flash('Engines already started...')
        #template_dict['sessionlog'].append(['Engines already started...',time.strftime("%Y-%m-%d %H:%M:%S")])
        return render_template('controller.html', data=template_dict)
    else:
        flash('Session lost....')
        template_dict['sessionlog'].append(['Session lost....',time.strftime("%Y-%m-%d %H:%M:%S")])
        return redirect(url_for('index'))


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# nav panel
@app.route('/startsession')
def startsession():
    global Steer 
    global Engine 
    global template_dict

    if 'uuid' in session:
        flash('Engines already started...')
        return redirect(url_for('controller'))
    
    else:
        Steer = l298nBoard.Motor("steering",16,20)
        Engine = l298nBoard.PWMMotor("engine",17,27,4,100)

        if Steer.Initialized and Engine.Initialized:
            session['uuid'] = os.urandom(12)
            
            del template_dict['sessionlog'][:]
            flash('Session started: ')
            template_dict['sessionlog'].append(['Session started: ',time.strftime("%Y-%m-%d %H:%M:%S")])
            flash(Steer.Log)
            template_dict['sessionlog'].append([Steer.Log,time.strftime("%Y-%m-%d %H:%M:%S")])
            flash(Engine.Log)
            template_dict['sessionlog'].append([Engine.Log,time.strftime("%Y-%m-%d %H:%M:%S")])
            return redirect(url_for('controller'))
        else:
            session.pop('uuid', None)   
            flash('Could not start my Engines...')
            return render_template('index.html', data=template_dict)


@app.route('/stopsession')
def stopsession():
    
    global Steer
    global Engine
    global template_dict

    if Steer is not None:
        del Steer
        Steer = None
    if Engine is not None:
        del Engine
        Engine = None

    session.pop('uuid', None)

    flash('Engines out...')
    template_dict['sessionlog'].append(['Engines out...',time.strftime("%Y-%m-%d %H:%M:%S")])
    return redirect(url_for('index'))

@app.route('/log')
def logentries():
    global template_dict
    global Steer
    global Engine

    if not template_dict['sessionlog']:
        flash('there are no log entries available...')        
        return redirect(url_for('index'))
    else:
        if 'uuid' in session:
            Engine.stop()
            Steer.stop()
            flash(Engine.Log + ' / ' + Steer.Log)
            template_dict['sessionlog'].append([Engine.Log + ' / ' + Steer.Log,time.strftime("%Y-%m-%d %H:%M:%S")])
            flash('Session paused for log...')
            template_dict['sessionlog'].append(['Session paused for log...',time.strftime("%Y-%m-%d %H:%M:%S")])      
        
        return render_template('log.html', data=template_dict)

# left panel
@app.route('/forward')
def forward():
    global Steer
    global Engine
    global template_dict
    Engine.forward()
    flash(Engine.Log)
    template_dict['sessionlog'].append([Engine.Log,time.strftime("%Y-%m-%d %H:%M:%S")])
    Engine.fullspeed()
    flash(Engine.Log)
    template_dict['sessionlog'].append([Engine.Log,time.strftime("%Y-%m-%d %H:%M:%S")])
    return redirect(url_for('controller'))

@app.route('/back')
def backward():
    global Steer
    global Engine
    global template_dict
    Engine.backward()
    Engine.halfspeed()
    flash(Engine.Log)
    template_dict['sessionlog'].append([Engine.Log,time.strftime("%Y-%m-%d %H:%M:%S")])
    return redirect(url_for('controller'))

@app.route('/stop')
def stop():
    global Steer
    global Engine
    global template_dict
    Engine.stop()
    Steer.stop()
    flash(Engine.Log + ' / ' + Steer.Log)
    template_dict['sessionlog'].append([Engine.Log + ' / ' + Steer.Log,time.strftime("%Y-%m-%d %H:%M:%S")])
    return redirect(url_for('controller'))

# right panel
@app.route('/right')
def right():
    global Steer
    global Engine
    global template_dict
    Steer.backward()
    flash(Steer.Log)
    template_dict['sessionlog'].append([Steer.Log,time.strftime("%Y-%m-%d %H:%M:%S")])
    return redirect(url_for('controller'))

@app.route('/left')
def left():
    global Steer
    global Engine
    global template_dict
    Steer.forward()
    flash(Steer.Log)
    template_dict['sessionlog'].append([Steer.Log,time.strftime("%Y-%m-%d %H:%M:%S")])
    return redirect(url_for('controller'))

@app.route('/ahead')
def ahead():
    global Steer
    global Engine
    global template_dict
    Steer.stop()
    flash(Steer.Log)
    template_dict['sessionlog'].append([Steer.Log,time.strftime("%Y-%m-%d %H:%M:%S")])
    return redirect(url_for('controller'))

@app.route('/rightforward')
def rightforward():
    global Steer
    global Engine
    global template_dict
    Steer.backward()
    Engine.forward()
    Engine.halfspeed()
    flash(Engine.Log + ' / ' + Steer.Log)
    template_dict['sessionlog'].append([Engine.Log + ' / ' + Steer.Log,time.strftime("%Y-%m-%d %H:%M:%S")])
    return redirect(url_for('controller'))

@app.route('/leftforward')
def leftforward():
    global Steer
    global Engine
    global template_dict
    Steer.forward()
    Engine.forward()
    Engine.halfspeed()
    flash(Engine.Log + ' / ' + Steer.Log)
    template_dict['sessionlog'].append([Engine.Log + ' / ' + Steer.Log,time.strftime("%Y-%m-%d %H:%M:%S")])
    return redirect(url_for('controller'))

@app.route('/rightbackward')
def rightbackward():
    global Steer
    global Engine
    global template_dict
    Steer.forward()
    Engine.backward()
    Engine.halfspeed()
    flash(Engine.Log + ' / ' + Steer.Log)
    template_dict['sessionlog'].append([Engine.Log + ' / ' + Steer.Log,time.strftime("%Y-%m-%d %H:%M:%S")])
    return redirect(url_for('controller'))

@app.route('/leftbackward')
def leftbackward():
    global Steer
    global Engine
    global template_dict
    Steer.backward()
    Engine.backward()
    Engine.halfspeed()
    flash(Engine.Log + ' / ' + Steer.Log)
    template_dict['sessionlog'].append([Engine.Log + ' / ' + Steer.Log,time.strftime("%Y-%m-%d %H:%M:%S")])
    return redirect(url_for('controller'))

# Main
# --------------------------------------------------------------
def main():
    app.run(host='0.0.0.0', debug=True, threaded=True)

if __name__ == "__main__":
    main()

# EOF
# --------------------------------------------------------------

