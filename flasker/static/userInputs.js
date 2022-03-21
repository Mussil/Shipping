function sendUserinfo(){
    const drivers = document.getElementById('drivers').value;
    const parcels = document.getElementById('parcels').value;
    console.log(drivers, parcels);

    const request = new XMLHttpRequest();
    request.open('POST', `/UserInputs/${drivers}/${parcels}`);
    request.send();
}