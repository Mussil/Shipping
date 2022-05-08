function showspinner() {
    document.body.style = "overflow: hidden;margin: 0;";
  
    const lockModal = document.getElementById("lock-modal");
    const loadingCircle = document.getElementById("loading-circle");
  
    lockModal.style.display = "block";
    loadingCircle.style.display = "block";
}
  
function hidespinner() {
    document.body.style = "overflow: scroll";
  
    const lockModal = document.getElementById("lock-modal");
    const loadingCircle = document.getElementById("loading-circle");
    lockModal.style.display = "none";
    loadingCircle.style.display = "none";
}
  