var map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 48.8566, lng: 2.3522},
    zoom: 12
  });
  
  google.maps.event.addListenerOnce(map, 'tilesloaded', function() {
    var overlay = new D3Overlay(map.getBounds(), map);
  });
  
  function D3Overlay(bounds, map) {
    this.bounds_ = bounds;
    this.map_ = map;
    this.div_ = null;
    this.setMap(map);
  }
  D3Overlay.prototype = new google.maps.OverlayView();
  
  D3Overlay.prototype.onAdd = function() {
    var div = document.createElement('div');
    div.style.borderStyle = 'none';
    div.style.borderWidth = '0px';
    div.style.position = 'absolute';
    div.style.width = '100%';
    div.style.height = '100%';
    this.div_ = div;
    var overlayProjection = this.getProjection();
    var svg = d3.select(div).append("svg")
      .attr("width", "100%")
      .attr("height", "100%");
      var width = 800,
      height = 600;
  
    // 1. Acquire the necessary data
        d3.json("data/neighbourhoods.geojson").then(function(neighborhoods) {
        d3.csv("neighbourhood_price.csv").then(function(prices) {
  
        // 2. Choose a suitable map projection
        var projection = d3.geoMercator().fitSize([width, height], neighborhoods);
  
        // 3. Create an SVG container
        var svg = d3.select(div).append("svg")
            .attr("width", width)
            .attr("height", height);
  
  
        // 4. Load the data
        var priceByNeighborhood = {};
        prices.forEach(function(d) {
            priceByNeighborhood[d.neighbourhood] = +d.price;
        });
        
  
        // 5. Create a color scale
        var colorScale = d3.scaleLinear()
            .domain(d3.extent(prices, function(d) { return +d.price; }))
            .range(["white", "red"]);
  
        
        // 6. Draw the map
        var neighborhoodsGroup = svg.append("g")
            .selectAll("path")
            .data(neighborhoods.features)
            .enter()
            .append("path")
            .attr("d", d3.geoPath().projection(projection));
        
  
  
        // 7. Color the neighborhoods
        neighborhoodsGroup.style("fill", function(d) {
            var price = priceByNeighborhood[d.properties.neighbourhood];
            
            return colorScale(price);
        });
  
        // 8. Add interactivity
        var tooltip = d3.select("body").append("div")
            .attr("class", "tooltip")
            .style("display", "none");
        
        neighborhoodsGroup.on("mouseover", function(d) {
            var price = priceByNeighborhood[d.properties.neighbourhood];
            console.log(price)
            tooltip.text(d.properties.neighbourhood + ": $" + price);
  
            tooltip.style("display", "block");
        })
        .on("mousemove", function(d) {
            tooltip.style("top", (d3.event.pageY-10)+"px")
                .style("left",(d3.event.pageX+10)+"px");
        })
        .on("mouseout", function(d) {
            tooltip.style("display", "none");
        });

        });
    });
        
        this.getPanes().overlayLayer.appendChild(div);
    };
  
    D3Overlay.prototype.draw = function() {
        var overlayProjection = this.getProjection();
        var bounds = this.bounds_;
        if (!bounds) {
          return;
        }
        var sw = overlayProjection.fromLatLngToDivPixel(bounds.getSouthWest());
        var ne = overlayProjection.fromLatLngToDivPixel(bounds.getNorthEast());
        var div = this.div_;
        div.style.left = sw.x + 'px';
        div.style.top = ne.y + 'px';
        div.style.width = (ne.x - sw.x) + 'px';
        div.style.height = (sw.y - ne.y) + 'px';
      };

  var overlay = new D3Overlay(map.getBounds(), map);
