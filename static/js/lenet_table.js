function lenet_table() {
  fetch("/get_lenet_report")
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("lenet-table").innerHTML = data.lenet_table;
      document.getElementById("lenet-table").classList.add("scrollable");
      document.getElementById("lenet-table").classList.add("content-table");
    });
}
