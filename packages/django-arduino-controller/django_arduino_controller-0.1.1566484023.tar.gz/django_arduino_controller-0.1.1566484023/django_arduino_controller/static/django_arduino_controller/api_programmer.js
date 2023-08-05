if (!logger)
    var logger = console;
deactivate_logger=false;
if(deactivate_logger){
    logger = {
        debug(message, ...optionalParams) {
        },
        info(message, ...optionalParams) {
        },
        error(message, ...optionalParams) {
        }
    };
}


if (typeof arduino_api_programmer === "undefined") {
    if (typeof arduino_api_controller === "undefined"){
        logger.error("Arduino API controller not loaded")
    }else {
        let api_programmer_api_selector_container = $('#api_programmer_api_selector_container');
        let api_programmer_api_function_selector = $('#api_programmer_api_function_selector');
        let api_programmer_api_code_creator = $('#api_programmer_api_code_creator');
        let programm = [];
        arduino_api_programmer = {
            apis: [],
            ApiFunction: class {
                constructor(func, api) {
                    this.func = func;
                    this.api = api;
                    this.create_selector();
                }

                create_selector() {
                    this.selector = $("<div class='api-function-selector'></div>");
                    this.selector.text(this.func.name);
                    let func = this;
                    this.selector.draggable({
                        revert: function () {
                            return arduino_api_programmer.dragging_function !== null;
                        },
                        helper: "clone",
                        start: function (event, ui) {
                            arduino_api_programmer.dragging_function = func;
                        },
                        stop: function (event, ui) {
                            arduino_api_programmer.dragging_function = null;
                        }
                    })
                }
            },

            Api: class {
                activate() {
                    api_programmer_api_function_selector.empty();
                    api_programmer_api_function_selector.append(this.function_selector);
                }

                constructor(api) {
                    this.api = api;
                    this.functions = [];
                    this.create_selector();
                    this.create_function_selector();
                    let pre_add_func = api.add_function;
                    let programmer_api = this;
                    for (let i = 0; i < api.functions.length; i++) {
                        programmer_api.add_function(api.functions[i]);
                    }
                    api.add_function = function (func) {
                        func = pre_add_func.call(api, func);
                        programmer_api.add_function(func)

                    };

                }

                add_function(func) {
                    this.functions[func.name] = new arduino_api_programmer.ApiFunction(func, this);
                    this.function_selector.append(this.functions[func.name].selector)
                }

                create_selector() {
                    this.selector = $("<div class='api-selector'></div>");
                    this.selector.text(this.api.name.replace(/([^])([A-Z])/g, "$1 $2"));
                    api_programmer_api_selector_container.append(this.selector);
                    this.selector.click(
                        this.activate.bind(this)
                    );
                }

                create_function_selector() {
                    this.function_selector = $("<div class='function-selector'> <div class='function_selecor_title'>" + this.api.name.replace(/([^])([A-Z])/g, "$1 $2") + "</div></div>")

                }
            },
            add_api: function (api) {
                programmer_api = new arduino_api_programmer.Api(api);
                arduino_api_programmer.apis.push();
                return programmer_api
            },
            add_function: function (func) {
                let e = $("<div class='programm_function_element'></div>");
                api_programmer_api_code_creator.append(e);
                e.attr("api",func.api.api.position);
                e.attr("name",func.func.name);
                e.append(func.func.input.clone()).find('button').remove()
            },
            serialize: function () {
                code=[];
                api_programmer_api_code_creator.find('.programm_function_element').each(function (i, ele) {
                    ele=$(ele);
                    let entry = {
                        api:parseInt(ele.attr("api")),
                        name:ele.attr("name"),
                        kwargs:{},
                    };

                    ele.find("[name]").each(function (i, subele) {
                       let attr = $(subele);
                        entry.kwargs[attr.attr("name")]=attr.val();
                        if(attr.attr("type") === "number")
                            entry.kwargs[attr.attr("name")]=Number(entry.kwargs[attr.attr("name")])
                    });
                    code.push(entry);
                });
                console.log(code);
            }
        };
        let pre_add_api = arduino_api_controller.add_api;
        arduino_api_controller.add_api = function (api) {
            pre_add_api(api);
            arduino_api_programmer.add_api(api);
        };

        javascriptApi = arduino_api_programmer.add_api({
            name: "js",
            functions: [],
        });
        api_programmer_api_code_creator.droppable({
            accept: ".api-function-selector",
            drop: function (even, ui) {
                if (arduino_api_programmer.dragging_function !== null) {
                    arduino_api_programmer.add_function(arduino_api_programmer.dragging_function);
                    arduino_api_programmer.dragging_function = null;
                }
            }
        });
        api_programmer_api_code_creator.sortable();
        $('#testbutton').click(arduino_api_programmer.serialize)
    }



}