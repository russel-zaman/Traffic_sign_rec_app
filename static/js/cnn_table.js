function cnn_table() {
  fetch("/get_cnn_report")
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("cnn-table").innerHTML = data.cnn_table;
      document.getElementById("cnn-table").classList.add("scrollable");
    });
}
