/*------------------------------------------------------
    Author : www.webthemez.com
    License: Commons Attribution 3.0
    http://creativecommons.org/licenses/by/3.0/
---------------------------------------------------------  */

(function ($) {
    "use strict";
    var mainApp = {

        

        initFunction: function () {
            /*MENU 
            ------------------------------------*/
            $('#main-menu').metisMenu();
			
            $(window).bind("load resize", function () {
                if ($(this).width() < 768) {
                    $('div.sidebar-collapse').addClass('collapse')
                } else {
                    $('div.sidebar-collapse').removeClass('collapse')
                }
            });

            

        var data1;
        fetch('http://172.24.135.30:8000/dup/count/00b392fd-c977-4be5-bf20-54c43a3a2a13/').then(function(response) {
            response.json().then(function(res) {
                console.log(res);
                data1 = res;
                chart_bar();
            })
            data1 = JSON.stringify(response);
           
        }, function (){

        });

        function chart_bar() {
            Morris.Bar({
                element: 'morris-bar-chart',
                data: data1,
                xkey: 'audio' ,
                ykeys: ['audio', 'businessobjects'],
                labels: ['audio', 'businessobjects', 'audio'],
                 barColors: [
    '#006400','#24C2CE',
    '#A8E9DC' 
  ],
                hideHover: 'auto',
                resize: true
            });
        };

                        Morris.Bar({
                element: 'morris-bar-chart2',
                data: [{
                    "total": 3215,
                    "essential": 61,
                    "non_essential": 3154
                   
                }],
                xkey: 'total',
                ykeys: ['essential', 'non_essential'],
                labels: ['Essential', 'Non Essential'],
                 barColors: [
    '#006400','#24C2CE',
    '#A8E9DC' 
  ],
                hideHover: 'auto',
                resize: true
            });
     
            
            fetch('http://172.24.135.30:8000/dup/count/00b392fd-c977-4be5-bf20-54c43a3a2a13/').then(function(response) {
                response.json().then(function(res) {
                    console.log(res);
                    data1 = res;
                    donut();
                })
                data1 = JSON.stringify(response);
               
            }, function (){
    
            });


            /* MORRIS DONUT CHART
            ----------------------------------------*/
            
            function donut() {
                Morris.Donut({
                    element: 'morris-donut-chart',
                    data: [{
                        label: "Download Sales",
                        value: 12
                    }, {
                        label: "In-Store Sales",
                        value: 30
                    }, {
                        label: "Mail-Order Sales",
                        value: 20
                    }],
                       colors: [
        '#A6A6A6','#24C2CE',
        '#A8E9DC' 
      ],
                    resize: true
                });
            }


            var data_nonlinked;
            fetch('http://172.24.135.30:8000/allnonessential/00b392fd-c977-4be5-bf20-54c43a3a2a13').then(function(response) {
                response.json().then(function(res) {
                    console.log(res);
                    data_nonlinked = res;
                    area_chart();
                })
                data1 = JSON.stringify(response);
               
            }, function (){
    
            });

            /* MORRIS AREA CHART
			----------------------------------------*/
            function area_chart() {
                Morris.Area({
                    element: 'morris-area-chart',
                    data: data_nonlinked,
                    xkey: 'folder',
                    ykeys: ['total', 'essential', "inon-essential"],
                    labels: ['total', 'essential', "inon-essential"],
                    pointSize: 2,
                    hideHover: 'auto',
                      pointFillColors:['#ffffff'],
                      pointStrokeColors: ['black'],
                      lineColors:['#A6A6A6','#24C2CE'],
                    resize: true
                });
    
                /* MORRIS LINE CHART
                ----------------------------------------*/
                Morris.Line({
                    element: 'morris-line-chart',
                    data: [
                          { y: '2014', a: 50, b: 90},
                          { y: '2015', a: 165,  b: 185},
                          { y: '2016', a: 150,  b: 130},
                          { y: '2017', a: 175,  b: 160},
                          { y: '2018', a: 80,  b: 65},
                          { y: '2019', a: 90,  b: 70},
                          { y: '2020', a: 100, b: 125},
                          { y: '2021', a: 155, b: 175},
                          { y: '2022', a: 80, b: 85},
                          { y: '2023', a: 145, b: 155},
                          { y: '2024', a: 160, b: 195}
                    ],
                
                     
          xkey: 'y',
          ykeys: ['a', 'b'],
          labels: ['Total Income', 'Total Outcome'],
          fillOpacity: 0.6,
          hideHover: 'auto',
          behaveLikeLine: true,
          resize: true,
          pointFillColors:['#ffffff'],
          pointStrokeColors: ['black'],
          lineColors:['gray','#24C2CE']
          
                });
            }
           
        
            $('.bar-chart').cssCharts({type:"bar"});
            $('.donut-chart').cssCharts({type:"donut"}).trigger('show-donut-chart');
            $('.line-chart').cssCharts({type:"line"});

            $('.pie-thychart').cssCharts({type:"pie"});
       
	 
        },

        initialization: function () {
            mainApp.initFunction();

        }

    }
    // Initializing ///


    $(document).ready(function () {
        mainApp.initFunction(); 
		$("#sideNav").click(function(){
			if($(this).hasClass('closed')){
				$('.navbar-side').animate({left: '0px'});
				$(this).removeClass('closed');
				$('#page-wrapper').animate({'margin-left' : '260px'});
				
			}
			else{
			    $(this).addClass('closed');
				$('.navbar-side').animate({left: '-260px'});
				$('#page-wrapper').animate({'margin-left' : '0px'}); 
			}
		});
    });

}(jQuery));
