# Templates

# This template is used to format request debug output when needed
request_debug="""
<h1>Request Debug Data</h1>
<table border=1>
    <tr><td>app              	  </td><td> {{ app.name                     }}</td></tr>
    <tr><td>app config            </td>
        <td> 
            <table border=0.5>
            {%- for key in app.config.keys() %}
                <tr><td>{{ key             }}</td>
                    <td>{{ app.config[key] }}</td>
                </tr>
            {%- endfor %}
            </table>
        <td>
    </tr>
    <tr><td>app eg config            </td>
        <td>
            <table border=1>
            {%- for section in app.egconfig %}
                <tr><td>Section: {{ section                      }}</td>
                    <td>
                    <table >
                    {%- for option in app.egconfig[section] %}
                    <tr><td>{{option}}         </td><td> {{ app.egconfig[section][option]   }}</td></tr>
                    {%- endfor %}
                    </table>
                    </td>
                </tr>
            {%- endfor %}
            </table>
        </td>
    </tr>
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
<table>
<h2>Actual function output follows</h2>
"""

