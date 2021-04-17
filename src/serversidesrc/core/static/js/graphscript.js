var dom = document.getElementById("container");
var myChart = echarts.init(dom);
var app = {};
var option;

var testing;
var nodes = new Array();
var links = new Array();
var categories = new Array();
var testData = { nodes, links, categories };



var securityGroupsArray = ["",""];
// var portsArray=["-1"]
// generateMultiplePorts(portsArray);



myChart.showLoading();

// generateSecurityGroup("");
//generateEntireGraph();
// generateSingleNodeOutgoing("");
//  generateSingleNodeIncoming("");
// generateSingleNode();
//generateMultipleSecurityGroups(securityGroupsArray);

/*
Known Issues:


Some of the font cases will be lower case. This isn't an actual issue  but it does make it more difficult to read the code


New Instance ID entered does not refresh graph

In and out buttuns require you to type into search bar and not use history
*/


//search triggers one enter is pressed and this string is fed into generateSignleNode
var searchBar = document.getElementById('searchBar');
var search = "";
searchBar.addEventListener('keyup', (e) => {
    search = e.target.value.toLowerCase();
   // console.log(searchString);
    if (e.key === "Enter") 
    {
        generateSingleNode(search);
    }
    else if (e.key  == "ArrowLeft") {
      // left arrow
      // alert(search +" outgoing ");
      generateSingleNodeOutgoing(search);
     }
    else if (e.key  == "ArrowRight") {
      // right arrow
      // alert(search +" incoming ");
      generateSingleNodeIncoming(search);
  }
    console.log(search);
});

//functions that catch In and Out button presses
document.getElementById("incomingBtn").addEventListener("click", function() {
  //console.log(search);
  // alert(search +" IN ");
  generateSingleNodeIncoming(search);
});

document.getElementById("outgoingBtn").addEventListener("click", function() {
//console.log(search);
// alert(search +" OUT ");
generateSingleNodeOutgoing(search);
});



/*
General Purpose functions that are used in each of the graph generating functions
*/



//This empties the global arrays so other graphs can be drawn
function clearGlobalArrays()
{

          while(testData.nodes.length > 0) {
            testData.nodes.length.pop();
        }
        while(testData.links.length > 0) {
          testData.links.length.pop();
        }
        while(testData.categories.length > 0) {
          testData.categories.length.pop();
        }      

}



/*
This function returns true/false dependind on whether there is an overlapping of links and
if there is then it determines the source of the ports and protocols of that link and
adds those ports to a ports array inside the testData link it is connected to If there isn't any overlap then it returns false
As an input it takes the data array, the testData array and the integer k which is the index number of
the data.links array we are comparing with.

There are essentially two ports and protocols arrays, one is a general one we use just to check for the ports/protocols in a particular link
The second set is used to tie specific sources to specific protocols which then have specific ports on them. We only use the second set for the
edge value while the first set is used for any .include() functions.
*/
function nodeOverLapCheckerAndConcatenation(data,testData,k)
{         
          var m;
          var duplicateLink=false;
          for(m=0;m<testData.links.length;m++)
          {
            if(data.links[k].source ==testData.links[m].source
              &&data.links[k].target ==testData.links[m].target)
            {
              var newSource=true;
              var newProtocol=true;
              var p;


              testData.links[m].ports.push(data.links[k].info.port);
              testData.links[m].protocols.push(data.links[k].info.protocol);



              for(p=0;p<testData.links[m].infoSources.length;p++)
              {
                if(testData.links[m].infoSources[p].source==data.links[k].info.source)//If they have the same source//if newSource is true then we wont find any new protocols
                {
                  var t;
                  for(t=0;t<testData.links[m].infoSources[p].protoPorts.length;t++)
                  {
                    if(testData.links[m].infoSources[p].protoPorts[t].protocol==data.links[k].info.protocol)//If they have the same protocol
                    {
                      
                      testData.links[m].infoSources[p].protoPorts[t].ports.push(data.links[k].info.port.toString());
                      newProtocol=false;

                    }

                  }

                  // testData.links[m].infoSources[p].ports.push(data.links[k].info.port.toString());
                  newSource=false;
                }
              }

              if(newProtocol==true && newSource==false)//If same source but new protocol
              {
                var portString=data.links[k].info.port.toString();
                var sourcesProtocolsPorts={

                  protocol:data.links[k].info.protocol.toString(),
                  ports:[portString]
    
    
                }
                testData.links[k].infoSources.push(sourcesProtocolsPorts);//new protocol added with corresponding port
              }
              if(newSource==true)
              {
                var portString=data.links[k].info.port.toString();
                var sourcesProtocolsPorts={
    
                  protocol:data.links[k].info.protocol.toString(),
                  ports:[portString]
    
    
                }
                var infoSourcesPorts={

                  source:data.links[k].info.source.toString(),
                  protoPorts:[sourcesProtocolsPorts],
    
                }
                testData.links[m].infoSources.push(infoSourcesPorts);

              }
              duplicateLink=true;
            }

          }
          return duplicateLink;
}



