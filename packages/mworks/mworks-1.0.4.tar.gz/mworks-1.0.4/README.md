# mworks

The goal of this project is to remove some boilerplate and add few standard
routes to flask applications.

## Usage

Add common routes to the flask application:

```python
from mworks import CommonRoutes
from flask import Flask

app = Flask(__name__)
mworks = CommonRoutes(app)
```

You can optionally add authorisation for sensitive endpoints:

```python
is_admin = lambda: request.remote_addr == '127.0.0.1'
mworks = CommonRoutes(app, auth_checks=[is_admin])
```

## Features

CommonRoutes has the following endpoints implemented:

- `/healthz` - Always returns HTTP 200, useful for healthchecks
- `/varz` - Get variables for service monitoring. Customizable.
- `/docz` - Read README.md from the application and render it.
- `/logz` - Render logs from the application in the browser.
