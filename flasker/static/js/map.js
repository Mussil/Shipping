let stations = JSON.parse(document.getElementById("map").dataset.stations);

const MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoicnV0aTEyMzQiLCJhIjoiY2wwMTMwY3FyMDBzNTNrbzB1YWp3aXJ4dSJ9.rRm6gErVoryz85FThkRiDQ";

L.mapbox.accessToken = MAPBOX_ACCESS_TOKEN;

const MAPBOX_DRIVING_API = "https://api.mapbox.com/directions/v5/mapbox/";

let INITIAL_DATE = new Date(2021, 12, 2, 0, 0, 0, 0); // 2.1.2022
const MIN_TO_SEC_RATIO = JSON.parse(document.getElementById("map").dataset.speed); //MIN_TO_SEC_RATIO [sec] reality = 60 [sec] simulator
const SEC_IN_MIN = 60; // each min has 60 sec in reality

let map = L.mapbox.map('map')
    .setView([31.790432720080467 , 34.63724819562294 ], 13.9)
    .addLayer(L.mapbox.styleLayer('mapbox://styles/mapbox/streets-v11'))
    .addControl(L.mapbox.geocoderControl('mapbox.places'));

L.control.layers({
    'streets view': L.mapbox.styleLayer('mapbox://styles/mapbox/streets-v11'),
    'light view': L.mapbox.styleLayer('mapbox://styles/mapbox/light-v10'),
    'outdoors view': L.mapbox.styleLayer('mapbox://styles/mapbox/outdoors-v11'),
    'satellite view': L.mapbox.styleLayer('mapbox://styles/mapbox/satellite-v9'),
    'dark view':L.mapbox.styleLayer('mapbox://styles/mapbox/dark-v10')
}).addTo(map);

const CSS_COLOR_NAMES = ["AntiqueWhite","Aqua","Aquamarine","Beige","Bisque","Black","BlanchedAlmond","Blue","BlueViolet","Brown","BurlyWood","CadetBlue",
"Chartreuse","Chocolate","Coral","CornflowerBlue","Crimson","Cyan","DarkBlue","DarkCyan","DarkGoldenRod","DarkGray","DarkGrey","DarkGreen","DarkKhaki","DarkMagenta",
"DarkOliveGreen","DarkOrange","DarkOrchid","DarkRed","DarkSalmon","DarkSeaGreen","DarkSlateBlue","DarkSlateGray","DarkSlateGrey","DarkTurquoise","DarkViolet",
"DeepPink","DeepSkyBlue","DimGray","DimGrey","DodgerBlue","FireBrick","ForestGreen","Fuchsia","Gainsboro","Gold","GoldenRod",
"Gray","Grey","Green","GreenYellow","HoneyDew","HotPink","IndianRed","Indigo","Ivory","Khaki","Lavender","LavenderBlush","LawnGreen","LemonChiffon","LightBlue",
"LightCoral","LightCyan","LightGoldenRodYellow","LightGray","LightGrey","LightGreen","LightPink","LightSalmon","LightSeaGreen","LightSkyBlue","LightSlateGray",
"LightSlateGrey","LightSteelBlue","LightYellow","Lime","LimeGreen","Linen","Magenta","Maroon","MediumAquaMarine","MediumBlue","MediumOrchid","MediumPurple","MediumSeaGreen",
"MediumSlateBlue","MediumSpringGreen","MediumTurquoise","MediumVioletRed","MidnightBlue","MintCream","MistyRose","Moccasin","NavajoWhite","Navy","OldLace","Olive",
"OliveDrab","Orange","OrangeRed","Orchid","PaleGoldenRod","PaleGreen","PaleTurquoise","PaleVioletRed","PapayaWhip","PeachPuff","Peru","Pink","Plum","PowderBlue",
"Purple","RebeccaPurple","Red","RosyBrown","RoyalBlue","SaddleBrown","Salmon","SandyBrown","SeaGreen","SeaShell","Sienna","Silver","SkyBlue","SlateBlue","SlateGray",
"SlateGrey","Snow","SpringGreen","SteelBlue","Tan","Teal","Thistle","Tomato","Turquoise","Violet","Wheat","Yellow","YellowGreen"];

