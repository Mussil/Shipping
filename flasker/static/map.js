let stations = JSON.parse(document.getElementById("map").dataset.stations);

const MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoicnV0aTEyMzQiLCJhIjoiY2wwMTMwY3FyMDBzNTNrbzB1YWp3aXJ4dSJ9.rRm6gErVoryz85FThkRiDQ";
// mapbox map creation
L.mapbox.accessToken = MAPBOX_ACCESS_TOKEN;

const MAPBOX_DRIVING_API = "https://api.mapbox.com/directions/v5/mapbox/";

let INITIAL_DATE = new Date(2021, 12, 2, 9, 18, 0, 0); // 7.3.2022
const MIN_TO_SEC_RATIO = 1; //TODO: FIX IT TO 4!!! MIN_TO_SEC_RATIO [sec] reality = 60 [sec] simulator
const SEC_IN_MIN = 60; // each min has 60 sec in reality

let map = L.mapbox.map('map')
    .setView([31.790432720080467 , 34.63724819562294 ], 14)
    .addLayer(L.mapbox.styleLayer('mapbox://styles/mapbox/streets-v11'));

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
const addStations2map = (stations) => {

    for (const station in stations) {
        coord=SP2Coords(station);
        coord.reverse();

        new L.marker(coord, {
            icon: L.mapbox.marker.icon({
                'marker-color': '#f86767',
                'marker-symbol'	: station, // TODO: 'post' symbol for packages :)
                'marker-size': 'small'
            })}).addTo(map);
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
function displayRoute(coordinates) {
    return coordinates.map((path) => new L.geoJson(path).addTo(map));
}

/**
 * @param {[number-lat, number-lon]} coords
 */
function displayDriver(coords, driverNum) {
    return new L.marker(new L.LatLng(coords[1], coords[0]), {
        icon: L.mapbox.marker.icon({
            'marker-size': 'medium',
            'marker-symbol': driverNum,
            'marker-color': 'yellow',
        })
    }).addTo(map);
}

/**
 * @param {*} coords 
 * @param {*} parcelNum  
 */
function displayParcel(coords, parcelNum) {
    const num = parcelNum;
    const marker = new L.marker(new L.LatLng(coords[0], coords[1]), {
        icon: L.mapbox.marker.icon({
            'marker-size': 'small',
            'marker-symbol': 'post', //'post' for packages symbol
            'marker-color': 'white'
        })
    }).addTo(map);
    marker.bindPopup(num);
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
                    return route.times[0] <= now &&
                    now < route.times[route.times.length - 1] &&
                    !(activeDrivers.findIndex(d => d.driver === route.driver) > -1)
                });
}

/**
 * @param {Array<[]>} layers 
 */
function removeCompleteRoutes(layers) {
    layers.forEach((layer) =>
        map.removeLayer(layer)
    );
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
async function navigateFromPointToPoint(driver, geojson, time) {
    return new Promise(res => {
        let j = 0;
        tick();
        function tick(){
            driver.setLatLng(L.latLng(geojson.coordinates[j][1],geojson.coordinates[j][0]));
            if (++j < geojson.coordinates.length) {
                setTimeout(tick, time * (MIN_TO_SEC_RATIO/SEC_IN_MIN));
            } else {
                res();
            }
        }
    })
}

/**
 * @param {{driver: x, path: Array(4), start:--, times: Array(4)}} route 
 * @param {{driver: x, layers: Array(y), driverIcon: e, coordinates: Array[[],[],...]}} newDriver 
 */
async function animateRoutes(route, newDriver) {

    for (let index = 0; index < route.path.length - 1; index++) {
        const timeDelta = (route.times[index+1] - route.times[index]);
        const coordDelta = newDriver.coordinates[index];
        const travelTimeRatio = Math.floor(timeDelta/coordDelta.coordinates.length);
        
        await navigateFromPointToPoint(newDriver.driverIcon, coordDelta, travelTimeRatio);
    }

    console.log("harrrayyyyy")

    // after all route animation - delete route & thier drivers icons
    removeCompleteRoutes(newDriver.layers);
    removeIcon(newDriver.driverIcon);
}

async function refreshRoutes(routes, activeDrivers) {
    const newActive = newActiveRoutes(routes, activeDrivers);
    console.log(newActive);

    newActive.forEach(async (route) => {
        const points = servicePointsToCoordinates(route.path);
        const coordinates = await getRoutCoordinates(points);

        // add path & car icon to the map
        const layers = displayRoute(coordinates);
        const driverIcon = displayDriver(coordinates[0].coordinates[0], route.driver);
        
        const newDriver = {
            driver: route.driver,
            layers,
            driverIcon,
            coordinates,
        };
        activeDrivers.push(newDriver);

        animateRoutes(route, newDriver);
    });
}

/**
 * find new parcels to move on map
 * @param {*} parcels 
 */
function newActiveParcels(parcels, newActiveParcels) {
    const now = INITIAL_DATE.getTime();
    return Object.keys(parcels).filter((parcelNum) => {        
        return parcels[parcelNum]["startTime"] <= now &&
        // !newActiveParcels.includes({parcelNum});
        !(newActiveParcels.findIndex(p => p.num === parcelNum) > -1);
    });
}

/**
 * show parcels on map in specific time
 * @param {*} results
 */
function refreshParcels(results, activeParcels) {
    const newActive =  newActiveParcels(results, activeParcels);
    newActive.forEach((parcelName) => {
        const layer = displayParcel(SP2Coords(results[parcelName].path[0][0]), parcelName);
        
        const newParcel = {
            num: parcelName,
            layer: layer,
        };

        activeParcels.push(newParcel);
    });
}

const main = async () => {

    let routes = JSON.parse(document.getElementById("map").dataset.routes);
    let results = JSON.parse(document.getElementById("map").dataset.results);
    
    let activeDrivers = [];
    let activeParcels = [];

    refreshRoutes(routes, activeDrivers);
    refreshParcels(results, activeParcels);

    setInterval(() => {
        refreshRoutes(routes, activeDrivers);
        refreshParcels(results, activeParcels);
        INITIAL_DATE = add_minutes(INITIAL_DATE, 1);
        
        console.log(INITIAL_DATE);

    }, 1000 * MIN_TO_SEC_RATIO);
    
    addStations2map(stations);

    console.log(activeDrivers);
}; 

main();