/*
This function should set the value property of each and every link. It does this by accessing the
infoSources array inside each link. From that is gets the source property in each array index and adds it to value string. Then
it gets each and every protcols and their corresponding ports from the ports array alongside that source and adds it the the value string.
It repeats this process for each unique source in the infoSources Array.

*/
function setValuesOfPorts(testData)
{
  var x;
  var valueString="";
  for(x=0;x<testData.links.length;x++)//Going through the links
  {
    valueString="";
    var y;
    for(y=0;y<testData.links[x].infoSources.length;y++)//Going through the sources 
    {
      valueString=valueString +"Source:" +testData.links[x].infoSources[y].source.toString();
      var v;
      for(v=0;v<testData.links[x].infoSources[y].protoPorts.length;v++)//Going through the protocols contained inside thouse sources
      {
        valueString=valueString +"___protocol:" +testData.links[x].infoSources[y].protoPorts[v].protocol.toString()+"  __Ports    :";
        var z;
        for(z=0;z<testData.links[x].infoSources[y].protoPorts[v].ports.length;z++)//Going through the ports contained within those protocols
        {
          valueString=valueString+testData.links[x].infoSources[y].protoPorts[v].ports[z].toString()+"     :";
        }

      }
    }
    // console.log(valueString);
    testData.links[x]["value"]=valueString
  }
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
      testData.categories[3] = {
        name: "appBalancer",
      };
}



/*
This function creates a link and places it into the testData.links array
The oldLink boolean is there to make sure there isn't another link with the same source/target node  so we dont
make a duplicate by accident. Integer k is the index number of data.links we are referencing
*/
function createlinks(data,testData,oldLink,k)
{
  if(oldLink==false)
  {
            var portString=data.links[k].info.port.toString();

            var sourcesProtocolsPorts={

              protocol:data.links[k].info.protocol.toString(),
              ports:[portString]
            }

            var infoSourcesPorts={

              source:data.links[k].info.source.toString(),
               protoPorts:[sourcesProtocolsPorts],
            }
              testData.links.push({
              infoSources:[infoSourcesPorts], 
                
              source: data.links[k].source,
              target: data.links[k].target,
              protocols:[],//Not used in edge value
              ports:[],//Not used in edge value

              lineStyle: {
                color: "green",
                curveness: 0.3
              },
            });


            testData.links[testData.links.length-1].ports.push(portString);
            testData.links[testData.links.length-1].ports.push(data.links[k].info.protocol);
          oldLink=true;
  
    }
}



/*
This function creates a link and places it into the testData.links array
The oldLink boolean is there to make sure there isn't another link with the same source/target node  so we dont
make a duplicate by accident. Integer k is the index number of data.links we are referencing
*/
function createlinksContainingPorts(data,testData,oldLink,k,portsArray)
{

  var portString=data.links[k].info.port.toString();
  var containsPorts=false;
  var m;
  
  for(m=0;m<portsArray.length;m++)
  {
    if(portsArray.includes(portString))
    {
      containsPorts=true;

    }
  }


  if(oldLink==false &&containsPorts==true)
  {
            

            var sourcesProtocolsPorts={

              protocol:data.links[k].info.protocol.toString(),
              ports:[portString]
            }

            var infoSourcesPorts={

              source:data.links[k].info.source.toString(),
               protoPorts:[sourcesProtocolsPorts],
            }
              testData.links.push({
              infoSources:[infoSourcesPorts], 
                
              source: data.links[k].source,
              target: data.links[k].target,
              protocols:[],//Not used in edge value
              ports:[],//Not used in edge value

              lineStyle: {
                color: "green",
                curveness: 0.3
              },
            });


            testData.links[testData.links.length-1].ports.push(portString);
            testData.links[testData.links.length-1].ports.push(data.links[k].info.protocol);
          oldLink=true;
  
    }
}




