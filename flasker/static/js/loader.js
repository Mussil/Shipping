loadSpinner();

function loadSpinner() {
    const src = document.getElementById("body");
    const html = `<div id="lock-modal"></div>
        <div class="loader" id="loading-circle">
            <span class="bar"></span>
            <span class="bar"></span>
            <span class="bar"></span>
        </div>`;
    src.insertAdjacentHTML("afterbegin", html);
}

function showspinner() {
    document.body.style = "overflow: hidden;margin: 0;";
  
    const lockModal = document.getElementById("lock-modal");
    const loadingCircle = document.getElementById("loading-circle");
  
    lockModal.style.display = "block";
    loadingCircle.style.display = "flex";
}
  
function hidespinner() {
    document.body.style = "overflow: scroll";
  
    const lockModal = document.getElementById("lock-modal");
    const loadingCircle = document.getElementById("loading-circle");
    lockModal.style.display = "none";
    loadingCircle.style.display = "none";
}
  