document.getElementById('end-button').addEventListener('click', function(){
    const parcels = JSON.parse(document.getElementById("map").dataset.results); 
    const routes = JSON.parse(document.getElementById("map").dataset.routes); 

    const successfullParcels = Object.keys(parcels).filter(p => 
        parcels[p].path.length != 0
    );

    const failedParcels = Object.keys(parcels).filter(p => 
        parcels[p].path.length === 0
    );
    
    let avgParcelTime = Object.keys(parcels).map(p =>{
        if(successfullParcels.includes(p)){
            return (getParcelFinishedTime(routes, p, parcels) - parcels[p].startTime)/1000;
        }
    });
    
    avgParcelTime = avgParcelTime.filter(time => time != undefined);
    avgParcelTime = avgParcelTime.reduce((a,b) => a + b, 0) / avgParcelTime.length;
    HMSObj = convertHMS(avgParcelTime);

    swal({
        title: "SIMULATION FINAL RESULTS",
        text: `➼ Average parcesl time in system: ${HMSObj[0]} hours and ${HMSObj[1]} min\n\n➼ Successfull parcels: ${successfullParcels.length}\n\n➼ Failed parcels: ${failedParcels.length}\n`,
        type: "success",
        showCancelButton: "Back",
        confirmButtonText: "End simulation",
        showConfirmButton: 'false',
        confirmButtonColor: "#ff0055",
        cancelButtonColor: "#999999",
        focusConfirm: false,
        focusCancel: true,
      }, function(){
            window.location.href = "/end-simulation";
    });
});

/**
 * this func converts sec in js to HH:MM:SS
 * @param {*} value 
 * @returns 
 */
function convertHMS(value) {
    const sec = parseInt(value, 10); 
    let hours   = Math.floor(sec / 3600); 
    let minutes = Math.floor((sec - (hours * 3600)) / 60);
    
    if (hours   < 10) {hours   = "0"+hours;}
    if (minutes < 10) {minutes = "0"+minutes;}
    return [hours,minutes];
}

/**
 * returns random color in css
 */
function getRandomColor() {
    return CSS_COLOR_NAMES[Math.floor(Math.random()*CSS_COLOR_NAMES.length)];
}

/**
 * @param {*} date 
 * @param {*} minutes 
 * @returns 
 */
function add_minutes(date , minutes) {
    return new Date(date.getTime() + minutes * 60000);
}

/**
 * @param {*} stations 
 */
function addStations2map(stations, stationsMarkers){

    for (const station in stations) {
        coord=SP2Coords(station);
        coord.reverse();

        const layer = new L.marker(coord, {
                        icon: L.mapbox.marker.icon({
                            'marker-color':"black",
                            'marker-symbol'	: station,
                            'marker-size': 'small'
                        })}).addTo(map);
        
        const station_obj = {
            layer: layer,
            num: station,
            coords: coord,
            currentParcels:[],
        }

        stationsMarkers.push(station_obj);
    }

};

function SP2Coords(name){
    return stations[name]
}

/**
 * 
 * @param {Array<int>} sps - list of service points 
 */
function servicePointsToCoordinates(sps) {
    return sps.map(SP2Coords)
}

/**
 * fetch coordinates from mapbox and format
 * @param {Array<{lat: number, lon: number}>} points
 * @returns {Array<[number, number]>}
 */
async function getRoutCoordinates(points) {

    let layesrArr = [];

    for (let index = 0; index < points.length - 1; index++) {
        let coords = `${points[index][0]},${points[index][1]};${points[index+1][0]},${points[index+1][1]}`;
        
        if(coords[1].startsWith("1")){
            coords = `${points[index][1]},${points[index][0]};${points[index+1][1]},${points[index+1][0]}`;
        }
        
        const url = new URL(`driving/${coords}`, MAPBOX_DRIVING_API);
        url.searchParams.set("geometries", "geojson");
        url.searchParams.set("overview", "full");
        url.searchParams.set("access_token", MAPBOX_ACCESS_TOKEN);
        const respose = await fetch(url).then(res => res.json());
        const [geometry] =  respose.routes;
        layesrArr.push(geometry.geometry);
    }

    return layesrArr;
}


