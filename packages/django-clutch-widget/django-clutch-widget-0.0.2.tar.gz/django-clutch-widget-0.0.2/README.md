django-clutch-widget
====================

Template tag to install your Clutch Widget account in your templates

## Installation and Usage

1. run `pip install django-clutch-widget`
2. add `'clutch'` to your `INSTALLED_APPS` setting.
3. set `CLUTCH_COMPANY_ID` 
4. In your templates (probably in your base template) you `{% load
   clutch_tags %}` add `{% clutch %}` whenever you want
