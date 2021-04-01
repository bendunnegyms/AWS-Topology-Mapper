var dom = document.getElementById("container");
var myChart = echarts.init(dom);
var app = {};
var option;

var testing;
var nodes = new Array();
var links = new Array();
var categories = new Array();
var testData = { nodes, links, categories };

myChart.showLoading();

// generateSecurityGroup("sampleSecurityGroup");
// generateEntireGraph();
generateSingleNode("i-0ab8089c913441c31");
function generateEntireGraph() {
  fetch("work.json")
    .then((response) => response.json())
    .then((data) => {

      var i;
      var alreadyExists = false;
      var numberOfNodes = 0;

      for (i = 0; i < data.Nodes.length; i++) {
        var j;

        //This for loop checks for errors in the JSON that would cause echarts to stop working such as duplicates
        for (j = 0; j < testData.nodes.length; j++) {
          if (typeof testData.nodes[j] === "undefined") {
            console.log("testFailed");
            alreadyExists = true;
          } else if (testData.nodes[j].id == data.Nodes[i].InstanceID) {
            alreadyExists = true;
          }
        }

        //This creates the nodes using the information from the JSON and inputs the nodes into the testData array
        if (
          alreadyExists == false &&
          (data.Nodes[i].Type == "ec2" ||
            data.Nodes[i].Type == "database")
        ) {
          if (typeof data.Nodes[i].InstanceID === "undefined") {
            //testing if instance is undefined
            console.log("testFailedTwice");
          } else if (typeof data.Nodes[i] === "undefined") {
            //testing if node itself is undefined
            console.log("testFailedagain");
          }

          /*
              Creating a new array of nodes using the input JSON file
              I used the numberOfNodes variable because It made debugging easier
            */

          testData.nodes[numberOfNodes] = {
            id: data.Nodes[i].InstanceID,
            name: data.Nodes[i].Name,
            symbolSize: 0.2,
            value: 0,
            category: data.Nodes[i].Type,
            symbol: "square",
          };

          //Incrementing the number of Nodes
          numberOfNodes++;
        }

        alreadyExists = false;
      }

      //Fills the testData links array with the data from the JSON links array
      var k;
      for (k = 0; k < data.Links.length; k++) {
        testData.links[k] = {
          source: data.Links[k].source,
          target: data.Links[k].target,
        };
      }

      //Required types that will be shown in the legend
      testData.categories[0] = {
        name: "ec2",
      };
      testData.categories[1] = {
        name: "loadBalancer",
      };
      testData.categories[2] = {
        name: "database",
      };

      loadChart(testData);
    });
}

function generateSingleNode(NodeID) {
  fetch("work.json")
    .then((response) => response.json())
    .then((data) => {
      var i;
      var alreadyExists = false;
      var numberOfNodes = 0;

      /*
     This for loop iterates over the  links and identifies any node connected with the source Node.
      It then adds it to an array of connectedNodes
     */

      var connectedNodes = new Array();
      connectedNodes.push(NodeID); //Source Node
      var k;
      for (k = 0; k < data.Links.length; k++) {
        if (data.Links[k].source == NodeID) {
          connectedNodes.push(data.Links[k].target);
          testData.links.push({
            source: data.Links[k].source,
            target: data.Links[k].target,
            lineStyle: {
              color: "green",
            },
          });
        }
        if (data.Links[k].target == NodeID) {
          connectedNodes.push(data.Links[k].source);
        }
      }

      /*
This for loop iterates over the nodes array in the JSON data and converts it into a format
that echarts will accept. It will only convert the desired Nodes
*/

      for (i = 0; i < data.Nodes.length; i++) {
        var j;
        //For loop that prevents undefined errors among nodes and also identifies if there are any duplicate Nodes in our testData array
        for (j = 0; j < testData.nodes.length; j++) {
          if (typeof testData.nodes[j] === "undefined") {
            console.log("testFailed");
            alreadyExists = true;
          } else if (testData.nodes[j].id == data.Nodes[i].InstanceID) {
            alreadyExists = true;
          }
        }
        //This if statement checks that the node we want is of the correct type and if there are any duplicate or undefined nodes in the JSON
        if (
          alreadyExists == false &&
          (data.Nodes[i].Type == "ec2" ||
            data.Nodes[i].Type == "database") &&
          
          connectedNodes.includes(data.Nodes[i].InstanceID)
        ) {
          //Second tests to help with debugging
          if (typeof data.Nodes[i].InstanceID === "undefined") {
            //testing if instance is undefined
            console.log("testFailedTwice");
          } else if (typeof data.Nodes[i] === "undefined") {
            //testing if node itself is undefined
            console.log("testFailedagain");
          }

          /*

              Creating a new array of nodes using the input JSON file
                Includes a short if statement that checks if is the source Node
              */
          var sourceNode;
          if (data.Nodes[i].InstanceID == NodeID) {
            sourceNode = true;
          } else {
            sourceNode = false;
          }

          testData.nodes[numberOfNodes] = {
            id: data.Nodes[i].InstanceID,
            name: data.Nodes[i].Name,
            symbolSize: sourceNode ? 4 : 1,
            value: 0,
            category: data.Nodes[i].Type,
            symbol: "square",
            itemStyle: {
              color: sourceNode ? "blue" : "red",
            },
          };
          numberOfNodes++;
        }

        alreadyExists = false;
      }

      testData.categories[0] = {
        name: "ec2",
      };
      testData.categories[1] = {
        name: "loadBalancer",
      };
      testData.categories[2] = {
        name: "database",
      };
      loadChart(testData);
    });
}

