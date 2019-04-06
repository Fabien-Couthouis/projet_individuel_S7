function copyRefToClipBoard(id) {
  const btn = $("#" + id)[0];
  copy(btn.innerText);

  // Inform user by changing button color for t ms
  const t = 200;
  defaultColor = btn.style.background;
  btn.style.background = "rgba(37, 237, 33, 0.13)";

  setInterval(function() {
    btn.style.background = defaultColor;
  }, t);
}

function copyAllToClipBoard(className) {
  const btns = $("." + className);
  let copyText = "";
  for (let b = 0; b < btns.length; b++) {
    copyText += btns[b].innerText + ",";
  }

  copy(copyText);
}

function copyTextarea(id) {
  const btn = $("#" + id)[0];
  copy(btn.value);
}

function copy(copyText) {
  //Create a temp "input" element
  let tempItem = document.createElement("input");

  tempItem.setAttribute("type", "text");
  tempItem.setAttribute("display", "none");

  //Assign the value to copy and add item to the document
  tempItem.setAttribute("value", copyText);
  document.body.appendChild(tempItem);

  //Copy the text
  tempItem.select();
  document.execCommand("Copy");

  //Remove item
  document.body.removeChild(tempItem);
}
