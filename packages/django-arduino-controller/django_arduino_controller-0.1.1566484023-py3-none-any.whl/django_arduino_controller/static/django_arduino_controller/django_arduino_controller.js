if(!logger)
    var logger = console;
if(typeof django_arduino_controller === "undefined"){
    django_arduino_controller = {
        port_listener_ws_url : null,
        board_listener_ws_url: null,
        port_listener_ws: new JsonWebsocket("Port Listener Websocket"),
        ports : {},
        boards : {},

        set_ports : function (data){
            for(let i=0;i<data.ports.available_ports.length;i++)
                django_arduino_controller.set_port_available(data.ports.available_ports[i]);

            for(let i=0;i<data.ports.connected_ports.length;i++)
                django_arduino_controller.set_port_connected(data.ports.connected_ports[i]);

            for(let i=0;i<data.ports.identified_ports.length;i++)
                django_arduino_controller.set_port_identified(data.ports.identified_ports[i]);

            for(let i=0;i<data.ports.ignored_ports.length;i++)
                django_arduino_controller.set_port_ignored(data.ports.ignored_ports[i]);

            var all_new = data.ports.available_ports
                .concat(data.ports.ignored_ports)
                .concat(data.ports.connected_ports.map(p => p.port))
                .concat(data.ports.identified_ports.map(p => p.port));

            let all_old = Object.keys(django_arduino_controller.ports);
            for(let i = 0;i<all_old.length;i++)
                if(all_new.indexOf(all_old[i])<0)
                    django_arduino_controller.remove_port(all_old[i])
        },
        remove_port : function (port) {
            if(django_arduino_controller.ports[port] === undefined)
                return;
            logger.info("remove "+port);
            django_arduino_controller.ports[port].data_element.remove();
            django_arduino_controller.ports[port].ws.close();
            delete django_arduino_controller.ports[port];
        },
        set_port_available : function (port) {
            var port_object = django_arduino_controller.generate_port(port);
            if(port_object.status === "available")
                return;
            if(port_object.ws !== null) {
                port_object.ws.close();
                port_object.ws = null;
            }
            port_object.status = "available";
            for (var key in port_object.data)
                port_object.data[key] = null;
            django_arduino_controller.update_port(port_object,{port:port});

            logger.info("port available: "+ port)
        },
        set_port_connected : function(port) {
            var port_object = django_arduino_controller.generate_port(port.port);
            if(port_object.status === "connected"|| port_object.status === "identified")
                return;
            port_object.status = "connected";
            django_arduino_controller.update_port(port_object,port);
            if(port_object.ws === null)
                port_object.ws = django_arduino_controller.create_port_websocket(port_object)
            logger.info("port connected: "+ port.port);
        },
        set_port_identified : function(port) {
            var port_object = django_arduino_controller.generate_port(port.port);
            if(port_object.status === "identified")
                return;
            if(port_object.status !== "connected")
                django_arduino_controller.set_port_connected(port);

            port_object.status = "identified";
            django_arduino_controller.update_port(port_object,port);
            django_arduino_controller.generate_board(port_object);
            port_object.ws.add_on_connect_function(function () {this.cmd_message("get_board");});
            logger.info("port identified: "+ port.port);
        },
        set_port_ignored : function(port) {
            var port_object = django_arduino_controller.generate_port(port);
            if(port_object.status === "ignored")
                return;
            if(port_object.ws !== null) {
                port_object.ws.close();
                port_object.ws = null;
            }
            port_object.status = "ignored";
            for (var key in port_object.data)
                port_object.data[key] = null;

            django_arduino_controller.update_port(port_object,{port:port});
            logger.info("port ignored: "+ port)
        },
        update_port  : function(port,port_data) {
            port.data.status = port.status;
            port.data = Object.assign(port.data, port_data);

            for(let key in port.data){
                port.data_element.find("[name='port_"+key+"']").text((port.data[key] !== null)?port.data[key]:"-")
            }
        },
        generate_port : function (port) {
            if(django_arduino_controller.ports[port] !== undefined)
                return django_arduino_controller.ports[port];

            django_arduino_controller.ports[port]={
                port:port,
                status:null,
                ws:null,
                data_element:null,
                data:{}
            };

            django_arduino_controller.ports[port].data_element = django_arduino_controller.port_template_generator(django_arduino_controller.ports[port]);
            return django_arduino_controller.ports[port];
        },
        port_template_generator:function(port){},

        generate_board : function (port_object){
            if(django_arduino_controller.boards[port_object.port] !== undefined)
                return django_arduino_controller.boards[port_object.port];

            django_arduino_controller.boards[port_object.port]={
                port:port_object,
                data_element:null
            };

            django_arduino_controller.boards[port_object.port].data_element = django_arduino_controller.board_template_generator(django_arduino_controller.ports[port_object.port]);

            return django_arduino_controller.boards[port_object.port];
        },

        board_template_generator:function(port){},

        create_port_websocket : function(port_object) {
            console.log(django_arduino_controller.board_listener_ws_url)
            let ws = new JsonWebsocket(port_object.port+" Listener Websocket",django_arduino_controller.board_listener_ws_url.replace("port_id",port_object.port));
            ws.add_cmd_funcion("board_update",function (data) {django_arduino_controller.update_port(port_object,data.board_data);});
            ws.add_cmd_funcion("set_board",function (data) {django_arduino_controller.set_board(data.port,data.board);});
            ws.add_cmd_funcion("port_data_point",django_arduino_controller.port_data_point);
            return ws;
        },

        set_board : function (port,board){
            if(django_arduino_controller.boards[port] === undefined)return;

            let mod_vars = Object.keys(board.module_variables);
            let data_container = django_arduino_controller.boards[port].data_element.find('[name="data_container"]');
            data_container.empty();

            for(let i=0;i<mod_vars.length;i++){

                let input = $(board.module_variables[mod_vars[i]].form)
                    .addClass('form-control');
                let label = $('<label for="ard_var_'+input.attr("name")+'">'+mod_vars[i]+'</label>');

                let f = $('<div class="form-group"></div>');
                f.append(label);
                f.append(input);
                if(input.attr("type") === "checkbox")
                    input.prop("checked",input.val() === "True");
                data_container.append(f);
                input.change(function () {
                    let val = input.val();
                    if(input.attr("type") === "checkbox")
                        val = input.prop("checked");
                    django_arduino_controller.boards[port].port.ws.cmd_message("set_board_attribute",
                        {attribute:mod_vars[i],value:val}
                    );
                })
            }
        },

        port_data_point : function (data) {
            if( django_arduino_controller.boards[data.port] === undefined)return;
            let ele = django_arduino_controller.boards[data.port].data_element.find('[name="data_point_'+data.key+'"]')
            if(ele.attr("type") === "checkbox")
                ele.prop("checked",data.y);
            else
                ele.val(data.y);
        }


    };

    django_arduino_controller.port_listener_ws.add_cmd_funcion("set_ports",django_arduino_controller.set_ports);
    $(document).ready(function() {
        if (django_arduino_controller.port_listener_ws_url !== null) {
            django_arduino_controller.port_listener_ws.connect(django_arduino_controller.port_listener_ws_url);
        }
    });
}
