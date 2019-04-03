function copyRefToClipBoard(index, refType) {
  //Get the text
  const copyText = $("." + refType + "_reference")[index].innerText;

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

  // Inform user by changing button color for t ms
  const t = 200;
  const btn = $("." + refType + "_copy_btn")[index];
  defaultColor = btn.style.background;
  btn.style.background = "rgba(37, 237, 33, 0.13)";

  setInterval(function() {
    btn.style.background = defaultColor;
  }, t);
}
