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

// generateSecurityGroup("";
// generateEntireGraph();
// generateSingleNode("");//"");

/*
General Purpose functions that are used in each of the graph generating functions
*/


/*
This function returns true/false dependind on whether there is an overlapping of links and
if there is then it concats the ports  of the overlapping links together
For example if there exists two objects in the links array with the same source/target but
a different port then this function should combine those two objects in the links array
into a single object in the testData.links array. If there isn't any overlap then it returns false
As an input it takes the data array, the testData array and the integer k which is the index number of
the data.links array we are comparing with
*/
function nodeOverLapCheckerAndConcatenation(data,testData,k)
{         
          var m;
          var duplicateLink=false;
          for(m=0;m<testData.links.length;m++)
          {
            if(data.Links[k].source ==testData.links[m].source
              &&data.Links[k].target ==testData.links[m].target)
            {
              duplicateLink=true;
              var currentPorts = testData.links[m].ports;
              var newPorts = currentPorts.concat("--------",data.Links[k].info.port);

            testData.links[m].ports=newPorts;

              var labelShown="----Source:---"+ data.Links[k].info.source.toString()+"----Protocol:------"+data.Links[k].info.protocol.toString()+"--ports:  "+newPorts;
              
              var value="value"

            testData.links[m][value]=labelShown;
            }

          }
          return duplicateLink;
}


/*
This is a short function that creates the category types for the graph
The types consist of every kind of node in the JSON such as ec2, loadBalancers and databases
These categories will be shown in the legend

*/
function createCategories(testData)
{
      testData.categories[0] = {
        name: "ec2",
      };
      testData.categories[1] = {
        name: "loadBalancer",
      };
      testData.categories[2] = {
        name: "database",
      };
}


/*
This function creates a link and places it into the testData.links array
The oldLink boolean is there to make sure there isn't another link with the same source/target node  so we dont
make a duplicate by accident. Integer k is the index number of data.links we are referencing
*/
function createLinks(data,testData,oldLink,k)
{
  if(oldLink==false)
  {
            var portString=data.Links[k].info.port.toString();
              testData.links.push({
              source: data.Links[k].source,
              target: data.Links[k].target,
              ports: portString ,
              value: "----Source:---"+ data.Links[k].info.source.toString()+"----Protocol:------"+data.Links[k].info.protocol.toString()+"--ports:  "+portString,
              lineStyle: {
                color: "green",
                curveness: 0.3
              },
            });
          oldLink=true;
  
    }
}



/*
This function should check the testData and see if there are any Nodes that contain the same instanceID
as the current data Node we are using
It  should return true if duplicates exist
It was used mainly for error checking and is largely redundant now
Will also return true if there is an undefined Node in testData

It takes the data array, testData array and an integer i which is index i of the data.Nodes array
*/
function checkForDuplicateNodesInTestData(data,testData,i)
{
var alreadyExists=false;
  for (j = 0; j < testData.nodes.length; j++) {
    if (typeof testData.nodes[j] === "undefined") {
      console.log("testFailed");
      alreadyExists = true;
    } else if (testData.nodes[j].id == data.Nodes[i].InstanceID) {
      console.log("testFailedDueToDuplicate");
      alreadyExists = true;
    }
  }

  return alreadyExists;

}



/*
Graph Generating Functions are below
Current functions that have been implemented are:
generateEntireGraph()
generateSingleNode(nodeInput)
generateSingleSecurityGroup(securityGroup Input)
*/


function generateEntireGraph() 
{
  fetch("work.json")
    .then((response) => response.json())
    .then((data) => {



/*
This for loop iterates over the data.links array
It then adds it to the testData.links array depending on whether or not the link is a duplicate
*/
var k;
for (k = 0; k < data.Links.length; k++) 
{
        var oldLink=nodeOverLapCheckerAndConcatenation(data,testData,k);
        createLinks(data,testData,oldLink,k);

}


      var i;
      var alreadyExists = false;
      var numberOfNodes = 0;

      for (i = 0; i < data.Nodes.length; i++) {
       


        alreadyExists=checkForDuplicateNodesInTestData(data,testData,i);

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

      //Create categories
      createCategories(testData)

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
                
          
          //Calling the concatenation function for ports and returning false if the current data.links[k] has no overlap in the testData.links
          var oldLink=nodeOverLapCheckerAndConcatenation(data,testData,k);
          createLinks(data,testData,oldLink,k);



        if (data.Links[k].target == NodeID) {
          connectedNodes.push(data.Links[k].source);
        }
      }
      }
      console.log(testData.links);

      /*
This for loop iterates over the nodes array in the JSON data and converts it into a format
that echarts will accept. It will only convert the desired Nodes
*/

      for (i = 0; i < data.Nodes.length; i++) {
        
        //Ensuring there are no duplicates or undefined Nodes in testdData
        alreadyExists=checkForDuplicateNodesInTestData(data,testData,i);
        //These if statements checks that the node we want is of the correct type and if there are any duplicate or undefined nodes in the JSON
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
            symbolSize: sourceNode ? 10 : 4,
            value: 0,
            category: data.Nodes[i].Type,
            // symbol: "square",
            itemStyle: {
              color: sourceNode ? "blue" : "red",
            },
          };
          numberOfNodes++;
        }

        alreadyExists = false;
      }

      //Create categories
      createCategories(testData)

      loadChart(testData);
    });
}

function generateSecurityGroup(SecurityGroup) {
  fetch("work.json")
    .then((response) => response.json())
    .then((data) => {
      var i;
      var alreadyExists = false;
      var numberOfNodes = 0;

      /*
This for loop iterates over the  links 
It then adds it to an array of links in testData
*/
      var k;
      for (k = 0; k < data.Links.length; k++) 
      {
        var oldLink=nodeOverLapCheckerAndConcatenation(data,testData,k);
        createLinks(data,testData,oldLink,k);
      }

      /*
This for loop iterates over the nodes array in the JSON data and converts it into a format
that echarts will accept. It will only convert the desired Nodes
*/

      for (i = 0; i < data.Nodes.length; i++) {
        

        //Checking for duplicate or undefined nodes for example if data.nodes[i] has a duplicate node in testData.nodes then it returns true
        alreadyExists=checkForDuplicateNodesInTestData(data,testData,i);
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

      //Create categories
      createCategories(testData)


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

        edgeSymbol: ['circle', 'arrow'],
        edgeSymbolSize: [1, 10],

        force: {
          // repulsion: 2000,
          // edgeLength: 60
      },

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