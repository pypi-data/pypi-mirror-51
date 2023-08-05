if (!logger)
    var logger = console;

if (typeof arduino_api_controller === "undefined") {
    arduino_api_controller = {
        api_ws_url: null,
        hidden: false,
        apis: [],
        api_controll_panel: $('#controller_sidebar_content'),
        api_ws: new JsonWebsocket("Arduino Api Websocket"),
        check_apis: function () {
            arduino_api_controller.api_ws.cmd_message("get_apis")
        },
        clear_apis: function () {
            for (let i = arduino_api_controller.apis.length - 1; i >= 0; i--) {
                arduino_api_controller.apis[i].remove();
            }
            arduino_api_controller.apis = []
        },
        api_constructor: function (api) {
            if(arduino_api_controller.hidden)return $("<div></div>");
            let panel = $('<div id="api_control_panel_' + api.position + '">' +
                '<div class="api_control_panel_title">' + api.name + '<span name="status_indicator"><span class="tooltiptext"></span></span></div><div name="api_control_panel_boards"></div></div>');
            arduino_api_controller.api_controll_panel.append(panel);
            return panel;
        },
        board_constructor: function (board) {
            let panel = $('<div name="api_control_panel_board_' + board.position + '"></div>');
            let title = $('<div class="api_control_panel_board_title">' + board.board_class + '</div>');
            panel.append(title);
            let selector=$('<select name="board_selector"><option selected disabled="disabled">choose board</option></select>');
            for(let i=0;i<board.possible_boards.length;i++){
                let option = $('<option value="'+i+'"></option>');
                option.text(board.possible_boards[i]);
                selector.append(option);
                if(board.possible_boards[i] === board.linked_board){
                    option.attr('selected',true);
                }
            };
            selector.change(function(){
                let send_data={api: board.api.position,
                    index:board.position,
                    possible_index:parseInt(selector.val())
                };
                arduino_api_controller.api_ws.cmd_message("link_possible_board", send_data);
                console.log(selector.val())
            });
            panel.append(selector);

            return panel
        },
        ApiFunction : class{
            constructor(api,name,data) {
                this.api = api;
                this.name= name;
                this.input = null;
                this.create_input(data);
            }

            create_input(data) {
                if(!data.visible)return;
                let box = $("<form class='api_function_box form'><div class='function_name h5'>"+this.name+"</div></form>");
                if(data.datalink !== undefined){
                    box.find('.function_name').append(' [<span datalink="'+data.datalink+'"></span>]')
                }

                for (let kwarg in data.kwargs) {
                    let funcdata = data.kwargs[kwarg];
                    let subbox=$("<div class='api_function_parameter form-check-inline'></div>");
                    let input = $('<input name="'+kwarg+'"class="form-control "/>');
                    input.attr("type", funcdata.type ? funcdata.type : "number");
                    input.val(funcdata.default ? funcdata.default : 0);
                    switch (funcdata.type) {
                        case "number":
                            if(funcdata.step)
                                input.attr("step", funcdata.step);
                            break;
                        default:
                            break;
                    }
                    subbox.append(input);
                    subbox.append("<label>" + kwarg + "</label>");
                    box.append(subbox);
                }
                let button = $("<button class='functionbutton btn btn-primary' disabled>set</button>");
                box.append(button);
                let func = this;
                box.submit(function( event ) {
                    event.preventDefault();
                    func.run($( this ).serializeArray());
                    });
                this.input = box;
            }

            run(data){
                console.log(this,data);
                if(!this.api.ready)
                    return;
                let send_data={api: this.api.position};
                for(let i=0;i<data.length;i++){
                    send_data[data[i].name] = data[i].value
                }
                arduino_api_controller.api_ws.cmd_message(this.name, send_data);

            }
        },
        Board: class {
            constructor(api, position, board_class, linked_board, possible_boards) {
                this.api = api;
                this.position = position;
                this.board_class = board_class;
                this.linked_board = linked_board.board;
                this.id = linked_board.id;
                this.possible_boards = possible_boards;
                this.container = arduino_api_controller.board_constructor(this);
                this.api.boardbox.append(this.container);
                this.data={}
            }

            remove() {
                let index = this.api.boardbox.indexOf(this.container);
                if (index > -1) {
                    this.api.boardbox.splice(index, 1);
                }
                this.container.remove();
                index = this.api.boards.indexOf(this);
                if (index > -1) {
                    this.api.boards.splice(index, 1);
                }
            }
            set_data(data){
                for (var attrname in data) { this.data[attrname] = data[attrname]; }
            }
        },
        API: class {
            constructor(name, position) {
                this.name = name;
                this.position = position;
                this.ready=false;
                this.container = arduino_api_controller.api_constructor(this);
                this.boardbox = this.container.find("[name='api_control_panel_boards']");
                this.status_indicator = this.container.find("[name='status_indicator']");
                this.boards = [];
                this.functions={};
            }

            remove() {
                this.clear_boards();
                this.container.remove();
            }

            set_boards(board_obj) {
                this.clear_boards();
                for (let i = 0; i < board_obj.required_boards.length; i++) {
                    this.add_board(new arduino_api_controller.Board(this, i, board_obj.required_boards[i], board_obj.linked_boards[i], board_obj.possible_boards[i]));
                }
            }

            clear_boards() {
                for (let i = this.boards.length - 1; i > 0; i--) {
                    this.boards[i].remove();
                }
                this.boards = [];
                this.boardbox.empty();
            }

            add_board(board) {
                this.boards.push(board);
            }
            set_status(data) {
                this.ready=false;
                this.container.find(".functionbutton").attr("disabled", true);
                if (data.status === true) {
                    this.container.find(".functionbutton").attr("disabled", false);
                    this.status_indicator.addClass("valid");
                    this.status_indicator.removeClass("invalid");
                    this.status_indicator.find(".tooltiptext").text("");
                    this.ready=true;
                }
                if (data.status === false) {
                    this.status_indicator.addClass("invalid");
                    this.status_indicator.removeClass("valid");
                    this.status_indicator.find(".tooltiptext").text(data.reason);
                }
            }

            set_data(data){
                for(let key in data){
                    $('[datalink="'+key+'"]').val(data[key]).text(data[key]);
                }
            }
            clear_functions(){

            }
            set_functions(data) {
                this.clear_functions();
                for (let func in data) {
                    if(data[func].api_function)
                        this.add_function(new arduino_api_controller.ApiFunction(this,func,data[func]));
                }
            }

            add_function(func) {
                this.functions[func.name] = func;
                if(func.input)
                    this.container.append(func.input);
                return func;
            }

            get_board_by_id(id) {
                for (let i = 0; i < this.boards.length; i++) {
                    if(this.boards[i].id === id)
                        return this.boards[i];
                }
                return null
            }
        },
        add_api: function (api) {
            arduino_api_controller.apis.push(api);
            arduino_api_controller.api_ws.cmd_message("get_boards", {api: api.position});
            arduino_api_controller.api_ws.cmd_message("get_status", {api: api.position});
            arduino_api_controller.api_ws.cmd_message("get_functions", {api: api.position});
        },
        set_apis: function (data) {
            arduino_api_controller.clear_apis();
            for (let i = 0; i < data.data.length; i++) {
                arduino_api_controller.add_api(new arduino_api_controller.API(data.data[i], i));
            }
        },
        set_boards: function (data) {
            arduino_api_controller.apis[data.data.api_position].set_boards(data.data)
        },
        set_status: function (data) {
            for (let i = 0; i < Math.min(data.data.length,arduino_api_controller.apis.length); i++) {
                arduino_api_controller.apis[i].set_status(data.data[i]);
            }
        },
        set_functions: function (data) {
            arduino_api_controller.apis[data.data.api_position].set_functions(data.data)
        },
        set_data: function (data) {
            for (let i = 0; i < Math.min(data.data.length,arduino_api_controller.apis.length); i++) {
                arduino_api_controller.apis[i].set_data(data.data[i]);
            }
        },
        set_running_data :function (data) {
        }
    };


    arduino_api_controller.api_ws.RECONNECT_TIME=2000;
    arduino_api_controller.api_ws.add_on_connect_function(arduino_api_controller.check_apis);
    arduino_api_controller.api_ws.add_cmd_funcion("set_apis", arduino_api_controller.set_apis);
    arduino_api_controller.api_ws.add_cmd_funcion("set_boards", arduino_api_controller.set_boards);
    arduino_api_controller.api_ws.add_cmd_funcion("set_status", arduino_api_controller.set_status);
    arduino_api_controller.api_ws.add_cmd_funcion("set_functions", arduino_api_controller.set_functions);
    arduino_api_controller.api_ws.add_cmd_funcion("set_data", arduino_api_controller.set_data);
    arduino_api_controller.api_ws.add_cmd_funcion("set_running_data", arduino_api_controller.set_running_data);
    $(document).ready(function () {
        arduino_api_controller.api_controll_panel.click();
        if (arduino_api_controller.api_ws_url !== null) {
            arduino_api_controller.api_ws.connect(arduino_api_controller.api_ws_url);
        }
    });

    $(window).on("beforeunload", function(e) {
        arduino_api_controller.api_ws.cmd_message("close");
        arduino_api_controller.api_ws.close();
    });
}