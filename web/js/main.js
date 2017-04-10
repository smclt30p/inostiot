
var graph = null
var data = null
var rowNumber = 0
var timebase = 500
var ip = ""
var running = false
var runner = null

var options = {
    'vAxis': {
      'title': 'Sensor value (raw)',
      'minValue': 0,
      'maxValue': 1024
    }, "hAxis": { "textPosition": 'none' }
}

google.charts.load("current", {"packages":["corechart"]});
google.charts.setOnLoadCallback(function() {

    graph = new google.visualization.LineChart(document.getElementById("graph_cont"))

    clearData();
    graph.draw(data, options);

});

function clearData() {


      data = new google.visualization.DataTable();

      data.addColumn("number", "Sensor data");
      data.addColumn("number", "Sensor 0");
      data.addColumn("number", "Sensor 1");
      data.addColumn("number", "Sensor 2");
      data.addColumn("number", "Sensor 3");
      data.addColumn("number", "Sensor 4");
      data.addColumn("number", "Sensor 5");

      graph.draw(data, options);

}

function queryServer(done) {
    
    $.ajax( "http://"+ ip +"/api?port=0,1,2,3,4,5").then(function(data) {
        done(data);
    }, function() {
        clearInterval(runner);
    })

}

function probe_server(ip, callback) {


  $.ajax("http://" + ip + "/api?version").then(function(data) {

    json = JSON.parse(data);

    if (json.status == "OK") {
      document.cookie = ip;
      callback();
    } else {
      alert("Invalid server!");
    }

  }, function() {
    alert("Invalid server!");
  });

}

function bodyLoaded() {

    var inputField = document.getElementById("time_in");
    var frequency = document.getElementById("frequency");
    frequency.innerHTML = "Frquency: " + (1 / (timebase / 1000)) + "Hz";
    inputField.value = timebase;

    $("#ip_address").val(document.cookie);

    $("#start").click(function() {

        ip = $("#ip_address").val()

        if (ip.length == 0) {
            return;
        }

        probe_server(ip, function() {

            if (!running) {

                $("#start").html("Stop monitor");

                runner = setInterval(function() {

                    queryServer(function(callback) {

                        if (rowNumber > 60) {
                            data.removeRow(0);
                        }

                        json = JSON.parse(callback);
                        temp = [];
                        temp.push(rowNumber);

                        for (var i = 0; i < json.rdata.length; i++) {
                            temp.push(json.rdata[i].value);
                        }

                        data.addRow(temp);
                        graph.draw(data, options);

                        rowNumber++;

                    });

                }, timebase);

                self.running = true;

            } else {

                $("#start").html("Start worker");
                clearInterval(runner);
                running = false
                rowNumber = 0
                clearData();
            }

        });

    })

    $("#timebase").click(function() {
      timebase = parseInt($("#time_in").val());
      var frequency = document.getElementById("frequency");
      frequency.innerHTML = "Frquency: " + (1 / (timebase / 1000)) + "Hz";
    });
    
}