/**
 * @param {Array<[]number, number>[]} polyLine 
 */
function displayRoute(coordinates, colorRoute) {
    let allRoute = [];
    coordinates.map(path => {
        for (let index = 0; index < path.coordinates.length - 1; index++) {
            const geojson = {'coordinates': [path.coordinates[index], path.coordinates[index+1]], 'type': 'LineString'}; 
            const layer = new L.geoJson(geojson).setStyle({
                color: colorRoute,
            }).addTo(map);
            allRoute.push(layer);    
        }
    });
    return allRoute;
}

/**
 * @param {[number-lat, number-lon]} coords
 */
function displayDriver(coords, driverNum) {
    const markerColor = getRandomColor();
    const marker = new L.marker(new L.LatLng(coords[1], coords[0]), {
        icon: L.mapbox.marker.icon({
            'marker-size': 'medium',
            'marker-symbol': 'car',
            'marker-color': markerColor,
        })
    }).addTo(map);
    marker.bindPopup(String(driverNum));
    // marker.openPopup();
    return [marker, markerColor];
}

/**
 * @param {*} coords 
 * @param {*} parcelNum  
 */
function displayParcel(coords, parcelNum) {
    var cssIcon = L.divIcon({
        className: 'svg-marker',
        html: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" fill="red" width="20" height="50"><path d="M40 8H8c-2.21 0-3.98 1.79-3.98 4L4 36c0 2.21 1.79 4 4 4h32c2.21 0 4-1.79 4-4V12c0-2.21-1.79-4-4-4zm0 8L24 26 8 16v-4l16 10 16-10v4z"></path>',
        // html: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" fill="red" width="60" height="150"><path d="M1 4.27v7.47c0 .45.3.84.75.97l6.5 1.73c.16.05.34.05.5 0l6.5-1.73c.45-.13.75-.52.75-.97V4.27c0-.45-.3-.84-.75-.97l-6.5-1.74a1.4 1.4 0 0 0-.5 0L1.75 3.3c-.45.13-.75.52-.75.97zm7 9.09l-6-1.59V5l6 1.61v6.75zM2 4l2.5-.67L11 5.06l-2.5.67L2 4zm13 7.77l-6 1.59V6.61l2-.55V8.5l2-.53V5.53L15 5v6.77zm-2-7.24L6.5 2.8l2-.53L15 4l-2 .53z"></path></svg>',
        // html:'<svg viewBox="0 0 2091 2091" xmlns="http://www.w3.org/2000/svg" fill="#C71585" width="20" height="20"><path d="M1906.333 1664l35 313q3 28-16 50-19 21-48 21h-1664q-29 0-48-21-19-22-16-50l35-313h1722zm-93-839l86 775h-1708l86-775q3-24 21-40.5t43-16.5h256v128q0 53 37.5 90.5t90.5 37.5 90.5-37.5 37.5-90.5V768h384v128q0 53 37.5 90.5t90.5 37.5 90.5-37.5 37.5-90.5V768h256q25 0 43 16.5t21 40.5zm-384-185v256q0 26-19 45t-45 19-45-19-19-45V640q0-106-75-181t-181-75-181 75-75 181v256q0 26-19 45t-45 19-45-19-19-45V640q0-159 112.5-271.5t271.5-112.5 271.5 112.5 112.5 271.5z"></path></svg>',
        iconSize: [24, 24],
    });
    
    marker = L.marker([coords[0], coords[1]], {icon: cssIcon}).addTo(map);

    marker.bindPopup(parcelNum);
    return marker;  
}

/**
 * 
 * @param {Route[]} routes 
 * @param {number[]} activeDrivers 
 */
