# ======================================================================
# BUTLER REQUEST TEMPLATES
# View for General request Edition
# (c) Sertechno 2020
# GLVH @ 2020-12-31 initial version
# GLVH @ 2021-03-20 adds support for 'other nics'
# Gerardo L Valera gvalera@emtecgroup.net
# ======================================================================
# src: view_request_templates.py

# Templates
# JavaScript/JQuery script templates

scr_functions_template="""
// Updates Subnets options upon Selected project -----------------------
function subnets() {
    //window.alert("subnets(): IN" );            
    // GET UUID FOR CURRENT PROJECT, IMPORTANT ON ON CHANGE ... --------
    var project = $("#vmProject");
    var project_uuid = project.val();
    // POPULATE SUBNETS LIST FOR PROPER PROJECT, ON LINE ---------------
    var subnets = [];                
    {%- for project in subnet_options %}
    {%- if loop.index == 1 %}
    if (project_uuid == "{{project.0}}"){ subnets = {{project.1}}; }
    {%- else %}
    else if (project_uuid == "{{project.0}}"){ subnets = {{project.1}}; }
    {%- endif %}
    {%- endfor %}
    // -----------------------------------------------------------------
    // PRIMARY SUB NET OPTIONS INITIALIZATION --------------------------    
    var $subnet = $("#vmSubnet");
    var subnet_uuid = $subnet.val();
    $subnet.empty();    
    $.each(subnets, function(index, [uuid,name]) {
        if ( uuid == subnet_uuid ) {
            $subnet.append("<option selected value='" + uuid + "'>" + name + "</option>");
        } else {
            $subnet.append("<option value='" + uuid + "'>" + name + "</option>");
        }
    });
    // OTHER SUBNETS OPTIONS INITIALIZATION ----------------------------
    // other nic cards may be empty ...
    subnets.unshift(["",":"]);
    {%- for i in range(3) %}
    var $nic{{i}} = $("#vmNic{{i}}Vlan");    
    var nic_uuid = $nic{{i}}.val();
    $nic{{i}}.empty();
    $.each(subnets, function(index,[uuid,name]) {
        if ( uuid == nic_uuid ) {
            $nic{{i}}.append("<option selected value='" + uuid + "'>" + name + "</option>");
        } else {
            $nic{{i}}.append("<option value='" + uuid + "'>" + name + "</option>");
        }
    });
    {%- endfor %}
    subnet_names();
};

// Updates Subnets options upon Selected project -----------------------
function subnet_names() {
    //window.alert( "subnet_names(): IN" );            
    // GET UUID FOR CURRENT PROJECT, IMPORTANT ON ON CHANGE ... --------
    var project = $("#vmProject");
    var project_uuid = project.val();
    //window.alert( "subnet_names(): populate subnets" );            
    // POPULATE SUBNETS LIST FOR PROPER PROJECT, ON LINE ---------------
    var subnets = [];                
    var selected = [];
    // Sets projects's subnets arrays          
    {%- for project in subnet_options %}
        {%- if loop.index == 1 %}
    if (project_uuid == "{{project.0}}"){ subnets = {{project.1}}; }
        {%- else %}
    else if (project_uuid == "{{project.0}}"){ subnets = {{project.1}}; }
        {%- endif %}
    {%- endfor %}
    
    //window.alert( "subnet_names(): capture selected ..." );            
    // Capture selected uuids ------------------------------------------
    {%- for i in range(4) %}
        var $uid{{i}}  = $("#vmVlan{{i}}Uuid");    
        if ( document.getElementById("vmVlan{{i}}Selected").checked )  {
            selected.push( $uid{{i}}.val() );
        }
    {%- endfor %}

    //window.alert("selected = " + selected.length + " [" + selected+"]");
    //window.alert( "subnet_names(): reset subnets list ..." );            
    // RESET Subnets list ----------------------------------------------
    {%- for i in range(4) %}
        var $uid{{i}}  = $("#vmVlan{{i}}Uuid");    
        var $flag{{i}} = $("#vmVlan{{i}}Selected");    
        var $name{{i}} = $("#vmVlan{{i}}Name");  
        $uid{{i}}.val("<uuid>{{i}}");
        $name{{i}}.val("<name>{{i}}");
        //window.alert( "RESET Subnet {{i}}");
        // Load subnets data up to max or empty
        if ( {{i}} < subnets.length ) {
            $uid{{i}}.val(subnets[{{i}}][0]);
            $name{{i}}.val(subnets[{{i}}][1]);
            document.getElementById("vmVlan{{i}}Uuid").value = subnets[{{i}}][0];
            document.getElementById("vmVlan{{i}}Name").value = subnets[{{i}}][1];
            if (selected.includes($uid{{i}}.val())) {
            //if (selected.includes(document.getElementById("vmVlan{{i}}Uuid").value)) {
                document.getElementById("vmVlan{{i}}Selected").checked = true;
                document.getElementById("vmVlan{{i}}Selected").value = subnets[{{i}}][0];
            }
        } else {
            $uid{{i}}.val("");
            $name{{i}}.val("");
            document.getElementById("vmVlan{{i}}Selected").checked = false;
        }
    {%- endfor %}
    /*
    window.alert(
        $uid0.val()+"|"+$name0.val()+"|"+document.getElementById("vmVlan0Selected").checked+" *** "+
        $uid1.val()+"|"+$name1.val()+"|"+document.getElementById("vmVlan1Selected").checked+" *** "+
        $uid2.val()+"|"+$name2.val()+"|"+document.getElementById("vmVlan2Selected").checked+" *** "+
        $uid3.val()+"|"+$name3.val()+"|"+document.getElementById("vmVlan3Selected").checked
    );
    */
    // window.alert("selected = " + selected.length + " " + selected);
      
    /*
    // -----------------------------------------------------------------
    // ALL SUBNETS OPTIONS INITIALIZATION ------------------------------
    {%- for i in range(4) %}
    var $uid{{i}}  = $("#vmVlan{{i}}Uuid");    
    var $flag{{i}} = $("#vmVlan{{i}}Selected");    
    var $name{{i}} = $("#vmVlan{{i}}Name");    
    var nic_uuid   = $uid{{i}}.val();
    $uid{{i}}.empty();
    document.getElementById('vmVlan{{i}}Selected').checked = false
    $name{{i}}.empty();
    $.each(selected, function(index,uuid) {
        if ( uuid == nic_uuid ) {
            document.getElementById('vmVlan{{i}}Selected').checked = true
        }
    });
    {%- endfor %}
    */
};


function managements() {
    // GET Value FOR CURRENT Corporate, IMPORTANT ON ON CHANGE ... -----
    var $dropdown    = $("#vmCorporate");
    var corporate = $dropdown.val();
    // POPULATE "Gerencias" LIST FOR PROPER "Corporate", ON LINE -------
    var managements = [];                
    {%- for key in gd_map.keys() %}
    if (corporate == "{{gd_map[key].corporate}}"){managements.push([{{gd_map[key].code}},"{{gd_map[key].description}}"]);}
    {%- endfor %}
    // -----------------------------------------------------------------
    // PRIMARY Gerencias OPTIONS INITIALIZATION ------------------------    
    var $management = $("#vmDepartment");
    $management.empty();    
    $.each(managements, function(index, [code,name]) {
        if ( code == $management.val() ) {
            $management.append("<option selected value='" + code + "'>" + name + "</option>");
        } else {
            $management.append("<option value='" + code + "'>" + name + "</option>");
        }
    });
};

// Calculates total storage requested for provisioninig ----------------
function get_storage() {
    //window.alert( "get_storage(): IN" );            
    var storage = 0;
    var size    = 0;
    {%- for i in range(12) %}
    size = parseInt($("#vmDisk{{i}}Size").val(),10); if ( ! isNaN(size) ) {storage = storage + size}; 
    {%- endfor %}
    return storage ;
};
// Summarize VM requirements -------------------------------------------
// Also recalculates expected monthly rate as per VM configuration
function summary() {
    try {
        var cps         = $("#vmCPS").val();
        var sockets     = $("#vmSockets").val();
        var ram         = $("#vmRAM").val();
        var cores       = cps * sockets;
        var storage     = get_storage();
        
        var topcc       = parseInt($("#vmTopCC").val());
        var corporate   = parseInt($("#vmCorporate").val())  - topcc;
        var department  = parseInt($("#vmDepartment").val()) - topcc - corporate;
        var environment = parseInt($("#vmCC").val())         - topcc;                
        var type        = parseInt($("#vmType").val())       - topcc;
        var cc          = topcc + corporate + department + environment + type;                
        $("#vmResume").val(cores + " CPU x " + ram + " GB RAM x " + storage + " GB");
        $("#vmMonth").val(get_month().toFixed(6) + " UF cargable a " + cc);
        $("#vmMessage1").val(cores + " CPU x " + ram + " GB RAM x " + storage + " GB " + topcc + "+" + corporate + "+" + department + "+" + environment + "+" + type + "=" + cc );
        return $("#vmResume").val();
    } catch (e) {
        window.alert(e.name + ': ' + e.message);
    }
};
// Look for proper rate upon cost center specification or default ------
function get_rate(type,cc) {
    //window.alert( "get_rate() IN type= "+type+" cc= "+cc  );            
    var rateid      = '' ;
    var ratedefault = '' ;
    var rate        = 0  ;
    var rateid      = 0  ;
    var ratedefault = 0 ;
    var Rates = [
    {%- for r in rates %}
        ["{{r}}",{{"%.24f"|format(rates[r])}}],
    {%- endfor %}
    ];
    
    // looks for specific rate code for CC
    for (r=0;r<Rates.length;r++){
        rateid      = type + ':' + cc ;
        if ( Rates[r][0] == rateid) {
            rate = Rates[r][1]; 
            break;
        }
    }
    if (rate == 0){
        // If specific rate not found then look for default rate
        for (r=0;r<Rates.length;r++){
            rateid = type + ':' + '1' ;
            if ( Rates[r][0] == rateid) {
                rate = Rates[r][1]; 
                break;
            }
        }
    }
    //window.alert( "get_rate() returns for " + type + ":" + cc + " rateid = " + rateid + " rate = "+rate  );            
    $("#vmMessage3").val("get_rate() returns for " + type + ":" + cc + " rateid = " + rateid + " rate = "+rate);
    return rate;
};

// Calculates expected monthy rate upon VM configuration ---------------
function get_month() {
    //window.alert( "get_month() IN" );            
    var cps          = $("#vmCPS").val();
    var sockets      = $("#vmSockets").val();
    var ram          = $("#vmRAM").val();
    var cores        = cps * sockets;
    var storage      = get_storage();
    // Will build actual detail level CC from components ---------------
    var topcc        = parseInt($("#vmTopCC").val());
    var corporate    = parseInt($("#vmCorporate").val())  - topcc;
    var management   = parseInt($("#vmDepartment").val()) - topcc - corporate;
    var environment  = parseInt($("#vmCC").val())         - topcc;                
    var disk_type    = parseInt($("#vmType").val())       - topcc;
    var cc           = topcc + corporate + management + environment + disk_type;                
    // Get actual rates ------------------------------------------------
    var rate_ram     = get_rate('RAM',cc);
    var rate_cores   = get_rate('CPU',cc);
    var rate_storage = get_rate('DSK',cc);                
    $("#vmMessage1").val("cc: " + cc +" ram: " + rate_ram + " cpu: " + rate_cores + " dsk: " + rate_storage);
    var month = cores * rate_cores + ram * rate_ram + storage * rate_storage ;
    $("#vmMessage2").val(cores+"*"+rate_cores+ "+" + ram+"*"+rate_ram+ "+" +storage+"*"+rate_storage+ " = "+month);
    return month ;
};        
// document ON LOAD event setup function -------------------------------
function load() {
    //window.alert( "load() IN" );            
    managements();
    set_attributes();
    //subnets();
    subnet_names();
    summary();
};
// ---------------------------------------------------------------------
"""
scr_request_template="""
// Project change event ------------------------------------------------ 
{# obsolete dropdown version (SelectField)
$("#vmProject").on('change',function() {
    //window.alert( "#vmProject".on.change(): IN" );            
    var $dropdown = $(this);
    var key = $dropdown.val();
    var vals = [];                
    {%- for project in subnet_options %}
    if (key == "{{project.0}}"){
         vals =  {{project.1}};
    }
    {%- endfor %}
    //subnets();
    subnet_names();
});
#}
$("#vmProject").on('change',function() {
    //window.alert( "vmProject.on.change(): IN" );            
    var key = $("#vmProject").val();
    var vals = [];                
    {%- for project in subnet_options %}
    if (key == "{{project.0}}"){
         vals =  {{project.1}};
    }
    {%- endfor %}
    //subnets();
    subnet_names();
});

$("#vmProjectName").on('change',function() {
    window.alert( "vmProjectName.on.change(): IN" );            
    var key = $("#vmProject").val();
    var vals = [];                
    {%- for project in subnet_options %}
    if (key == "{{project.0}}"){
         vals =  {{project.1}};
    }
    {%- endfor %}
    //subnets();
    subnet_names();
});

// Corporate change event ---------------------------------------------- 
$("#vmCorporate").on('change',function() {
    //window.alert( "#vmProject".on.change(): IN" );            
    var $dropdown = $(this);
    var key = $dropdown.val();
    var vals = [];                
    {%- for corporate in corporate_options %}
    if (key == "{{corporate.0}}"){
         vals =  {{corporate.1}};
    }
    {%- endfor %}
    managements();
    summary();
});


// sets Project and Category depending on Environment and Cluster ------
function set_attributes() {
    var environment = $("#vmCC").val();
    var cluster     = $("#vmCluster").val();
    var envid       = environment + ':' + cluster ;
    
    var envs = [
    {%- for e in environments_codes %}
        {%- for c in environments_codes[e] %}
        ["{{e}}:{{c}}","{{environments_codes[e][c]['project']}}","{{environments_codes[e][c]['category']}}","{{environments_codes[e][c]['project_name']}}","{{environments_codes[e][c]['category_description']}}"],
        {%- endfor %}
    {%- endfor %}
    ];
    
    // searchs specific environment:cluster pair for Project & Category
    //window.alert( "env id: " + envid + " len= " + envs.length );            
    for (e=0;e<envs.length;e++){
        //window.alert( "env" + e + ": " + envs[e][0] + envs[e][1] + envs[e][3] );            
        if ( envs[e][0] == envid) {
            //window.alert( "match env" + e + ": " + envs[e][0] + " " + envs[e][1] + " " + envs[e][3] );            
            //vmProject.val(envs[e][1]);
            $("#vmProject").val(envs[e][1]);
            $("#vmCategory").val(envs[e][2]);
            $("#vmProjectName").val(envs[e][3]);
            $("#vmCategoryName").val(envs[e][4]);
            break;
        }
    }
    //window.alert( "project: " + vmProject.val() + " " + vmProjectName.val()  );            

    //window.alert( "callig subnets ..."  );            
    //window.alert( "project: " + $("#vmProject").val() + " " + $("#vmProjectName").val()  );            
    
    $("#vmMessage4").val("project: " + $("#vmProject").val() + " " + $("#vmProjectName").val());

    //subnets();
    //window.alert( "set attributes callig subnet_namess ..."  );            
    subnet_names();
    return;           
};


// Environment change event -------------------------------------------- 
$("#vmCC").on('change',function() {
    set_attributes();
    summary();
});

// Cluster change event ------------------------------------------------ 
$("#vmCluster").on('change',function() {
    set_attributes();
    summary();
});


"""
scr_cpu_template="""
// Cores per socket change event handler -------------------------------
$("#vmCPS").on('change',function() {
    //window.alert( "#vmCPS".on.change(): IN" );            
    var $vmCPS     = $(this);
    var $vmSockets = $("#vmSockets");
    var cps        = $vmCPS.val();
    var sockets    = $vmSockets.val();
    var cores      = cps * sockets;
    var $cpu       = $("#vmCPU");
    $cpu.val(cores);
    $cpu.text(cores);
    summary();
});
// Sockets change event handler ----------------------------------------
$("#vmSockets").on('change',function() {
    //window.alert( "#vmSockets".on.change(): IN" );            
    var $vmCPS     = $("#vmCPS");
    var $vmSockets = $(this);
    var cps        = $vmCPS.val();
    var sockets    = $vmSockets.val();
    var cores      = cps * sockets;
    var $cpu       = $("#vmCPU");
    $cpu.val(cores);
    $cpu.text(cores);
    summary();
});
"""
scr_storage_template="""
// Disk Image change event handler -------------------------------------
function check_image_size(i) {            
    //window.alert( "check_image_size("+i+") IN"   );            
    var Size     = $("#vmDisk"+i+"Size");            
    var Selected = $("#vmDisk"+i+"Image option:selected"    );
    var imagesize = 0;
    var tokens = $(Selected).text().split("("); 
    var token1 = tokens[1].split(" "); 
    imagesize = parseInt(token1[0],10);
    if (parseInt(Size.val(),10) < imagesize){
        Size.val(imagesize);
        i = i + 1;
        window.alert( "Tamaño de disco " + i + " será expandido según requerimiento de imagen: " + $(Selected).text());
    }
    summary();
};
// Disk size change event handler --------------------------------------
function check_disk_size(i){
    //window.alert( "check_disk_size("+i+") IN"   );            
    var Image = $("#vmDisk"+i+"Image");
    if (i == 0){
        if ( ! Image.val() == "" ){
            check_image_size(i);
        }
    }
    summary();
};
"""
scr_events_template="""
// Configuration fields change event handlers --------------------------
//$("#vmCPU").on( 'change' , summary() );
$("#vmDebug").on('change',function() {window.alert( "#vmDebug.on.change(): IN" );window.repaint();});
$("#vmRAM").on( 'change' , function(){summary();} );
$("#vmDepartment").on( 'change' , function(){summary();} );
$("#vmCC").on( 'change' , function(){summary();} );
$("#vmType").on( 'change' , function(){summary();} );
{%- for i in range(12) %}
$("#vmDisk{{i}}Size").on('change',function(){check_disk_size({{i}});});
{%- if i == 0 %}
$("#vmDisk{{i}}Image").on('change',function(){check_image_size({{i}});});
{%- endif %}
{%- endfor %}
// document ON LOAD event setup ----------------------------------------
window.onload = load();
// ---------------------------------------------------------------------
"""
scr_help_template="""
function help(obj) {
    window.alert("Help IN obj="+obj);
    var Help = $("#vmHelp");
    var msg  = "";
    if      (obj=='vmName'){msg="Este es el nombre único de la MV";}
    else if (obj=='vmCPS') {msg="Número de CPU cores por socket";}
    window.alert("Help msg="+msg);
    $Help.val (msg);            
    $Help.text(msg);            
};
$("#vmName").on("click",help("vmName"));
$("#vmCPS").mouseover (help("vmCPS" ));
"""

# Scripts array (script order is significative)
Script_Templates = [
    scr_functions_template,
    scr_storage_template,
    scr_request_template,
    scr_cpu_template,
    scr_events_template,
]
# EOF ******************************************************************