/*
This function should check the testData and see if there are any nodes that contain the same instanceID
as the current data Node we are using
It  should return true if duplicates exist
It was used mainly for error checking and is largely redundant now
Will also return true if there is an undefined Node in testData


Due to the new JSON file containing Arns/loadbalancers not having instanceIDs on some of the  nodes this function will not work

It takes the data array, testData array and an integer i which is index i of the data.nodes array
*/
function checkForDuplicatenodesInTestData(data,testData,i)
{
var alreadyExists=false;
  for (j = 0; j < testData.nodes.length; j++) {
    if (typeof testData.nodes[j] === "undefined") {
      console.log("testFailed");
      alreadyExists = true;
    } else if (testData.nodes[j].id == data.nodes[i].InstanceID) {
      console.log("testFailedDueToDuplicate");
      alreadyExists = true;
    }
  }

  return alreadyExists;

}


/*
This function takes in the data array and an index of it and checks what type or node it is. It then returns that types corresponding
name and id
*/
function determineNameAndType(data,i)
{
              var nameTypeArray = new Array();
              //Series of if statements designed to determine the correct id of each node
              var idOfNode;
              var nameOfNode;
  
              if(data.nodes[i].type=="loadBalancer")
              {
                idOfNode=data.nodes[i].name;
                nameOfNode=data.nodes[i].name;
              }
              else if(data.nodes[i].type=="appBalancer")
              {
                
                idOfNode=data.nodes[i].arn;
                nameOfNode=data.nodes[i].name;
              }
              else if (data.nodes[i].type=="database")
              {
                idOfNode=data.nodes[i].instanceID;
                nameOfNode=data.nodes[i].name;
              }
              else if (data.nodes[i].type=="ec2")
              {
                idOfNode=data.nodes[i].instanceID;
                nameOfNode=data.nodes[i].name;
              }
              nameTypeArray.push(idOfNode);
              nameTypeArray.push(nameOfNode);

              return nameTypeArray;
}




/*
Graph Generating Functions are below
Current functions that have been implemented are:
generateEntireGraph()
generateSingleNode(nodeInput)
generateSingleNodeIncoming(nodeInput)
generateSingleNodeOutgoing(nodeInput)
generateSecurityGroup(securityGroup Input String)
generateMultipleSecurityGroups(securityGroup Input Array)
*/


function generateEntireGraph() 
{
  fetch("work.json")
    .then((response) => response.json())
    .then((data) => {
      clearGlobalArrays();
/*
This for loop iterates over the data.links array
It then adds it to the testData.links array depending on whether or not the link is a duplicate
*/
      var k;
      for (k = 0; k < data.links.length; k++) 
      {
              var oldLink=nodeOverLapCheckerAndConcatenation(data,testData,k);
              createlinks(data,testData,oldLink,k);
      }
      var i;
      var numberOfnodes = 0;

      console.log(data)
      for (i = 0; i < data.nodes.length; i++) 
      {

             /*
              Creating a new array of nodes using the input JSON file
              I used the numberOfnodes variable because It made debugging easier
            */


            var idOfNode;
            var nameOfNode;
            var nameAndTypeArray= new Array();
            nameAndTypeArray =  determineNameAndType(data,i);
            idOfNode=nameAndTypeArray[0];
            nameOfNode=nameAndTypeArray[1];




          testData.nodes[numberOfnodes] = {
            id: idOfNode,
            name: nameOfNode,
            symbolSize: 0.2,
            value: 0,
            category: data.nodes[i].type,
            symbol: "square",
          };

          //Incrementing the number of nodes
          numberOfnodes++;
        // }

        alreadyExists = false;
      }

      //Create categories
      createCategories(testData)
      setValuesOfPorts(testData)
      console.log(testData);

      loadChart(testData);
    });
}




