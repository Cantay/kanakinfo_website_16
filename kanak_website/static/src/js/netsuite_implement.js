odoo.define('kanak_website.netsuite_implement', function(require) {
    "use strict";

    var ajax = require('web.ajax');


    $(document).ready(function() {

      //   $(document).ready(function(){
      // $("#hide").click(function(){
      //   $("p").hide();
      // });
      $("#project_management").click(function(ev) {
          $(".MS-content button").css({ "background-color": "white", "color": "black" });
          $("#project_management").css({ "background-color": "#153e69", "color": "white" });
          $("#showp div").hide();
          $("#showp .active").hide();
          $("#project_management_content").show();


      });
      $("#project_planning").click(function(ev) {
          $(".MS-content button").css({ "background-color": "white", "color": "black" });
          $("#project_planning").css({ "background-color": "#153e69", "color": "white" });
          $("#showp div").hide();
          $("#showp .active").hide();
          $("#project_planning_content").show();
      });
      $("#integration_of_data").click(function(ev) {
          $(".MS-content button").css({ "background-color": "white", "color": "black" });
          $("#integration_of_data").css({ "background-color": "#153e69", "color": "white" });
          $("#showp div").hide();
          $("#showp .active").hide();
          $("#integration_of_data_content").show();
      });
      $("#quality_of_the_data").click(function(ev) {
          $(".MS-content button").css({ "background-color": "white", "color": "black" });
          $("#quality_of_the_data").css({ "background-color": "#153e69", "color": "white" });
          $("#showp div").hide();
          $("#showp .active").hide();
          $("#quality_of_the_data_content").show();
      });
      $("#change_management").click(function(ev) {
          $(".MS-content button").css({ "background-color": "white", "color": "black" });
          $("#change_management").css({ "background-color": "#153e69", "color": "white" });
          $("#showp div").hide();
          $("#showp .active").hide();
          $("#change_management_content").show();
      });
      $("#cost_invades").click(function(ev) {
          $(".MS-content button").css({ "background-color": "white", "color": "black" });
          $("#cost_invades").css({ "background-color": "#153e69", "color": "white" });
          $("#showp div").hide();
          $("#showp .active").hide();
          $("#cost_invades_content").show();
      });
      $("#ceaseless_improvement").click(function(ev) {
          $(".MS-content button").css({ "background-color": "white", "color": "black" });
          $("#ceaseless_improvement").css({ "background-color": "#153e69", "color": "white" });
          $("#showp div").hide();
          $("#showp .active").hide();
          $("#ceaseless_improvement_content").show();
      });
    
    });

});