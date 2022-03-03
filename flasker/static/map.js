let stations = JSON.parse(document.getElementById("map").dataset.stations);

const MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoicnV0aTEyMzQiLCJhIjoiY2wwMTMwY3FyMDBzNTNrbzB1YWp3aXJ4dSJ9.rRm6gErVoryz85FThkRiDQ";
// mapbox map creation
L.mapbox.accessToken = MAPBOX_ACCESS_TOKEN;

const MAPBOX_DRIVING_API = "https://api.mapbox.com/directions/v5/mapbox/";


let map = L.mapbox.map('map')
    .setView([31.790432720080467 , 34.63724819562294 ], 14)
    .addLayer(L.mapbox.styleLayer('mapbox://styles/mapbox/streets-v11'));

const addStations2map = (stations) => {

    for (const station in stations) {
        coord=stations[station];
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
function displayDriver(coords) {
    return new L.marker(new L.LatLng(coords[1], coords[0]), {
        icon: L.mapbox.marker.icon({
            'marker-size': 'medium',
            'marker-symbol': 'car',
            'marker-color': 'yellow',
        })
    }).addTo(map);
}


/**
 * 
 * @param {Route[]} routes 
 * @param {number[]} activeDrivers 
 */
function newActiveRoutes(routes, activeDrivers) {
    const now = Date.now();
    return routes.filter((route) => {
                    return route.times[0] < now &&
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
                setTimeout(tick, time * 100);
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
        const timeDelta = Math.floor((route.times[index+1] - route.times[index]) / 10000);
        const coordDelta = newDriver.coordinates[index];
        const travelTimeRatio = Math.floor(timeDelta/coordDelta.coordinates.length);

        await navigateFromPointToPoint(newDriver.driverIcon, coordDelta, travelTimeRatio);
    }

    // after all route animation - delete route 
    removeCompleteRoutes(newDriver.layers);
}

async function refreshRoutes(routes, activeDrivers) {
    const newActive = newActiveRoutes(routes, activeDrivers);
    newActive.forEach(async (route) => {
        const points = servicePointsToCoordinates(route.path);
        const coordinates = await getRoutCoordinates(points);

        // add path & car icon to the map
        const layers = displayRoute(coordinates);
        const driverIcon = displayDriver(coordinates[0].coordinates[0]);
        
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

const main = async () => {

    let routes = JSON.parse(document.getElementById("map").dataset.routes);
    console.log(routes);
    let activeDrivers = [];

    refreshRoutes(routes, activeDrivers);

    setInterval(() => {
        refreshRoutes(routes, activeDrivers);
        console.log(activeDrivers);

    }, 1000 * 60);
    
    addStations2map(stations);

    console.log(activeDrivers);
}; 

main();