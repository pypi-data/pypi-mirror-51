# Flask-Statsd

Generate and send Flask metrics in [Graphite Carbon Format](http://graphite.wikidot.com/carbon) format.


# Install
```bash
pip install flask-carbon-statsd

# Latest Code

pip install git+https://github.com/labeneator/flask_carbon_statsd.git
```


# Usage Example
```python
# myapp.py
from flask import Flask, Blueprint
from flask_carbon_statsd import FlaskCarbonStatsdTimerCounter

flask_metrics = FlaskCarbonStatsdTimerCounter(host='localhost', port=8125)


app = Flask(__name__)
flask_metrics.init_app(app)

# or
flask_metrics = FlaskCarbonStatsd(app=app, host='localhost', port=8125)

bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard')
def index(device):
    return 'OK'

app.register_blueprint(bp)
```

* Request `/dashboard` with  FlaskCarbonStatsdTimer

    ```
    flask.carbon.statsd.dev.flask_template.app.local.LocalHost-3.dashboard.index.200:3.650904|ms
    ```

* Request `/dashboard` with  FlaskCarbonStatsdTimerCounter

    ```
    flask.carbon.statsd.dev.flask_template.app.local.LocalHost-3.dashboard.index.200:3.650904|ms
    flask.carbon.statsd.dev.flask_template.app.local.LocalHost-3.dashboard.index.200:1|c
    ```
