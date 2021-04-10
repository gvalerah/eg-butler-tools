from jinja2 import Template

# Templates

query_example_temp="""
<table border=1>
<tr><td>app              	  </td><td> {{ app.name                     }}</td></tr>
<tr><td>request.method     	  </td><td> {{ request.method               }}</td></tr>
<tr><td>request.content_type  </td><td> {{ request.content_type         }}</td></tr>
<tr><td>request.content_length</td><td> {{ request.content_length       }}</td></tr>
<tr><td>request.data     	  </td><td> {{ request.data                 }}</td></tr>
<tr><td>request args     	  </td><td> {{ request.args|length          }}</td></tr>
{%- for key in request.args.keys() %}
<tr><td></td><td>{{ key }} : {{ request.args.get(key) }}</td></tr>
{%- endfor %}
<tr><td>request form     	  </td><td> {{ request.form                 }}</td></tr>
{%- for key in request.form.keys() %}
<tr><td></td><td>{{ key }} : {{ request.form.get(key) }}</td></tr>
{%- endfor %}
<tr><td>request files    	  </td><td> {{ request.files                }}</td></tr>
{%- for key in request.files.keys() %}
<tr><td></td><td>{{ key }} : {{ request.files.get(key) }}</td></tr>
{%- endfor %}
<tr><td>request values          </td><td> {{ request.values             }}</td></tr>
<tr><td>request json            </td><td> {{ request.json               }}</td></tr>
<tr><td>request get('name')     </td><td> {{ request.args.get("name")   }}</td></tr>
<tr><td>request getlist('name') </td><td> {{ request.args.getlist("name")}}</td></tr>
<tr><td>request get_json()      </td><td> {{ request.get_json()         }}</td></tr>
<tr><td>PAYLOAD</td><td>{{data}}</td></tr>
<table><br>
"""

# ---------------------------------------------------------

# TRX 001 - Example Transaction --------------
trx_001_temp="""
{
"title":"{{data.title}}",
"payload":"{{data.payload}}"
}
"""

def trx_001(data):
    return Template(trx_001_temp).render(data=data)

# ---------------------------------------------------------