function generateSingleNode(NodeID){
  fetch("work.json")
  .then((response) => response.json())
  .then((data) => {
    clearGlobalArrays();
    var i;
    var numberOfnodes = 0;

    /*
   This for loop iterates over the  links and identifies any node connected with the source Node.
    It then adds it to an array of connectednodes
   */

    var connectednodes = new Array();
    connectednodes.push(NodeID); //Source Node

    
    var k;
    for (k = 0; k < data.links.length; k++) {
        if (data.links[k].target == NodeID || data.links[k].source == NodeID) 
        {
          if (data.links[k].target == NodeID)
          {
            connectednodes.push(data.links[k].source);
          }
          else{
            connectednodes.push(data.links[k].target);
          }
            
        //Calling the concatenation function for ports and returning false if the current data.links[k] has no overlap in the testData.links
        var oldLink=nodeOverLapCheckerAndConcatenation(data,testData,k);
        createlinks(data,testData,oldLink,k);
    }
    }
    console.log(testData.links);

    /*
This for loop iterates over the nodes array in the JSON data and converts it into a format
that echarts will accept. It will only convert the desired nodes
*/

    for (i = 0; i < data.nodes.length; i++) {


      var idOfNode;
      var nameOfNode;
      var nameAndTypeArray= new Array();
      nameAndTypeArray =  determineNameAndType(data,i);
      idOfNode=nameAndTypeArray[0];
      nameOfNode=nameAndTypeArray[1];
      

      if ( connectednodes.includes(idOfNode)) 
      {


        /*
              Creating a new array of nodes using the input JSON file
              Includes a short if statement that checks if is the source Node
        */
        var sourceNode;
        if (idOfNode == NodeID) {
          sourceNode = true;
        } else {
          sourceNode = false;
        }

        testData.nodes[numberOfnodes] = {
          id: idOfNode,
          name: nameOfNode,
          symbolSize: sourceNode ? 10 : 4,
          value: 0,
          category: data.nodes[i].type,
          // symbol: "square",
          itemStyle: {
            color: sourceNode ? "blue" :  "#cf6dca",
          },
        };
        numberOfnodes++;
      
    }
  }

    
    createCategories(testData)
    setValuesOfPorts(testData)

  // console.log(testData);

    loadChart(testData);
  });




}





function generateSingleNodeOutgoing(NodeID) {
  fetch("graph_data")
    .then((response) => response.json())
    .then((data) => {
      clearGlobalArrays();
      var i;
      var numberOfnodes = 0;

      /*
     This for loop iterates over the  links and identifies any node connected with the source Node.
      It then adds it to an array of connectednodes
     */

      var connectednodes = new Array();
      connectednodes.push(NodeID); //Source Node

      
      var k;
      for (k = 0; k < data.links.length; k++) {
        if (data.links[k].source == NodeID) 
        {
          connectednodes.push(data.links[k].target);
                     
          //Calling the concatenation function for ports and returning false if the current data.links[k] has no overlap in the testData.links
          var oldLink=nodeOverLapCheckerAndConcatenation(data,testData,k);
          createlinks(data,testData,oldLink,k);
      }
      }
      console.log(testData.links);

      /*
This for loop iterates over the nodes array in the JSON data and converts it into a format
that echarts will accept. It will only convert the desired nodes
*/

      for (i = 0; i < data.nodes.length; i++) {


        var idOfNode;
        var nameOfNode;
        var nameAndTypeArray= new Array();
        nameAndTypeArray =  determineNameAndType(data,i);
        idOfNode=nameAndTypeArray[0];
        nameOfNode=nameAndTypeArray[1];
        

        if ( connectednodes.includes(idOfNode)) 
        {


          /*
                Creating a new array of nodes using the input JSON file
                Includes a short if statement that checks if is the source Node
          */
          var sourceNode;
          if (idOfNode == NodeID) {
            sourceNode = true;
          } else {
            sourceNode = false;
          }

          testData.nodes[numberOfnodes] = {
            id: idOfNode,
            name: nameOfNode,
            symbolSize: sourceNode ? 10 : 4,
            value: 0,
            category: data.nodes[i].type,
            // symbol: "square",
            itemStyle: {
              color: sourceNode ? "blue" : "#a738e8", //purple
            },
          };
          numberOfnodes++;
        
      }
    }

      
      createCategories(testData)
      setValuesOfPorts(testData)
      loadChart(testData);
    });
}