function newActiveRoutes(routes, activeDrivers) {
    const now = INITIAL_DATE.getTime();
    return routes.filter((route) => {
                    return new Date(route.times[0]).setSeconds(0, 0) === now &&
                    now < route.times[route.times.length - 1] &&
                    !(activeDrivers.findIndex(d => d.driver === route.driver) > -1)
                });
}

/**
 * @param {icon} icon 
 */
function removeIcon(icon){
    map.removeLayer(icon);
}


/**
 * navigate a driver beween 2 point on the map
 * @param {*} driver 
 * @param {*} geojson 
 * @param {*} time
 */
async function navigateFromPointToPoint(driver, geojson, time, parcels2Pass, layers) {
    return new Promise(res => {
        let j = 0;
        tick();
        function tick(){
            driver.setLatLng(L.latLng(geojson.coordinates[j][1],geojson.coordinates[j][0]));
            parcels2Pass.forEach((parcel) => {
                parcel.parcelIcon.setLatLng(L.latLng(geojson.coordinates[j][1],geojson.coordinates[j][0]));
            });

            if (++j < geojson.coordinates.length) {
                removeIcon(layers.shift())
                setTimeout(tick, time * (MIN_TO_SEC_RATIO/SEC_IN_MIN));
            } else {
                res();
            }
        }
    })
}

/**
 * remove un activated driver from activer drivers array
 * @param {*} activeDrivers 
 * @param {*} driver 
 */
async function removeOutdatedDriver(activeDrivers, driver) {
    const now = INITIAL_DATE.getTime();

    const driverIndex = activeDrivers.findIndex((d) => {
        d.driver === driver.driver;
    });

    await new Promise(res => {
        activeDrivers.splice(driverIndex, 1);
        res();
    });
    
    // console.log(`removed ${driver.driver} from active >>>>`);
    // console.log(activeDrivers);
}

/**
 * @param {{driver: x, path: Array(4), start:--, times: Array(4)}} route 
 * @param {{driver: x, layers: Array(y), driverIcon: e, coordinates: Array[[],[],...]}} newDriver 
 */
async function animateRoutes(route, newDriver, activeParcels, activeDrivers) {

    for (let index = 0; index < route.path.length - 1; index++) {
        const timeDelta = (route.times[index+1] - route.times[index]);
        const coordDelta = newDriver.coordinates[index];
        const travelTimeRatio = Math.floor(timeDelta/coordDelta.coordinates.length);

        let parcels2Pass = activeParcels.filter((parcel) => {
            const driverNum = route.driver;
            const station1 = route.path[index];
            const station2 =  route.path[index+1];

            for (let station = 0; station < parcel.path.length - 1; station++) {
                const firstMatch =  parcel.path[station]; // <station, driver>
                const secondMatch = parcel.path[station+1]; // <station, driver>

                // if there is a match between driver to parcel
                if(station1 === firstMatch[0] && station2 === secondMatch[0] && driverNum === firstMatch[1] && driverNum === secondMatch[1]){
                    return parcel;
                }
            }
        });
        
        await navigateFromPointToPoint(newDriver.driverIcon, coordDelta, travelTimeRatio, parcels2Pass, newDriver.layers);
    }

    // console.log(`harrrayyyyy driver ${newDriver.driver} finished his path !!!`);

    // after all route animation - delete route & thier drivers icons
    removeIcon(newDriver.driverIcon);
    removeOutdatedDriver(activeDrivers, newDriver);
}

function smoothPath(coords) {

    let newCoords = [];

    for (let index = 0; index < coords.length; index++) {
        const newPath = [];
        const path = [...coords[index].coordinates];
        const pathLength = coords[index].coordinates.length;
        
        for (let coord = 0; coord < pathLength; coord++) {
            const point1 = path[coord];
            const point2 = path[coord+1];

            if(coord === 1){
                newPath.push(point1);
            }
            else if(coord === pathLength - 1){
                break;
            }

            const middle = [(point1[0]+point2[0])/2, (point1[1]+point2[1])/2];

            newPath.push(middle);
            newPath.push(point2);
        } 

        newCoords[index] = {'coordinates': [], 'type': 'LineString'}; 
        newCoords[index].coordinates = newPath;
    }
    return newCoords;
}

