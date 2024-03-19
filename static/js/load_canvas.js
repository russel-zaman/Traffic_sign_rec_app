//canvas test
function load_canvas() {
  console.log("in load_canvas");
  const file = document.getElementById("i_files").files[0];

  if (!file) return;

  const reader = new FileReader();

  reader.readAsDataURL(file);

  reader.onload = function (event) {
    const imgElement = document.createElement("img");
    imgElement.src = event.target.result;
    //document.getElementById("input").src = event.target.result;

    imgElement.onload = function (e) {
      const canvas = document.createElement("canvas");
      const MAX_WIDTH = 416;

      const scaleSize = MAX_WIDTH / e.target.width;
      canvas.width = MAX_WIDTH;
      canvas.height = e.target.height * scaleSize;

      const ctx = canvas.getContext("2d");

      ctx.drawImage(e.target, 0, 0, canvas.width, canvas.height);

      const srcEncoded = ctx.canvas.toDataURL(e.target, "image/jpeg");

      // you can send srcEncoded to the server
      document.querySelector("#imageBox1").src = srcEncoded;
    };
  };
}
