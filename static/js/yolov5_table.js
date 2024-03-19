function recall_table() {
  fetch("/get_recall_report")
    .then((response) => response.json())
    .then((data) => {
      // Add header row to table
      // let tableHTML =
      //   '<thead><tr><th colspan="3">Recall</th></tr></thead>' +
      //   data.recall_table;
      document.getElementById("recall-table").innerHTML = data.recall_table;
      document.getElementById("recall-table").classList.add("scrollable");
      document.getElementById("recall-table").classList.add("content-table");
    });
}

function precision_table() {
  fetch("/get_precision_report")
    .then((response) => response.json())
    .then((data) => {
      // Add header row to table
      // let tableHTML =
      //   '<thead><tr><th colspan="3">Recall</th></tr></thead>' +
      //   data.recall_table;
      document.getElementById("precision-table").innerHTML =
        data.precision_table;
      document.getElementById("precision-table").classList.add("scrollable");
      document.getElementById("precision-table").classList.add("content-table");
    });
}