function generateSecurityGroup(SecurityGroup) {
  fetch("work.json")
    .then((response) => response.json())
    .then((data) => {
      var i;
      var xPos;
      var yPos;
      var alreadyExists = false;
      var numberOfNodes = 0;

      /*
This for loop iterates over the  links 
It then adds it to an array of links in the form of source and target
*/
      var k;
      for (k = 0; k < data.Links.length; k++) {
        testData.links.push({
          source: data.Links[k].source,
          target: data.Links[k].target,
          lineStyle: {
            color: "green",
          },
        });
      }

      /*
This for loop iterates over the nodes array in the JSON data and converts it into a format
that echarts will accept. It will only convert the desired Nodes
*/

      for (i = 0; i < data.Nodes.length; i++) {
        var j;

        //For loop that prevents undefined errors among nodes and also identifies if there are any duplicate Nodes in our testData array
        for (j = 0; j < testData.nodes.length; j++) {
          if (typeof testData.nodes[j] === "undefined") {
            console.log("testFailed");
            alreadyExists = true;
          } else if (testData.nodes[j].id == data.Nodes[i].InstanceID) {
            alreadyExists = true;
          }
        }
        //This if statement checks that the node we want is of the correct type and if there are any duplicate or undefined nodes in the JSON
        if (
          alreadyExists == false &&
          (data.Nodes[i].Type == "ec2" ||
            data.Nodes[i].Type == "database") &&
          data.Nodes[i].SecurityGroups.includes(SecurityGroup)
        ) {
          if (typeof data.Nodes[i].InstanceID === "undefined") {
            //testing if instance is undefined
            console.log("testFailedTwice");
          } else if (typeof data.Nodes[i] === "undefined") {
            //testing if node itself is undefined
            console.log("testFailedagain");
          }
          //Creating the node
          testData.nodes[numberOfNodes] = {
            id: data.Nodes[i].InstanceID,
            name: data.Nodes[i].Name,
            symbolSize: 3,
            value: 0,
            category: data.Nodes[i].Type,
            symbol: "square",
          };

          //Incrementing the number of Nodes
          numberOfNodes++;
        }

        alreadyExists = false;
      }

      testData.categories[0] = {
        name: "ec2",
      };
      testData.categories[1] = {
        name: "loadBalancer",
      };
      testData.categories[2] = {
        name: "database",
      };

      console.log(testData);

      loadChart(testData);
    });
}

function loadChart(graph) {
  myChart.hideLoading();

  graph.nodes.forEach(function (node) {
    node.label = {
      show: node.symbolSize > 0.1,
    };
  });
  option = {
    Animation: "false",
    coordinateSystem: "cartesian2d", //added in
    title: {
      text: "EdgeScan Graph",
      subtext: "Default layout",
      top: "bottom",
      left: "right",
    },
    tooltip: {},
    legend: [
      {
        // selectedMode: 'single',
        data: graph.categories.map(function (a) {
          return a.name;
        }),
      },
    ],
    animationDuration: 1500,
    animationEasingUpdate: "quinticInOut",
    series: [
      {
        name: "EdgeScan Graph",
        type: "graph",
        layout: "force", //"none",
        data: graph.nodes,
        links: graph.links,
        categories: graph.categories,
        roam: true,
        label: {
          position: "right",
          formatter: "{b}",
        },
        lineStyle: {
          color: "source",
          curveness: 0.3,
        },
        emphasis: {
          focus: "adjacency",
          lineStyle: {
            width: 10,
          },
        },
      },
    ],
  };

  myChart.setOption(option);
}

if (option && typeof option === "object") {
  myChart.setOption(option);
}