## -*- coding: utf-8; -*-
<%inherit file="/form.mako" />

<%def name="title()">${index_title} &raquo; ${report.name}</%def>

<%def name="content_title()">${report.name}</%def>

<%def name="context_menu_items()">
  % if request.has_perm('report_output.list'):
      ${h.link_to("View Generated Reports", url('report_output'))}
  % endif
</%def>

<%def name="render_form()">
  <p style="padding: 1em;">${report.__doc__}</p>
  ${parent.render_form()}
</%def>

${parent.body()}
