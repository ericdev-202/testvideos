# django-static-jquery-ui


Django application contains all jquery static files.


## Install

```shell
pip install django-static-jquery-ui
```

## Settings

    INSTALLED_APPS = [
        ...
        'django_static_jquery_ui',
        ...
    ]

## Usage

### Example 1

Include jquery-ui resources in template file.

```html
{% load static %}

<link rel="stylesheet" href="{% static "jquery-ui/jquery-ui.min.css" %}" />
<script src="{% static "jquery-ui/external/jquery/jquery.js" %}"></script>
<script src="{% static "jquery-ui/jquery-ui.min.js" %}"></script>
```

### Example 2

Use "ui-lightness" theme and enable i18n for datepicker.

```html
{% load static %}

<link rel="stylesheet" href="{% static "jquery-ui/jquery-ui.min.css" %}" />
<link rel="stylesheet" href="{% static "jquery-ui/ui-lightness/theme.css" %}" />
<script src="{% static "jquery-ui/external/jquery/jquery.js" %}"></script>
<script src="{% static "jquery-ui/jquery-ui.min.js" %}"></script>
<script src="{% static "jquery-ui/i18n/datepicker-zh-Hans.js" %}"></script>
```

### Example 3

Includ jquery-ui resources in model admin site.

```python
class TestModelAdmin(admin.ModelAdmin):
    class Media:
        css = {
            "all": [
                "jquery-ui/jquery-ui.min.css",
                "jquery-ui/ui-lightness/theme.css",
            ]
        }
        js = [
            "jquery-ui/external/jquery/jquery.min.js",
            "jquery-ui/jquery-ui.min.js",
            "jquery-ui/i18n/datepicker-zh-Hans.js",
        ]
```


*Note:*

- You can use site's default jquery.js instead of jquery.js shipped in jquery-ui.


## About Release Versions

- The first three version number matches with jQuery UI's version number.
- The fourth version number is own release number.

## Release

### 1.12.1.1 2020/03/17

- Rename application name from jquery_ui to django_static_jquery_ui. **Note:** Rename is NOT backward compatible, please change the app name in INSTALLED_APPS inside settings.py.

### 1.12.1.0 2019/12/06

- First release.
- Include all files of jquery-ui 1.12.1 and offical themes, all files are download from https://jqueryui.com/download/all/.
- Include i18n language files for datepicker widget which are download from the demo site.