async function refreshRoutes(routes, activeDrivers, activeParcels) {
    const newActive = newActiveRoutes(routes, activeDrivers);

    newActive.forEach(async (route) => {
        const points = servicePointsToCoordinates(route.path);
        let coordinates = await getRoutCoordinates(points);
        coordinates = smoothPath(coordinates);
        coordinates = smoothPath(coordinates);

        const driverData = displayDriver(coordinates[0].coordinates[0], route.driver);
        const driverIcon = driverData[0];
        const driverColor = driverData[1];

        const layers = displayRoute(coordinates, driverColor);
        
        const newDriver = {
            driver: route.driver,
            layers,
            driverIcon,
            coordinates,
        };

        await new Promise(res => {
            activeDrivers.push(newDriver);
            res();
        });

        // console.log(`added ${newDriver.driver} to active >>>>`);
        // console.log(activeDrivers);

        animateRoutes(route, newDriver, activeParcels, activeDrivers);
    });
}

/**
 * return parcel removal time
 * @param {*} routes 
 * @param {*} parcel 
 */
function getParcelFinishedTime(routes, parcelName, results) {

    const lastParcelDriver = results[parcelName].path[results[parcelName].path.length - 2][1];
    const lastParcelDriverStation = results[parcelName].path[results[parcelName].path.length - 2][0];
    const parcelDriver = routes.filter(d => d.driver === lastParcelDriver)[0]; //{routes[driver]}
    const driverStationTimeIndex = parcelDriver.path.findIndex(station => station === lastParcelDriverStation);

    return parcelDriver.times[driverStationTimeIndex]; 
}

/**
 * find new parcels to move on map
 * @param {*} parcels 
 */
function newActiveParcels(results, newActiveParcels, routes) {
    const now = INITIAL_DATE.getTime();
    return Object.keys(results).filter((parcelNum) => {   
        return  results[parcelNum]["path"].length != 0 && // TODO: fix that - Mussi  
        results[parcelNum]["startTime"] <= now &&
        now < getParcelFinishedTime(routes, parcelNum, results) &&
        !(newActiveParcels.findIndex(p => p.num === parcelNum) > -1);
    });
}

/**
 * show parcels on map in specific time
 * @param {*} results
 */
async function refreshParcels(results, activeParcels, routes) {
    const newActive =  newActiveParcels(results, activeParcels, routes);
    
    newActive.forEach(async (parcelName) => {
        await new Promise(res => {
            const parcelIcon = displayParcel(SP2Coords(results[parcelName].path[0][0]), parcelName);
            const newParcel = {
                num: parcelName,
                parcelIcon: parcelIcon,
                path: results[parcelName].path,
                finishPathTime: getParcelFinishedTime(routes, parcelName, results) + 1000, // remove parcel 2 sec later ...  
                distance: results[parcelName].totalDistance,
                startTime: results[parcelName].startTime,
                cost: results[parcelName].payActual
            };

            activeParcels.push(newParcel);

            updateParcelsWhenStart(newParcel);
            res();
        });

    });
}

/**
 * update time on map
 */
function clockTime() {

    const hour = (INITIAL_DATE.getHours() < 10) ? ("0" + INITIAL_DATE.getHours()) : INITIAL_DATE.getHours();
    const min = (INITIAL_DATE.getMinutes() < 10) ? ("0" + INITIAL_DATE.getMinutes()) : INITIAL_DATE.getMinutes();
    const day = INITIAL_DATE.getDate();
    const month = INITIAL_DATE.getMonth() + 1;
    const year = INITIAL_DATE.getFullYear();

    document.getElementById("clock").innerHTML =`${hour}:${min}`;
    document.getElementById("date").innerHTML =`${day}/${month}/${year}`;
}

/**
 * this function remove all parcels when they finish path
 * @param {*} activeParcels 
 */
