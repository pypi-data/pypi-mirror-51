### WWIDGET
This package is to fast embed html snippets  to any web application

#### WWIDGET Usage
```
from wwidget.login.login import LoginWidget

tpl = LoginWidget(
    template='a_login.html',
    username={
        'required': True,
        'id': 'username'
    },
    password={
        'required': True
    },
    button={
        'value': 'Sign in'
    },
    form_attrs={}
)

tpl.output
```

#### Options
- form_attrs: supports any attributes
- action: if not set empty url is taken as default
- method: if not set POST is taken as default
- username, password: as a dictionary holding required, id, class
- button: as a dictionary holding value, type, class, id, name, style
