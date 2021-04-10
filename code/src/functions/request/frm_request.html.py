def get_discos():
    table_discos="""
            <table> <!-- DISCOS ------------------------------------ -->
                <thead>
                    <tr>
                        <th width=32><b>Disco #</b></th>
                        <th width=64><b>Tamaño en GB</b></th>
                        <th width=32><b></b></th>
                        <th width=384><b>Imagen de Disco</b></th>
                        <th width=32><b></b></th>
                        <th width=256><b>Otra Subnet</b></th>
                    </tr>
                </thead>
                <tbody>
                """
    for i in range(12):
        table_discos = table_discos+f"""
                    <tr>
                        <td align=center>{i+1}</td>
                        <td><input class="form-control" id="vmDisk{i}Size" name="vmDisk{i}Size" type="number" value={{{{form.vmDisk{i}Size.data}}}}></td>
                        <td></td>
                        <td>
                            <select class="form-control" name="vmDisk{i}Image" id="vmDisk{i}Image">
                              {{%- for value,option in form.vmDisk0Image.choices %}}
                                {{%- if value == form.vmDisk{i}Image.data %}}
                                <option selected value="{{value}}">{{option}}</option>
                                {{%- else %}}
                                <option value="{{value}}">{{option}}</option>
                                {{%- endif %}}
                              {{%- endfor %}}
                            </select>
                        </td>
                        """
        if i <3:
            table_discos=table_discos+f"""
                        <td></td>
                        <td><select class="form-control" name="vmNic{i}Vlan" id="vmNic{i}Vlan"></select></td>
                        """
        table_discos = table_discos+"""
                    </tr>
                    """
    table_discos = table_discos+f"""
            </tbody>
        </table>
        """
    return table_discos

