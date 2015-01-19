

  
//google.load("visualization", "1", {packages:["corechart"]});
google.load("visualization", "1.1", {packages:["bar"]});
google.setOnLoadCallback(drawChart);
function drawChart() {

    var jsonData = $.ajax({
        url: "data.json",
        dataType:"json",
        async: false
    }).responseText;
 
  var data = new google.visualization.DataTable(jsonData);
  
  //var chart = new google.visualization.Gauge(document.getElementById('chart_div'));

var options = {
          width: 700,
          chart: {
            title: 'Progress towards Test Site',
            subtitle: 'Videos on the right axis'
          },
          series: {
            0: { axis: 'left', label: 'Crowdin' }, 
            1: { axis: 'left', label: 'Subtitles' }, 
            2: { axis: 'right',label: 'Videos' }
          },
          axes: {
            y: {
              left: {label: 'Strings'}, // Left y-axis.
              right: {side: 'right', } // Right y-axis.
            }
          }
        };


  //var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
  var chart = new google.charts.Bar(document.getElementById('chart_div'));


  chart.draw(data, options);

}
  