function generateSingleNodeIncoming(NodeID){
  fetch("graph_data")
  .then((response) => response.json())
  .then((data) => {
    clearGlobalArrays();
    var i;
    var numberOfnodes = 0;

    /*
   This for loop iterates over the  links and identifies any node connected with the source Node.
    It then adds it to an array of connectednodes
   */

    var connectednodes = new Array();
    connectednodes.push(NodeID); //Source Node

    
    var k;
    for (k = 0; k < data.links.length; k++) {
      if (data.links[k].target == NodeID ) 
      {
        connectednodes.push(data.links[k].source);
                   
        //Calling the concatenation function for ports and returning false if the current data.links[k] has no overlap in the testData.links
        var oldLink=nodeOverLapCheckerAndConcatenation(data,testData,k);
        createlinks(data,testData,oldLink,k);
    }
    }
    console.log(testData.links);

    /*
This for loop iterates over the nodes array in the JSON data and converts it into a format
that echarts will accept. It will only convert the desired nodes
*/

    for (i = 0; i < data.nodes.length; i++) {


      var idOfNode;
      var nameOfNode;
      var nameAndTypeArray= new Array();
      nameAndTypeArray =  determineNameAndType(data,i);
      idOfNode=nameAndTypeArray[0];
      nameOfNode=nameAndTypeArray[1];
      

      if ( connectednodes.includes(idOfNode)) 
      {


        /*
              Creating a new array of nodes using the input JSON file
              Includes a short if statement that checks if is the source Node
        */
        var sourceNode;
        if (idOfNode == NodeID) {
          sourceNode = true;
        } else {
          sourceNode = false;
        }

        testData.nodes[numberOfnodes] = {
          id: idOfNode,
          name: nameOfNode,
          symbolSize: sourceNode ? 10 : 4,
          value: 0,
          category: data.nodes[i].type,
          // symbol: "square",
          itemStyle: {
            color: sourceNode ? "blue" : "red",
          },
        };
        numberOfnodes++;
      
    }
  }

    
    createCategories(testData)
    setValuesOfPorts(testData)
    loadChart(testData);
  });




}










function generateSecurityGroup(securityGroups) {
  fetch("graph_data")
    .then((response) => response.json())
    .then((data) => {
      clearGlobalArrays();
      var i;
      var numberOfnodes = 0;

      //CreateLinks in testData.links
      var k;
      for (k = 0; k < data.links.length; k++) 
      {
        var oldLink=nodeOverLapCheckerAndConcatenation(data,testData,k);
        createlinks(data,testData,oldLink,k);
      }


      //Create Nodes in testData.nodes
      for (i = 0; i < data.nodes.length; i++) {
        

        if ( data.nodes[i].securityGroups.includes(securityGroups)) {

          var idOfNode;
          var nameOfNode;
          var nameAndTypeArray= new Array();
          nameAndTypeArray =  determineNameAndType(data,i);
          idOfNode=nameAndTypeArray[0];
          nameOfNode=nameAndTypeArray[1];

          //Creating the node
          testData.nodes[numberOfnodes] = {
            id: idOfNode,
            name: nameOfNode,
            symbolSize: 3,
            value: 0,
            category: data.nodes[i].type,
            symbol: "square",
            
          };
          numberOfnodes++;
        }
      }

      //Create categories
      createCategories(testData)
      setValuesOfPorts(testData)

      console.log(testData);

      loadChart(testData);
    });
}




function generateMultipleSecurityGroups(securityGroups) {
  fetch("graph_data")
    .then((response) => response.json())
    .then((data) => {
      clearGlobalArrays();
      var i;
      var numberOfnodes = 0;

      var k;
      for (k = 0; k < data.links.length; k++) 
      {
        var oldLink=nodeOverLapCheckerAndConcatenation(data,testData,k);
        createlinks(data,testData,oldLink,k);
      }

      //Create Nodes in testData.nodes
      for (i = 0; i < data.nodes.length; i++) {


        //Short for loop to determine if the node contains the some of the required securityGroups
        var containsSecurityGroup=false;
        var t;
        var sg;
        for(t=0;t<securityGroups.length;t++)
        {
          sg=securityGroups[t];
         if( data.nodes[i].securityGroups.includes(sg))
         {
          containsSecurityGroup=true;
         }
        }


        if ( containsSecurityGroup==true) {

          var idOfNode;
          var nameOfNode;
          var nameAndTypeArray= new Array();
          nameAndTypeArray =  determineNameAndType(data,i);
          idOfNode=nameAndTypeArray[0];
          nameOfNode=nameAndTypeArray[1];

          //Creating the node
          testData.nodes[numberOfnodes] = {
            id: idOfNode,
            name: nameOfNode,
            symbolSize: 3,
            value: 0,
            category: data.nodes[i].type,
            symbol: "square",
            
          };
          numberOfnodes++;
        }
      }
      console.log(testData);

      //Create categories
      createCategories(testData)
      setValuesOfPorts(testData)

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
      text: "",
      subtext: " ",
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
          repulsion: 100,
          edgeLength: 250
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