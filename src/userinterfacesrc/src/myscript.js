fetch('test.json')
  .then(response => response.json())
  .then(data => loadChart(data));


function loadChart(myJsonStuff){
  console.log(myJsonStuff)
  var myChart = echarts.init(document.getElementById('chart1'));
  var data = new Array();
  var i=0;
  var xPos=0;
  var yPos=0;

  for(i=0;i<myJsonStuff.Instances.length;i++) //This goes through each instance
  {
      xPos=xPos+50;
      if(xPos >500)
      {
          xPos=0;
          yPos=yPos+50;
      }
      
      data[i]=
      {
        name:myJsonStuff.Instances[i].InstanceID, 
        label:myJsonStuff.Instances[i].Name, 
        IP:myJsonStuff.Instances[i].IPAddress,
        x: (xPos),y:(yPos)
      }                                                                         
  }

          // specify chart configuration item and data
      option = {
          
      title: {
          text: 'Graph graphTest'
      },
      tooltip: {},
      animationDurationUpdate: 1500,
      animationEasingUpdate: 'quinticInOut',
      
          series: [
          {
              tooltip:{
                  fontSize:10
              },
              type: 'graph',
              layout: 'none',
              symbolSize: 50,
              roam: true,
              label: {
                  show: true
              },
              edgeSymbol: ['circle', 'arrow'],
              edgeSymbolSize: [4, 10],
              edgeLabel: {
                  fontSize: 20
              },
              data:data,
              // links: [],
              links: [],
              lineStyle: {
                  opacity: 0.9,
                  width: 2,
                  curveness: 0
              }
          }
      ]
  };

// option && myChart.setOption(option);
myChart.setOption(option);
}
