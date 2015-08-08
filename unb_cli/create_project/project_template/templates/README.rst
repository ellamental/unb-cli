{{ verbose_name }}
{{ markup.h1(verbose_name) }}

{{ project_description }}

{% if False %}{% block doc %}
Documentation
=============

Documentation for {{ verbose_name }} can be found in the ``/docs``
directory{% if docs_url %}or online at {{ docs_url }}{% endif %}.
{% endblock %}{% endif %}{{ wrap_block(self.doc()) }}

{% if False %}{% block issue %}
Issue Reporting and Contact Information
=======================================

If you have any problems with this software, please take a moment to report
them by email {{ markup.url(issue_reporting_email) }}.

If you are a security researcher or believe you have found a security
vulnerability in this software, please contact us by email at
{{ markup.mailto(security_reporting_email) }}.
{% endblock %}{% endif %}{{ wrap_block(self.issue()) }}

{% if False %}{% block copyright %}
Copyright and License Information
=================================

{{ mit_copyright_line }}

This project is licensed under the {{ license }} license.  Please see the
LICENSE file for more information.
{% endblock %}{% endif %}{{ wrap_block(self.copyright()) }}

