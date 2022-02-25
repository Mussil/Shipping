// mapbox map creation
L.mapbox.accessToken = 'pk.eyJ1IjoicnV0aTEyMzQiLCJhIjoiY2wwMTMwY3FyMDBzNTNrbzB1YWp3aXJ4dSJ9.rRm6gErVoryz85FThkRiDQ';

let map = L.mapbox.map('map')
    .setView([31.790432720080467 , 34.63724819562294 ], 14)
    .addLayer(L.mapbox.styleLayer('mapbox://styles/mapbox/streets-v11'));

// get data from server-side
let routes = JSON.parse(document.getElementById("map").dataset.routes);

const now = new Date();

//---------------------------------------------------------------------------------------------

function SP2Coords(name){
    return stations[name]
}

function animation(car, geojson){

    driver = car['car'];

    let j=0;
    tick();

    function tick(){
        driver.setLatLng(L.latLng(geojson[j][1],geojson[j][0]));
        if (++j < geojson.length) {
            setTimeout(tick, 100);
        } 
    }
}

function converTimes(driverTime){
    // number of minutes from 24:00 divide by 60

    divided=60 // 60 min in reality == 1 min here 
    ti11=new Date(driverTime)
    return (ti11.getHours()*60+ti11.getMinutes())/divided + ti11.getSeconds();
}

async function calcPolyLine(routes){

    let path_coordinates = []; // array for oordinates for path
    let coords_res;

    for(let i=0; i<routes.length; i++){
        driver = routes[i];
        driver['geojson'] = [];
        driver['polyLine'] = [];

        path_coordinates[i] = [];
        path = driver['path'];

        for(let j=0; j<path.length-1 ; j++){ 
            let coords = `${SP2Coords(path[j])[1]},${SP2Coords(path[j])[0]};${SP2Coords(path[j+1])[1]},${SP2Coords(path[j+1])[0]}`;

            coords_res = await fetch('https://api.mapbox.com/directions/v5/mapbox/driving/' + coords + '?geometries=geojson&overview=full&access_token=pk.eyJ1IjoicnV0aTEyMzQiLCJhIjoiY2wwMTMwY3FyMDBzNTNrbzB1YWp3aXJ4dSJ9.rRm6gErVoryz85FThkRiDQ');
            coords_res = await coords_res.json();
            coords_res = coords_res['routes'][0]['geometry']['coordinates'];

            path_coordinates[i].push(coords_res);

            for(let k=0; k<coords_res.length; k++){
                driver['polyLine'].push([coords_res[k][1], coords_res[k][0]]);
            }
        }

        driver['geojson'] = path_coordinates[i];
    }

    return Promise.all(path_coordinates);
}

async function initialMap(carsColor){

    // add stations to the map
    for (const station in stations) {
        coord=stations[station]
        coord.reverse()
        new L.marker(coord, {
            icon: L.mapbox.marker.icon({
                'marker-color': '#f86767',
                'marker-symbol'	: station,
                'marker-size': 'small'
            })}).addTo(map);
    }
    
    console.log(routes);

    await calcPolyLine(routes);
    console.log(routes);

    // add cars symbols to the map
    for(let driver of routes){
        path=driver['path'];
        startTime=driver['start'];
        firstCoords=SP2Coords(path[0])
        driver['car']= L.marker([firstCoords[0], firstCoords[1]], {
                                    icon: L.mapbox.marker.icon({
                                        'marker-size': 'medium',
                                        'marker-symbol': 'car',
                                        // 'marker-color': (i < carsColor.length) ? carsColor[i] : carsColor[i % carsColor.length],	
                                    })
                                })

        
        setTimeout((car)=>{
            console.log(driver);
            car.addTo(map);
            L.polyline(driver['polyLine']).addTo(map);
            animation(driver, driver['geojson'][0]);
        },converTimes(startTime)*1000 ,driver['car']);

    }

}

function moveCarsByTime(){
    console.log(routes);
    for(let driver of routes){
        // console.log(driver);
        // console.log(driver.geojson);
        console.log(Object.keys(driver));
        // for(let i=0; i<driver['geojson'].length; i++){
        //     console.log(driver['geojson'][i]);
        //     //////////////////////////////////////////////////
        // }
    }
}

async function main(){

    const mapObject = initialMap(carsColor); 
    // const l = mapObject[0];
    // const map = mapObject[1];
    // const routes = mapObject[2];
    moveCarsByTime();
}

let stations = JSON.parse(document.getElementById("map").dataset.stations);
const carsColor = ["blueviolet", "blue", "brown", "chartreuse", "darkorchid", "darkred", "darksalmon", "fuchsia", "hotpink", "cadetblue", "aqua", "aquamarine"];
main();