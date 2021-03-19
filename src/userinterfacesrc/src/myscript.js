fetch('test.json')
  .then(response => response.json())
  .then(data => doshit(data));

function doshit(data){
  data.map(d=>console.log(d.Description))
}

function loadChart(){
  el = document.getElementById('chart1')
  el.innerHTML = "<h2>This would be your chart</h2>"


//   new Chart(data)
}
