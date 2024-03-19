function show_cnnGraph() {
  //   document.getElementById("graph1Container").classList.toggle("show");
  //   document.getElementById("graph2Container").classList.toggle("show");
  //toggling the button State
  //   const btn = document.getElementById("cnnGraph");
  //   if (btn.disabled) {
  //     btn.disabled = false;
  //   } else {
  //     btn.disabled = true;
  //   }

  document.getElementById("graph1Container").classList.remove("hide");
  document.getElementById("graph2Container").classList.remove("hide");
  document.getElementById("graphName1").innerHTML =
    "VGG Net Accuracy (Train vs Val)";
  document.getElementById("graphImg1").src =
    "../static/images/cnn_accuracy.png";
  document.getElementById("graphName2").innerHTML =
    "VGG Net Loss (Train vs Val)";
  document.getElementById("graphImg2").src = "../static/images/cnn_loss.png";
}

function show_lenetGraph() {
  //document.getElementById("graph1Container").style.display = "none";
  document.getElementById("graphName1").innerHTML =
    "LeNet5 Accuracy (Train vs Val)";
  document.getElementById("graphImg1").src =
    "../static/images/lenet_accuracy.png";
  document.getElementById("graphName2").innerHTML =
    "LeNet5 Loss (Train vs Val)";
  document.getElementById("graphImg2").src = "../static/images/lenet_loss.png";
}

function show_yoloGraph() {
  //document.getElementById("graph1Container").style.display = "none";
}