frm_request_html="""
<form method="post" class="form" role="form">
    <!-- csrf_token: {{ form.csrf_token }} hidden_tag(): {{ form.hidden_tag() }} name: {{ form.name }} -->
    <table bgcolor=white> <!-- MAIN TABLE -------------------------- -->
        <tr>
            <td>
                <table> <!-- Main VM fields request form ----------- -->
                    <tr>
                        <td width=256><b>Solicitud</b></td>
                        {%- if row.Id > 0 %}
                        <td style="color:blue">{{row.Id}} <b>{{get_request_status_description(row.Status)|join(', ')}}</b></td>
                        {%- else %}
                        <td style="color:blue"><b>Nueva solicitud</b></td>
                        {%- endif %}
                    </tr>
                    <tr>
                        <td width=256><b>Nombre de MV   </b></td>
                        <!-- <td><input class="form-control" id="vmName" name="vmName" type="text" value="{ {rox.vm_name} }"></td> -->
                        <td><input class="form-control" id="vmName" name="vmName" type="text" value="{{form.vmName.data}}"></td>
                        {# %- if 'vmName' in form.errors %}<td><font color=red>{% for error in form.errors.vmName %}{{error}}{% endfor %}</td>{% endif % #}
                        {%- if form.vmData.extra is defined and form.vmData.extra %}
                            <td width=32></td>
                            <td width=256><b>Cluster</b></td>
                            <td>
                              <select class="form-control" name="vmCluster" id="vmCluster">
                                {%- for value,option in form.vmCluster.choices %}
                                  {%- if value == form.vmCluster.data %}
                                  <option selected value="{{value}}">{{option}}</option>
                                  {%- else %}
                                  <option             value="{{value}}">{{option}}</option>
                                  {%- endif %}
                                {%- endfor %}
                              </select>
                            </td>
                        {%- endif %}
                    </tr>
                    <tr>
                        <td><b>CPU cores por Socket</b></td>
                        <!-- td><input class="form-control" id="vmCPS" name="vmCPS" type="number" value="{{form.vmCPS.data}}" onchange="get_cpu()"></td -->
                        <td><input class="form-control" id="vmCPS" name="vmCPS" type="number" value="{{form.vmCPS.data}}"></td>
                        {%- if form.vmData.extra is defined and form.vmData.extra %}
                            <td width=32></td>
                            <td width=256><b>Proyecto</b></td>
                            <td>
                              <!-- GV 202010318 select class="form-control" name="vmProject" id="vmProject" onchange="get_subnet_options(this.value)" -->
                              <select class="form-control" name="vmProject" id="vmProject" onchange="get_project_subnet_options(this.value)">
                                {%- for value,option in form.vmProject.choices %}
                                  {%- if value == form.vmProject.data %}
                                  <option selected value="{{value}}">{{option}}</option>
                                  {%- else %}
                                  <option value="{{value}}">{{option}}</option>
                                  {%- endif %}
                                {%- endfor %}
                              </select>
                            </td>
                        {%- endif %}
                    </tr>
                    <tr>
                        <td><b>Sockets</b></td>
                        <!-- td><input class="form-control" id="vmSockets" name="vmSockets" type="number" value="{{form.vmSockets.data}}" onchange="get_cpu()"></td -->
                        <td><input class="form-control" id="vmSockets" name="vmSockets" type="number" value="{{form.vmSockets.data}}"></td>
                        {%- if form.vmData.extra is defined and form.vmData.extra %}
                            <td width=32></td>
                            <td width=256><b>Categoria</b></td>
                            <td>
                              <select class="form-control" name="vmCategory" id="vmCategory">
                                {%- for value,option in form.vmCategory.choices %}
                                  {%- if value == form.vmCategory.data %}
                                  <option selected value="{{value}}">{{option}}</option>
                                  {%- else %}
                                  <option             value="{{value}}">{{option}}</option>
                                  {%- endif %}
                                {%- endfor %}
                              </select>
                            </td>
                        {%- endif  %}
                    </tr>
                    <!--tr>
                        <td><b>Número de CPUs </b></td>
                        <! -- td style="color:blue"><b>{{ form.vmCPS.data * form.vmSockets.data }}</b></td - ->
                        <td style="color:blue"><b>
                            <input class="form-control-plaintext" id="vmCPU" name="vmCPU" type="text" style="color:blue;font-weight:bold;" value="{{ form.vmCPS.data * form.vmSockets.data }}">
                        </b></td>
                    </tr-->
                    <tr>
                        <td><b>Memoria RAM en GB</b></td>
                        <!-- <td><input class="form-control" id="vmRAM" name="vmRAM" type="number" value="{{rox.memory_size_gib}}"></td> -->
                        <td><input class="form-control" id="vmRAM" name="vmRAM" type="number" value="{{form.vmRAM.data}}"></td>
                        <td width=32></td>
                        <td width=256><b>Subred</b></td>
                        <td><select class="form-control" name="vmSubnet" id="vmSubnet"></select></td>
                    </tr>
                    <tr>
                        <td><b>Corporativa</b></td>
                        <td>
                          <select class="form-control" name="vmCorporate" id="vmCorporate">
                            {%- for value,option in form.vmCorporate.choices %}
                              {%- if value == form.vmCorporate.data %}
                              <option selected value="{{value}}">{{option}}</option>
                              {%- else %}
                              <option value="{{value}}">{{option}}</option>
                              {%- endif %}
                            {%- endfor %}
                          </select>
                        </td>
                        <td width=32></td>
                        <td><b>DRP</b></td>
                        <td>{{ form.vmDRP }}</td>
                    </tr>
                    <tr>
                        <td><b>Gerencia</b></td>
                        <td>
                          <select class="form-control" name="vmDepartment" id="vmDepartment">
                            {%- for value,option in form.vmDepartment.choices %}
                              {%- if value == form.vmDepartment.data %}
                              <option selected value="{{value}}">{{option}}</option>
                              {%- else %}
                              <option value="{{value}}">{{option}}</option>
                              {%- endif %}
                            {%- endfor %}
                          </select>
                        </td>
                        <td width=32></td>
                        <td><b>CD ROM</b></td>
                        <td>{{ form.vmCDROM }}</td>
                    </tr>
                    <tr>
                        <td><b>Centro de Costo</b></td>
                        <td>
                          <select class="form-control" name="vmCC" id="vmCC">
                            {%- for value,option in form.vmCC.choices %}
                              {%- if value == form.vmCC.data %}
                              <option selected value="{{value}}">{{option}}</option>
                              {%- else %}
                              <option value="{{value}}">{{option}}</option>
                              {%- endif %}
                            {%- endfor %}
                          </select>
                        </td>
                        <td></td>
                        <td><b>Resumen de MV</b></td>
                        <td><input class="form-control-plaintext" id="vmResume" name="vmResume" type="text" value="Resume" style="color:blue;font-weight:bold;"></td>
                    </tr>
                    <tr>
                        <td><b>Tipo de disco</b></td>
                        <td>
                          <select class="form-control" name="vmType" id="vmType">
                            {%- for value,option in form.vmType.choices %}
                              {%- if value == form.vmType.data %}
                              <option selected value="{{value}}">{{option}}</option>
                              {%- else %}
                              <option value="{{value}}">{{option}}</option>
                              {%- endif %}
                            {%- endfor %}
                          </select>
                        </td>
                        <td></td>
                        <td><b>Mensual estimado UF</b></td>
                        <td><input class="form-control-plaintext" id="vmMonth" name="vmMonth" type="text" value="Month" style="color:blue;font-weight:bold;"></td>
                    </tr>
                </table>
            </td>
        </tr>
        <hr>
        <!-- td><input class="form-control-plaintext" id="vmHelp" name="vmHelp" type="text" value="" style="color:red"></td -->
        {%- if form.vmData.debug is defined and form.vmData.debug %}
        <tr>
        <td><input class="form-control-plaintext" id="vmMessage" name="vmMessage" type="text" value="Message" style="color:red;font-weight:bold;"></td>
        </tr>
        {%- endif %}
        <tr>
            <td>
            <hr>
            <!-- VM required storage specifications ---------------- -->
            """+get_discos(
)+"""
            <hr>
            </td>
        </tr>
        <tr><td>
        <table> <!-- REQUERIMIENTO ESPECIAL ---------------------------- -->
            <thead>
                <tr><th width=1024><b>Requerimiento especial</b></th></tr>
            </thead>
            <tbody>
                <tr><td><input class="form-control" id="vmRequestText" name="vmRequestText" type="text" value="{{form.vmRequestText.data}}"></td></tr>  
            </tbody>
        </table>
        </td></tr>
    </table>
    <hr>
    <!-- Button options as per user role --------------------------- -->
    {%- if form.vmData.rolename == 'Requestor' %}
        <!-- Options for Requestor role ---------------------------- -->
        {# %- if row.Status is none or has_status(row.Status,form.vmData.status.NONE) % #}
        {%- if row.Status is none or row.Status == 0 or has_status(row.Status,form.vmData.status.NONE) %}
            <!-- Options for non Created Request ----------------------- -->
            <input class="btn btn-default" id="submit_Guardar"    name="submit_Guardar"    type="submit" value="Guardar">
            <input class="btn btn-default" id="submit_Retorno"   name="submit_Retorno"   type="submit" value="Retorno">
        {%- elif has_status(row.Status,form.vmData.status.CREATED) %}
            <!-- Options for Created Request ----------------------- -->
            <input class="btn btn-default" id="submit_Guardar"    name="submit_Guardar"    type="submit" value="Guardar">
            <input class="btn btn-default" id="submit_Completado" name="submit_Completado" type="submit" value="Completado" >
            <input class="btn btn-default" id="submit_Cancelar"   name="submit_Cancelar"   type="submit" value="Cancelar">
            <input class="btn btn-default" id="submit_Retorno"   name="submit_Retorno"   type="submit" value="Retorno">
        {%- elif has_status(row.Status,form.vmData.status.REQUESTED) %}
            <!-- Options for Requested Request - ---------------------->
            <input class="btn btn-default" id="submit_Cancelar"   name="submit_Cancelar"   type="submit" value="Cancelar">
            <input class="btn btn-default" id="submit_Retorno"   name="submit_Retorno"   type="submit" value="Retorno">    
        {%- else %}
            <!-- Options for Inactive Request ---------------------- -->
            <input class="btn btn-default" id="submit_Retorno"   name="submit_Retorno"     type="submit" value="Retorno">
        {%- endif %}
    {%- elif form.vmData.rolename == 'Approver' %}
        <!-- Options for Approver role ----------------------------- -->
        {%- if has_status(row.Status,[form.vmData.status.REQUESTED,form.vmData.status.REVIEWED]) %}
            <!-- Options for Requested Request --------------------- -->
            <input class="btn btn-default" id="submit_Guardar"    name="submit_Guardar"    type="submit" value="Guardar">
            <input class="btn btn-default" id="submit_Rechazar"   name="submit_Rechazar"   type="submit" value="Rechazar">
            <input class="btn btn-default" id="submit_Aprobar"    name="submit_Aprobar"    type="submit" value="Aprobar">
            <input class="btn btn-default" id="submit_Retorno"   name="submit_Retorno"   type="submit" value="Retorno">
        {%- elif has_status(row.Status,[form.vmData.status.REJECTED,form.vmData.status.APPROVED]) %}
            <!-- Options for Handled Request ----------------------- -->
            <input class="btn btn-default" id="submit_Retorno"   name="submit_Retorno"   type="submit" value="Retorno">    
        {%- else %}
            <!-- Options for Inactive or post approved Request ----- -->
            <input class="btn btn-default" id="submit_Retorno"   name="submit_Retorno"     type="submit" value="Retorno">
        {%- endif %}
    {%- else %}
        <!-- Options for Other/Viewer role ------------------------- -->
            <input class="btn btn-default" id="submit_Retorno"   name="submit_Retorno"     type="submit" value="Retorno">
    {%- endif %}
    <hr>
    <!-- HIDDEN DATA -->
    <input id="vmTopCC"   name="vmTopCC"     type="hidden" value="{{form.vmTopCC}}">
    <!-- HIDDEN DATA COMPLETE -->
    {%- if form.vmData.debug is defined and form.vmData.debug %}
        <!--DEBUG DATA FOLLOWS ------------------------------------- -->
        <b>DEBUG MODE is ON: form.vmData.debug is defined and True then debug data follows:</b><br>
        <hr> 
        <p>form.vmTopCC={{form.vmTopCC}}</p>
        row = {{row}}<br>
        top cost center = {{form.vmData.top_cost_center}} {{form.vmData.top_cost_center_id}}<br>
        {%- for status in form.vmData.status %}
            {%- if has_status(row.Status,form.vmData.status[status]) %}
                Status = {{row.Status}} has status {{status}} {{form.vmData.status[status]}}<br> 
            {%- endif %}
        {%- endfor %}
        <hr>
        rox = {{rox}}
        <hr>
        form.vmData = {{form.vmData}}
        <!--DEBUG DATA complete ------------------------------------ -->
    {%- endif %}
</form>
"""

if __name__ == "__main__":
    print(frm_request_html)
