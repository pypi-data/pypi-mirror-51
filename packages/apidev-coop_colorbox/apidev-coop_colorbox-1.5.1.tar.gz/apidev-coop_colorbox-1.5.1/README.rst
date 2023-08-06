coop-colorbox, make easy to use jquery.colorbox in a django app
===============================================================


Install
=======

pip::

     pip install apidev_coop-colorbox


Settings
========

In settings.py::

    INSTALLED_APPS = (
        '...',
        'colorbox',
    )

Views
=====
views::

     from django.utils.decorators import method_decorator
     from django.http import HttpResponseRedirect, Http404

     from colorbox.decorators import popup_redirect
     class MyView(FormView):
         """edit the profile of the current user"""
         template_name = "form_popup_template.html"

         @method_decorator(popup_redirect)
         def dispatch(self, request, *args, **kwargs):
             """Manage close of the colorbox popup"""
             self.user = request.user
             return super(EditProfileView, self).dispatch(request, *args, **kwargs)

         def get_form_class(self):
             """returns the form class to use"""
             return MyForm

         def form_valid(self, form):
             form.save()
             return HttpResponseRedirect(reverse(’next_step'))

form_popup_template
===================
template::

     {% extends "colorbox/popup_form_base.html" %}
     {% load i18n %}
     {% block title %}{% trans "Edit" %}{% endblock %}
     {% block form_url %}{% url 'my_view' %}{% endblock %}

You can also overrides or extends `{% block form_intro %}` {% block form_fields %}` `{% block popup_buttons %}`
or `{% block extra_head %}`

main template
=============
template::

     {% load static i18n %}
     <script type="text/javascript" charset="utf-8" src="{% static 'js/jquery.colorbox-min.js' %}"></script>
     <script type="text/javascript" charset="utf-8" src="{% static 'js/jquery.form.js' %}"></script>
     <script type="text/javascript" src="{% static 'js/colorbox.coop.js' %}"></script>
     <link rel="stylesheet" href="{% static 'css/colorbox.css' %}" type="text/css" />
     <script>
       $(function () {
         // activate popups
         $("a.colorbox-form").colorboxify();
       });
     </script>
     <a class="colorbox-form" href="{% url 'my_view' %}">{% trans "Edit" %}</a>


In tests
========
tests::

     from colorbox.utils import assert_popup_redirects
     assert_popup_redirects(response, reverse('my_view'))


License
=======

coop-colorbox uses the BSD license see license.txt