async function removeParcelWhenEnds(activeParcels, arrivedSuccessfullyParcels) {
    const now = INITIAL_DATE.getTime();
    const removedParcels = activeParcels.filter(p => p.finishPathTime < now);
    
    removedParcels.forEach(async (p) => {
        await new Promise(res => {
            removeIcon(p.parcelIcon);
            const parcelIndex = activeParcels.findIndex(parcel => parcel.num === p.num);
            
            activeParcels.splice(parcelIndex, 1);
            arrivedSuccessfullyParcels.push(p);
            updateArrivedParcels(p);
            res();
        })
    });
}

/**
 * update the text-box on map to show activeDrivers
 * @param {*} activeDrivers 
 */
 function updateHTML(activeDrivers, activeParcels, arrivedSuccessfullyParcels) {

    const data1 = `<h4>① active drivers : ${activeDrivers.length} </h4><br/>`; 
    const data2 = `<h4>② parcels during shipment : ${activeParcels.length}</h4><br/>`; 
    const data3 = `<h4>③ parcels successfully shipped : ${arrivedSuccessfullyParcels.length}</h4>`; 

    document.getElementById("active-data").innerHTML = data1 + data2 + data3;
}

/**
 * update table of parcels when finish their path
 * @param {*} parcel 
 */
function updateArrivedParcels(parcel) {

    const table = document.getElementById("myTable");
    const row = table.insertRow(1);

    const parcelNum = row.insertCell(0);
    const parcelStart = row.insertCell(1);
    const parcelEnd = row.insertCell(2);
    const parcelDistance = row.insertCell(3);
    const parcelDrivers = row.insertCell(4);
    const parcelsCost = row.insertCell(5);

    parcelNum.className="td-map";
    parcelStart.className="td-map";
    parcelEnd.className="td-map";
    parcelDistance.className="td-map";
    parcelDrivers.className="td-map";
    parcelsCost.className="td-map";

    parcelNum.innerHTML = parcel.num;
    parcelStart.innerHTML = `${new Date(parcel.startTime).getHours()}:${new Date(parcel.startTime).getMinutes()}`;
    parcelEnd.innerHTML = `${new Date(parcel.finishPathTime).getHours()}:${new Date(parcel.finishPathTime).getMinutes()}`;
    parcelDistance.innerHTML = parcel.distance;
    parcelDrivers.innerHTML = [... new Set(parcel.path.map(p => {
        return p[1];
    }))].length - 1;
    parcelsCost.innerHTML = parcel.cost.toFixed(3);

}

/**
 * update 'parcels-in-system' table
 * @param {} params 
 */
function updateParcelsWhenStart(parcel) {
    let h = new Date(parcel.startTime).getHours();
    let m = new Date(parcel.startTime).getMinutes();

    h = (h < 10) ? ("0" + h) : h;
    m = (m < 10) ? ("0" + m) : m;

    const parcelsData = `⦿ parcel <strong>${parcel.num}</strong> enetered to station #${parcel.path[0][0]} at ${h}:${m}<br/><br/>`;    
    document.getElementById("parcels-in-system").innerHTML = parcelsData + document.getElementById("parcels-in-system").innerHTML;  
}

async function main(){
    let routes = JSON.parse(document.getElementById("map").dataset.routes); // all drivers
    let results = JSON.parse(document.getElementById("map").dataset.results); // all parcels
    
    let stationsMarkers = [];
    let activeDrivers = [];
    let activeParcels = [];
    let arrivedSuccessfullyParcels = [];

    addStations2map(stations, stationsMarkers);
    refreshRoutes(routes, activeDrivers, activeParcels);
    refreshParcels(results, activeParcels, routes);
    updateHTML(activeDrivers, activeParcels, arrivedSuccessfullyParcels);
    clockTime();

    setInterval(() => {

        INITIAL_DATE = add_minutes(INITIAL_DATE, 1);

        refreshRoutes(routes, activeDrivers, activeParcels);
        refreshParcels(results, activeParcels, routes);
        removeParcelWhenEnds(activeParcels, arrivedSuccessfullyParcels);
        
        updateHTML(activeDrivers, activeParcels, arrivedSuccessfullyParcels);
        clockTime();

    }, 1000 * MIN_TO_SEC_RATIO);   

}; 

main();

