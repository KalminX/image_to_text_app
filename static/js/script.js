function copyText() {
  const textArea = document.getElementById("extractedText");
  textArea.select();
  textArea.setSelectionRange(0, 999999); // For mobile
  document.execCommand("copy");
  alert("Copied to clipboard!");
}
function showLoader() {
  document.getElementById("loader").style.display = "block";
}
