$(function () {
    var thHeight = $(".table th:first").height();
    $(".table th").resizable({
        handles: "e",
        minHeight: thHeight,
        maxHeight: thHeight,
        minWidth: 40,
        resize: function (event, ui) {
            var sizerID = '.table' + "-sizer";
            $(sizerID).width(ui.size.width);
        }
    });
});

// odoo.define('table_resizable', function (require) {
//     'use strict';

//     var options = require('web_editor.snippets.options');

//     options.registry.custom_table_size = options.Class.extend({


//         start: function () {
//             var self = this;

//             // this.$el.find(".js_add").on("click", _.bind(this._add_new_tab, this));
//             // this.$el.find(".js_remove").on("click", _.bind(this._remove_current_tab, this));

//             this._super();
//         },

//         drop_and_build_snippet: function () {
//             var self = this;
//             alert('???')
//             var thHeight = $(".table th:first").height();
//             self.$target.find(".table th").resizable({
//                 handles: "e",
//                 minHeight: thHeight,
//                 maxHeight: thHeight,
//                 minWidth: 40,
//                 resize: function (event, ui) {
//                     var sizerID = ".table" + "-sizer";
//                     $(sizerID).width(ui.size.width);
//                 }
//             });
//         },
//     });

// });