console.log("connection working");

// Define variables for our base layers
var streetmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets",
  accessToken: API_KEY
});

// satellite map background tile layer
var satellitemap =  L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.satellite",
    accessToken: API_KEY
});

var darkmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.dark",
  accessToken: API_KEY
});

var Stamen_TonerBackground = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/toner-background/{z}/{x}/{y}{r}.{ext}', {
	attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
	subdomains: 'abcd',
	maxZoom: 18,
	ext: 'png'
});

var Stamen_Watercolor = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.{ext}', {
	attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
	subdomains: 'abcd',
	maxZoom: 18,
	ext: 'png'
});

// Initialize all of the LayerGroups to be used
var layers = {
  CREEK_SITES: new L.LayerGroup(),
  BOUNDARIES: new L.LayerGroup()
};

// Create the map with layers
var map = L.map("map", {
  center: [44.933457, -93.502959],
  zoom: 10.7,
  layers: [
    layers.CREEK_SITES,
    layers.BOUNDARIES
  ]
});

// Add 'darkmap' tile layer to the map as default
darkmap.addTo(map);


// Create an overlay object
var overlayMaps = {
  "Stream Level": layers.CREEK_SITES,
  "Subwatersheds_test": layers.BOUNDARIES
  
};

var baseMaps = {
  "Street Map": streetmap,
  "Dark Map": darkmap,
  "Black and White": Stamen_TonerBackground,
  "Watercolor Map": Stamen_Watercolor
};


L.control.layers(baseMaps, overlayMaps).addTo(map);

// =================================================================================================
// WATERSHED BOUNDARIES LAYER
// =================================================================================================

// use var 'watershed' from 'watersheds.js' to import into leaflet geoJSON object
var watershedJson = L.geoJSON(watershed, {

  fillColor: 'lightblue',
  weight: 1.5,
  
  // highlight subwatershed in red for mouseover
  onEachFeature: function(feature, layer) {

    layer.on("mouseover", function(item) {
      layer.setStyle({fillColor: 'orange'})
    })
    .on("mouseout", function(item) {
      layer.setStyle({fillColor: 'lightblue'})
    });
  }
});

watershedJson.addTo(layers.BOUNDARIES);


// =================================================================================================
// WATERSHED BOUNDARIES LAYER
// =================================================================================================

// var geoData = "https://raw.githubusercontent.com/bbeck0744/water-levels/master/data/geospatial/major_subwatersheds.geojson";


// d3.json(geoData, function(data){
//   // add GeoJSON layer to the map once the file is loaded
//   L.geoJson(data ,{
//   onEachFeature: function(features, layer) {
//   layer.bindPopup(features.properties.Maj_shed);
//   }
//   }).addTo(layers.BOUNDARIES);
//   });


// =================================================================================================
// CREEK SITES LAYER
// =================================================================================================


Plotly.d3.csv('combined_data.csv', function(err, rows){

    function unpack(rows, key) {
        return rows.map(function(row) { return row[key]; });
    }


var sites = [{
  names: "CPA01",
  location: [44.964088, -93.672554],
  subwatershed: "Painters Creek"
},
{
  names: "CMH04",
  location: [44.901323, -93.332248],
  subwatershed: "Minnehaha Creek"
},
{
  names: "CMH24",
  location: [44.915574, -93.242167],
  subwatershed: "Minnehaha Creek"
},

{
    names: "CMH01",
    location: [44.9412, -93.4551],
    subwatershed: "Minnehaha Creek"
}
];

function circleClick(e) {
  const name = e.sourceTarget.options.name;
  document.getElementById('name').innerHTML = name;
  updateSite(name);
}

for (let i = 0; i < sites.length; i++) {
  L.circle(sites[i].location, 200, {
    name: sites[i].names, 
    fillOpacity: 0.8,
    color: "orange",
    fillColor: "blue",
    weight: 1.5
  }).addTo(layers.CREEK_SITES)
  .bindPopup("<p> Site: " + sites[i].names + "</p>")
  .on("click", circleClick)
  .on("mouseover", function() {
    this.setStyle({color: "orange", fillColor: 'blue', weight: 3})
  })
  .on("mouseout", function() {
    this.setStyle({color: "orange", fillColor: 'blue', weight: 1.5})
  });
}
    
var allsitenames = unpack(rows, 'site'),
    allDate = unpack(rows, 'rounded_time'),
    allLevel = unpack(rows, 'level_ft'),
    currentSite,
    currentLevel = [],
    currentDate = [];

  
  function getSiteData(chosenSite) {
    currentLevel = [];
    currentDate = [];
    RecentLevel = [];
    MaxLevel = [];

    for (var i = 0 ; i < allsitenames.length ; i++){
      if ( allsitenames[i] === chosenSite ) {
        currentLevel.push(allLevel[i]);
        currentDate.push(allDate[i]);
        RecentLevel.push(allLevel[0])
      } 
    }

  };

// Default Site Data
setBubblePlot('CPA01');



function setBubblePlot(chosenSite) {
    getSiteData(chosenSite);  

    var trace1 = {
      x: currentDate,
      y: currentLevel,
      mode: 'lines',
      marker: {
        size: 5, 
        opacity: 0.5
      }
    };

    var data = [trace1];

    var layout = {
        title: 'Stream Flow for <br>'+ chosenSite,
            yaxis: {
                title: {
                    text: 'Stream Flow (cfs)'
                }
            }

    };
    var config = {responsive: true}

    Plotly.newPlot('plotdiv', data, layout, config, {showSendToCloud: true});
};

function updateSite(site){
  setBubblePlot(site);

}

d3.select("#name").on("change", updateSite);
});