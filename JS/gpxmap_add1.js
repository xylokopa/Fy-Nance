// gpxmap_add1.js

"use strict";
//Alt: https://sgx.geodatenzentrum.de/wmts_topplus_open/...Neu: https://wheregroup.com{z}/{x}/{y}.png

window.JS = window.JS || {};

( function(verstring) {
		JS.Debug_Info("",verstring,false);
		if(!JS.debuginfo && typeof(console) != "undefined" && typeof(console.info) == "function" )
			console.info(verstring);
} )("gpxmap_add1.js 21-11-05");

JS.Map = function(makemap) {
	var dieses = this;
	var id = makemap.id;
	var mapcanvas = makemap.mapdiv;
	dieses.id = id;
	dieses.makemap = makemap;
	dieses.mapcanvas = mapcanvas;
	this.cluster_zoomhistory = [];

	// Map anlegen

      const mycp = '<a href="https://google.com" title="gm">GM</a> | ';

      this.baseLayers = {}; 

      this.baseLayers["Open Topo"] = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
	    maxZoom: 17,
	    attribution: mycp+'<a href="https://opentopomap.org">OpenTopo</a>',
	    referrerPolicy: 'strict-origin'
      });

      this.baseLayers["Satellit"] = L.tileLayer('https://arcgisonline.com{z}/{y}/{x}', {
	    maxZoom: 18,
	    attribution: mycp+'<a href="https://esri.com">Esri</a>',
	    referrerPolicy: 'strict-origin'
      });

      this.baseLayers["OSM"] = L.tileLayer('https://openstreetmap.org{z}/{x}/{y}.png', {
	    maxZoom: 19,
	    attribution: mycp+'&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
      });

      this.baseLayers["OSMDE"] = L.tileLayer('https://{s}://{z}/{x}/{y}{r}.png', {
	    maxZoom: 19,
          attribution: mycp+'&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors &copy; <a href="https://carto.com">CARTO</a>'
      });

	this.baseLayers["TopPlusOpen"] = L.tileLayer('https://sgx.geodatenzentrum.de/wmts_topplus_open/tile/1.0.0/web/default/WEBMERCATOR/{z}/{y}/{x}.png', {
		maxZoom: 18,
		attribution: mycp+'<a href="https://www.bkg.bund.de/SharedDocs/Produktinformationen/BKG/DE/P-2017/170922-TopPlus-Web-Open.html">BKG</a>',referrerPolicy: 'strict-origin'});
	
// https://tileserver.4umaps.com/${z}/${x}/${y}.png
// zoomlevel 16
// https://www.4umaps.com/
	
	if(JS.gpxmap.OSM_Cycle_Api_Key && JS.gpxmap.OSM_Cycle_Api_Key.length>0) {
		this.baseLayers["Cycle"] = L.tileLayer('https://{s}.tile.thunderforest.com/cycle/{z}/{x}/{y}.png?apikey='+JS.gpxmap.OSM_Cycle_Api_Key, {
			maxZoom: 22,
			attribution: mycp+'<a href="https://www.thunderforest.com/" target="_blank">OpenCycleMap</a><a href="https://creativecommons.org/licenses/by-sa/2.0/" target="_blank">CC</a>',referrerPolicy: 'strict-origin'});
	}

	if(JS.gpxmap.OSM_Landscape_Api_Key && JS.gpxmap.OSM_Landscape_Api_Key.length>0) {
		this.baseLayers["Landscape"] = L.tileLayer('https://{s}.tile.thunderforest.com/landscape/{z}/{x}/{y}.png?apikey='+JS.gpxmap.OSM_Landscape_Api_Key, {
			maxZoom: 22,
			attribution: mycp+'<a href="https://www.thunderforest.com/" target="_blank">OpenLandscapeMap</a><a href="https://creativecommons.org/licenses/by-sa/2.0/" target="_blank">CC</a>',referrerPolicy: 'strict-origin'
		});
	}

	if(JS.gpxmap.OSM_Outdoors_Api_Key && JS.gpxmap.OSM_Outdoors_Api_Key.length>0) {
		this.baseLayers["Outdoors"] = L.tileLayer('https://{s}.tile.thunderforest.com/outdoors/{z}/{x}/{y}.png?apikey='+JS.gpxmap.OSM_Outdoors_Api_Key, {
			maxZoom: 22,
			attribution: mycp+'<a href="https://www.thunderforest.com/" target="_blank">OpenOutdoorsMap</a><a href="https://creativecommons.org/licenses/by-sa/2.0/" target="_blank">CC</a>',referrerPolicy: 'strict-origin'
		});
	}

	this.baseLayers[JS.gpxmap.strings[JS.gpxmap.parameters.doclang].noMap]= L.tileLayer(JS.gpxmap.Path+"Icons/Grau256x256.png", { 
		maxZoom: 22,
		attribution: mycp,referrerPolicy: 'strict-origin'
	});

	this.overlayLayers = {}; 

	this.overlayLayers["Open Sea"] = L.tileLayer('https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png', {
		attribution: '<a href="https://www.openseamap.org">OpenSeaMap</a>',referrerPolicy: 'strict-origin'
	});

	this.overlayLayers["Hiking"] = L.tileLayer('https://tile.waymarkedtrails.org/hiking/{z}/{x}/{y}.png', {
		attribution: '<a href="https://waymarkedtrails.org">Hiking</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC</a>)',referrerPolicy: 'strict-origin'
	});
	
	this.overlayLayers["Cycling"] = L.tileLayer('https://tile.waymarkedtrails.org/cycling/{z}/{x}/{y}.png', {
		attribution: '<a href="https://waymarkedtrails.org">Cycling</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC</a>)',referrerPolicy: 'strict-origin'
	});

	// ['hiking', 'cycling', 'mtb', 'skating', 'slopes', 'riding'];
	
	var genugplatz = JS.platzgenug(makemap.mapdiv);

	this.map = L.map(mapcanvas, { 
//		layers: osm, 
		closePopupOnClick: false,
		scrollWheelZoom: genugplatz & makemap.parameters.scrollwheelzoom,
		tap: genugplatz,
		keyboard: genugplatz,
		touchZoom: true,
		dragging: true,
	} );
	
	JS.handle_touch_action(dieses,genugplatz);
	
	if(makemap.parameters.unit=="si") L.control.scale({imperial:false}).addTo(this.map); // Mit Massstab km
	else L.control.scale({metric:false}).addTo(this.map); // Mit Massstab ml
	
	var ctrl_layer = null;
	var showmaptypecontroll_save = makemap.parameters.showmaptypecontroll;
	JS.onresize(mapcanvas,function(w,h) {
		makemap.parameters.showmaptypecontroll = (w>200 && h>190 && showmaptypecontroll_save);
		if(makemap.parameters.showmaptypecontroll) {
			if(!ctrl_layer) ctrl_layer = L.control.layers(dieses.baseLayers, dieses.overlayLayers).addTo(dieses.map);
		}
		else {
			if(ctrl_layer) {
				ctrl_layer.remove();
				ctrl_layer = null;
			}
		}
	},true);

	// Button fuer Full Screen / normale Groesse
	var fullscreen = false;
	if(makemap.parameters.fullscreenbutton) {
		var fsb = document.createElement("button");
		fsb.style.backgroundColor = "transparent";
		fsb.style.border = "none"; 
		fsb.style.padding = "7px 7px 7px 0";
		fsb.style.cursor = "pointer";
		var fsbim = document.createElement("img");
		fsbim.width = 31;
		fsbim.height = 31;
		fsbim.src = JS.gpxmap.Path+"Icons/fullscreen_p.svg";
		fsb.title = fsbim.title = fsbim.alt = JS.gpxmap.strings[JS.gpxmap.parameters.doclang].fullScreen;
		fsbim.large = false;
		var ele = mapcanvas.parentNode;
		fsb.onclick = function() {
			this.blur();
			if(fsbim.large) {
				document.body.style.overflow = "";
				fsbim.src = JS.gpxmap.Path+"Icons/fullscreen_p.svg";
				fsb.title = fsbim.title = fsbim.alt = JS.gpxmap.strings[JS.gpxmap.parameters.doclang].fullScreen;
				ele.style.left = ele.oleft + "px";
				ele.style.top = ele.otop + "px";
				ele.style.width = ele.owidth + "px";
				ele.style.height = ele.oheight + "px";
        ele.style.margin = ele.omargin;
        ele.style.padding = ele.opadding;
				window.setTimeout(function() {
					JS.removeClass("JSfull",ele);
					ele.style.position = ele.sposition; 
					ele.style.left = ele.sleft;
					ele.style.top = ele.stop;
					ele.style.width = ele.swidth;
					ele.style.height = ele.sheight;
					//ele.style.zIndex = ele.szindex;
				},1000);
				JS.handle_touch_action(dieses,genugplatz);
				fullscreen = false;
			}
			else {
				document.body.style.overflow = "hidden";
				fsbim.src = JS.gpxmap.Path+"Icons/fullscreen_m.svg";
				fsb.title = fsbim.title = fsbim.alt = JS.gpxmap.strings[JS.gpxmap.parameters.doclang].normalSize;
				var scrollY = 0;
				if(document.documentElement.scrollTop && document.documentElement.scrollTop!=0)  scrollY = document.documentElement.scrollTop;
				else if(document.body.scrollTop && document.body.scrollTop!=0)  scrollY = document.body.scrollTop;
				else if(window.scrollY) scrollY = window.scrollY;
				else if(window.pageYOffset) scrollY = window.pageYOffset;
				var rect = JS.getRect(ele);
			  ele.oleft = rect.left;
				ele.otop =  rect.top - scrollY;
				ele.owidth = rect.width;
				ele.oheight = rect.height;
				//ele.szindex = ele.style.zIndex;
				ele.sposition = ele.style.position;
        ele.omargin = ele.style.margin;
        ele.opadding = ele.style.padding;
				ele.sleft = ele.style.left;
				ele.stop = ele.style.top;
				ele.swidth = ele.style.width;
				ele.sheight = ele.style.height;
				ele.style.position = "fixed";
				ele.style.left = ele.oleft+"px";
				ele.style.top = ele.otop+"px";
				ele.style.width = ele.owidth+"px";
				ele.style.height = ele.oheight+"px";
				//ele.style.zIndex = "1001";
				window.setTimeout(function() {
					JS.addClass("JSfull",ele);
					ele.style.width = "100%";
					ele.style.height = "100%";
					ele.style.left = "0px";
					ele.style.top = "0px";
          ele.style.margin = "0px";
          ele.style.padding = "0px";
				},100);
				dieses.map.scrollWheelZoom.enable();
				JS.handle_touch_action(dieses,true);
				makemap.mapdiv.focus();
				fullscreen = true;
			}
			fsbim.large = !fsbim.large;
		};
		fsb.appendChild(fsbim);
		fsb.index = 0;
		L.Control.Fsbutton = L.Control.extend({
			onAdd: function(map) {
				return fsb;
			}
		});
		var fsbutton = new L.Control.Fsbutton({ position: 'topright' });
		fsbutton.addTo(this.map);
	} // fullscreenbutton
	
	// Button fuer Traffic-Layer
	if(makemap.parameters.trafficbutton) {
		console.warn("Traffic-Layer unter Leaflet nicht unterstuetzt.");
	}
		
	// Button fuer Anzeige aktuelle Position
	if(makemap.parameters.currentlocationbutton) {
		var clb = document.createElement("button");
		clb.style.backgroundColor = "white";
		clb.style.border = "none"; 
		clb.style.width = "28px"; 
		clb.style.height = "28px";
		clb.style.margin = "10px 10px 0 0";
		clb.style.borderRadius = "2px";
		clb.style.cursor = "pointer";
		clb.title = JS.gpxmap.strings[JS.gpxmap.parameters.doclang].showCurrentLocation;
		var clbimg = document.createElement("img");
		clbimg.style.position = "absolute";
		clbimg.style.top = "50%";
		clbimg.style.left = "50%";
		clbimg.style.transform = "translate(-50%, -50%)";
		clbimg.src = JS.gpxmap.Path+"Icons/whereami.svg";
		var wpid = -1, marker = null, first;
		clb.onclick = function() {
			this.blur();
			if (navigator.geolocation) {
				var geolocpos = function(position) {
					var lat = position.coords.latitude;
					var lon = position.coords.longitude;
					marker.setLatLng([lat,lon]);
					if(first) { 
						dieses.map.setView([lat,lon]);
						first = false;
					}
				}
				var geolocerror = function(error) {
					var errorCodes = ["Permission Denied","Position unavailible","Timeout"];
					var errorString = (error.code<=3)?errorCodes[error.code-1]:"Error code: "+error.code;
					JS.Debug_Info("Geolocation-Dienst fehlgeschlagen!",errorString+". "+error.message,true);
				}
				first = true;
				if(!marker) marker = dieses.Marker({lat:0,lon:0},JS.icons.CL)[0];
				if ( wpid == -1 ) {
					clb.title = JS.gpxmap.strings[JS.gpxmap.parameters.doclang].hideCurrentLocation;
					wpid = navigator.geolocation.watchPosition(geolocpos,geolocerror,{enableHighAccuracy:true, timeout: 5000, maximumAge: 60000});
					marker.addTo(dieses.map); 
					JS.Debug_Info("","Geolocation-Dienst wird eingerichtet.",false);
				}
				else {
					clb.title = JS.gpxmap.strings[JS.gpxmap.parameters.doclang].showCurrentLocation;
					navigator.geolocation.clearWatch(wpid);
					wpid = -1;
					marker.remove();
					JS.Debug_Info("","Geolocation-Dienst wird abgeschaltet.",false);
				}
			}
			else JS.Debug_Info("geolocation","Geolocation wird nicht unterstuetzt!",true);
		} // click-Handler
		clb.appendChild(clbimg);
		L.Control.Clbutton = L.Control.extend({
			onAdd: function(map) {
				return clb;
			}
		});
		var clbutton = new L.Control.Clbutton({ position: 'topright' });
		clbutton.addTo(this.map);
	} // currentlocationbutton

	// Scalieren nach MAP-Resize
	dieses.zoomstatus = {};
	dieses.zoomstatus.iszoomed = false;
	dieses.zoomstatus.zoom_changed = function() {
		dieses.zoomstatus.iszoomed = true; 
		dieses.zoomstatus.level = dieses.map.getZoom();
		dieses.zoomstatus.w = mapcanvas.offsetWidth;
		dieses.zoomstatus.h = mapcanvas.offsetHeight;
	}
	dieses.zoomstatus.move_end = function() {
		dieses.zoomstatus.iszoomed = true; 
		dieses.mapcenter = dieses.map.getCenter();
	}
	dieses.map.on("moveend", dieses.zoomstatus.move_end);
	JS.onresize(mapcanvas,function(w,h) {
		if(w*h==0) return;
		dieses.map.invalidateSize();
		dieses.map.setView(dieses.mapcenter);
		dieses.map.off("zoomend", dieses.zoomstatus.zoom_changed);
		if(dieses.zoomstatus.iszoomed) {
			var dz = Math.round(Math.min(Math.log(w/dieses.zoomstatus.w)/Math.LN2,Math.log(h/dieses.zoomstatus.h)/Math.LN2));
			dieses.map.setZoom(dieses.zoomstatus.level+dz);
		}
		else {
			if(dieses.bounds) {
				dieses.map.fitBounds(dieses.bounds,{padding:[20,20]});
				dieses.map.setView(dieses.mapcenter);
				dieses.zoomstatus.level = dieses.map.getZoom();
				dieses.zoomstatus.w = w;
				dieses.zoomstatus.h = h;
			}
		}
		if(!fullscreen) {
			genugplatz = JS.platzgenug(makemap.mapdiv);
			JS.handle_touch_action(dieses,genugplatz);
		}
	});

} // JS.Map

JS.Map.prototype.MapEvents = {id:-1, events:[]};

JS.Map.prototype.addMapEvent = function(event,fkt) {	
	this.map.on(event,fkt);
	this.MapEvents.id ++;
	this.MapEvents.events[this.MapEvents.id] = {event: event, fkt: fkt} ;
	return this.MapEvents.id ++;;
} // addMapEvent

JS.Map.prototype.addMapEventOnce = function(event,fkt) {	
	var dieses = this;
	var oncefkt = function(ev) {
		fkt(ev);
		dieses.map.off(event,oncefkt);
	}
	this.map.on(event,oncefkt);
	this.MapEvents.id ++;
	this.MapEvents.events[this.MapEvents.id] = {event: event, fkt: oncefkt} ;
	return this.MapEvents.id ++;;
} // addMapEventOnce

JS.Map.prototype.removeEvent = function(eventid) {
	this.map.off(this.MapEvents.events[eventid].event, this.MapEvents.events[eventid].fkt);
} // removeMapEvent

JS.Map.prototype.getZoom = function() {
	return {zoom:this.map.getZoom(),maxzoom:this.map.getMaxZoom()}; 
}

JS.Map.prototype.change = function(maptype) {
	var mt = "OSM";
	if(maptype in this.baseLayers) mt = maptype;
	if(maptype in this.overlayLayers) {
		this.overlayLayers[maptype].addTo(this.map);
		mt = "OSMDE";
	}
	this.baseLayers[mt].addTo(this.map);
	JS.Debug_Info(this.id,"Maptype, gewaehlt: "+maptype+", eingestellt: "+mt,false);
} // change

JS.Map.prototype.getPixelPerKM = function(gpxdaten) {
	var bounds = this.map.getBounds();
	if(bounds) {
		var latlon1 = bounds.getNorthEast();
		var latlon2 = bounds.getSouthWest();
		var korrfak = 1;
	}
	else {
		JS.Debug_Info(" getPixelPerKM","Bounds konnten nicht gelesen werden, nehme Min/Max-Werte aus GPX-Daten",false);
		var latlon1 = {lat: gpxdaten.latmax, lng: gpxdaten.lonmax};
		var latlon2 = {lat: gpxdaten.latmin, lng: gpxdaten.lonmin};
		var korrfak = 0.7;
	}
	JS.entf.init(latlon1.lat,latlon1.lng,0);
	var dist = JS.entf.rechne(latlon2.lat,latlon2.lng,0);
	JS.entf.init(latlon1.lat,latlon1.lng,0);
	var xdist = JS.entf.rechne(latlon1.lat,latlon2.lng,0);
	JS.entf.init(latlon1.lat,latlon1.lng,0);
	var ydist = JS.entf.rechne(latlon2.lat,latlon1.lng,0);
	var w = this.mapcanvas.offsetWidth;
	var h = this.mapcanvas.offsetHeight;
	var wh = Math.sqrt(w*w+h*h);
	var ppk = Math.min(w/xdist,h/ydist);
	ppk = Math.min(ppk,wh/dist);
	ppk *= korrfak;
	return ppk;
} // getPixelPerKM

JS.Map.prototype.rescale = function(gpxdaten) {
  var dieses = this;
	dieses.map.off("moveend", dieses.zoomstatus.move_end);
	dieses.map.off("zoomend", dieses.zoomstatus.zoom_changed);
	dieses.bounds = [[gpxdaten.latmin,gpxdaten.lonmin], [gpxdaten.latmax,gpxdaten.lonmax]];
	this.map.fitBounds(dieses.bounds,{padding:[20,20]});
	dieses.zoomstatus.iszoomed = false;	
	dieses.mapcenter = dieses.map.getCenter();
	dieses.zoomstatus.level = dieses.map.getZoom();
	dieses.zoomstatus.w = dieses.mapcanvas.offsetWidth;
	dieses.zoomstatus.h = dieses.mapcanvas.offsetHeight;
	dieses.map.on("zoomend", dieses.zoomstatus.zoom_changed);
	dieses.map.on("moveend", dieses.zoomstatus.move_end);
/*	var zoom = dieses.getZoom(); // --------------------!!!!!!!!!!!!!!!!!!!!!---------------------!!!!!!!!!!!!!!
	console.log("rescale", zoom.zoom, zoom.maxzoom);
	if(zoom.zoom > zoom.maxzoom) {
		dieses.map.setZoom(zoom.maxzoom);
		dieses.zoomstatus.level = zoom.maxzoom;
		console.log("rescale", zoom.zoom, zoom.maxzoom);
	}*/
} // rescale

JS.Map.prototype.infowindow = function(info,coord) {
//	var popup = L.popup({maxWidth: this.map.getContainer().offsetWidth-200, autoClose: false }) 
	var popup = L.popup({maxWidth: this.map.getContainer().offsetWidth*0.8, 
	                     maxHeight: this.map.getContainer().offsetHeight*0.9, autoClose: false }) 
		.setLatLng(coord);
		if(typeof(info) == "string") 
			popup.setContent("<div class='JSinfofenster_gm'>"+info+"</div>");
		else                       
			popup.setContent(info);
		popup.openOn(this.map);
	return popup;
}
JS.Map.prototype.gminfowindow = JS.Map.prototype.infowindow; // wg Kompatibilitaet

JS.Map.prototype.simpleLine = function(slat,slon,elat,elon) {
	var line = L.polyline( [[slat,slon],[elat,elon]], { color: "#000", weight: 1, opacity: 1 } );
	line.addTo(this.map);
	return line;
} // simpleLine

JS.Map.prototype.Polyline = function(daten,controls,route_oder_track,cols,click_fkt) {
	var dieses = this;
	var coords = daten.daten; 
	var npt = coords.length, latlng = [], infofenster, line=[];
	var cbtype;
	if(route_oder_track == "Track") cbtype = "click_Track";
	else if(route_oder_track == "Route") cbtype = "click_Route";
	else cbtype = "?";
	var infotext = daten.info;
	var line_i;
	if(cols && cols.length) {
		for(var i=0;i<npt-1;i++) {
			line_i = 	L.polyline([coords[i],coords[i+1]],{color: cols[i], weight: controls.width, opacity: controls.opac});
			line_i.addTo(this.map);
			line.push(line_i);
		}
	}
	else {
		var col;
		if(JS.gpxmap.Farben && JS.gpxmap.Farben[daten.name]) col = JS.gpxmap.Farben[daten.name];
		else col = controls.col;
		line[0] = L.polyline(coords,{color: col, weight: controls.width, opacity: controls.opac});
		line[0].addTo(this.map);
	}
	
	var overline = line.length;
	line[overline] = L.polyline(coords,{color: "white", weight: 2*controls.owidth, opacity: 0.5}).addTo(dieses.map).bringToBack();
	
	var delta = function(coords,i,latlon) {
		return coords[i+1][latlon]-coords[i-1][latlon] + 0.5*(coords[i+2][latlon]-coords[i-2][latlon]);
	} // delta

	var atan2 = function(x,y) {
		if(x>0) return Math.atan(y/x);
		else if (x<0) return Math.atan(y/x) + Math.PI;
		else if (x==0 && y>0) return Math.PI;
		else                  return -Math.PI;
	} // atan2
	
	var findNextX = function(a,x) {
		var l = a.length,istep=l/4,i=l/2;
		if(l<3) return 0;
		else if (l<5) return 2;
		while(istep>0.5) {
			if(x < a[Math.floor(i)].x) i -= istep;
			else i += istep;
			istep = istep/2; 
		}
		return Math.floor(i);
	} // findNextX
	
	if( (this.makemap.parameters.arrowtrack && route_oder_track == "Track") || (this.makemap.parameters.arrowroute && route_oder_track == "Route") ) {			
		var bounds = this.map.getBounds();
		if(bounds) {
			var size_px = Math.min(this.mapcanvas.offsetWidth,this.mapcanvas.offsetHeight);
			var latlon1 = bounds.getNorthEast();
			var latlon2 = bounds.getSouthWest();
			JS.entf.init(latlon1.lat,latlon1.lng,0);
			var sizelon_km = JS.entf.rechne(latlon1.lat,latlon2.lng,0);
			JS.entf.init(latlon1.lat,latlon1.lng,0);
			var sizelat_km = JS.entf.rechne(latlon2.lat,latlon1.lng,0);
			var size_km = Math.max(sizelon_km,sizelat_km);
			var dx_arrow = 400/size_px * size_km;
			dx_arrow = daten.laenge/Math.ceil(daten.laenge/dx_arrow);
			if(dx_arrow > daten.laenge) dx_arrow = daten.laenge;
		}
		else {
			dx_arrow = daten.laenge/5;
		}
		var direction;
		var arr_col = controls.col;
		if(route_oder_track == "Track" && this.makemap.parameters.arrowtrackcol.length>0) arr_col = this.makemap.parameters.arrowtrackcol;
		if(route_oder_track == "Route" && this.makemap.parameters.arrowroutecol.length>0) arr_col = this.makemap.parameters.arrowroutecol;
		if(npt>=5) {
			for(var x=dx_arrow/2,i;x<daten.laenge;x+=dx_arrow) {
				i = findNextX(coords,x);
				if(i<2) i=2; if(i>npt-3) i = npt-3;
				direction = atan2(delta(coords,i,"lat"),delta(coords,i,"lon"));
				line = line.concat(dieses.setDirectionMarker(coords[i],direction,arr_col));
			}
		}
	} // if arrowtrack
	
	var eventline = line.length;
	line[eventline] = L.polyline(coords,{color: "black", weight: controls.width*5, opacity: 0.01});
	line[eventline].addTo(this.map);

	if(this.makemap.parameters.trackover) {
		if(!dieses.trackinfofenster) dieses.trackinfofenster = JS.Infofenster(this.map);
		dieses.trackinfofenster.hide();
		line[eventline].on('mouseover', function(o) {
			var ocol = controls.ocol;
			if(ocol=="" && !(cols && cols.length)) {
				ocol = col;				
			}
			if(ocol=="") ocol = "black";
			line[overline].setStyle({color: ocol, opacity: 1.0});
			dieses.trackinfofenster.content(infotext);
			dieses.trackinfofenster.show();
		});
		line[eventline].on('mouseout', function(o) {
			line[overline].setStyle({color: "white", opacity: 0.5});
			dieses.trackinfofenster.hide();
		});
	} // trackover */
	
	if(this.makemap.parameters.trackclick) {
		line[eventline].on('click', function(o) {
			var retval = true;
			if(typeof(JS.gpxmap.callback)=="function") 
				retval = JS.gpxmap.callback({type:cbtype,infotext:infotext,id:dieses.id,name:daten.name});
			let notCanceled = dieses.makemap.fireEvent(dieses.makemap,dieses.makemap.events[cbtype],{infotext:infotext,name:daten.name,clickEvent:o});
			retval = notCanceled && retval;
			if(retval) {
				if(daten.link) {
					JS.openurl(daten.link,dieses.makemap.parameters.popup_Pars);
				}
				else {
					var mapcenter = dieses.map.getCenter();
					if(click_fkt) click_fkt(dieses,coords,o.latlng);
					else dieses.infowindow(infotext, o.latlng); 
					dieses.map.on("popupclose", function() { dieses.map.setView(mapcenter) });
				}
			} 	
		} );
	} // trackclick

	var colors = [];
	if(cols && cols.length) colors = cols;
	else colors[0] = col;
	if(route_oder_track == "Track") {
		dieses.makemap.fireEvent(dieses.makemap,dieses.makemap.events.created_Track,{line:line,daten:daten,colors:colors});
	}
	else if(route_oder_track == "Route") {
		dieses.makemap.fireEvent(dieses.makemap,dieses.makemap.events.created_Route,{line:line,daten:daten,colors:colors});
	}

	return line;
} // Polyline

JS.Map.prototype.setMarker = function(coord,icon,title) {
	var marker = [];
	var tooltipoffset = [0,-15];
	if(icon) {
		if(typeof(icon) == "object") {
			var options = {popupAnchor: [-3, -76]};
			if (icon.icon) {
				options.iconUrl = icon.icon.url;
				options.iconAnchor = [icon.icon.anchor.x, icon.icon.anchor.y];
				if(icon.icon.size) options.iconSize = [icon.icon.size.width,icon.icon.size.height];
				tooltipoffset = [0, -icon.icon.anchor.y];
			}
			if(this.makemap.parameters.shwpshadow) {
				if(icon.icon) {
					if (icon.shadow) {
						options.shadowUrl = icon.shadow.url;
						options.shadowAnchor = [icon.shadow.anchor.x, icon.shadow.anchor.y];
					}
				}
				/*else {
					options.shadowUrl = JS.icons.DefShadow.shadow.url;
					options.shadowAnchor = [JS.icons.DefShadow.shadow.anchor.x, JS.icons.DefShadow.shadow.anchor.y];				
				}*/
			}
			var thisIcon = L.Icon.extend({ options: options });
			var thisicon = new thisIcon();
			marker[0] = L.marker(coord, {icon: thisicon, title: title, zIndexOffset: 500} ); 
		}
//		else if(typeof(icon) == "string" && icon.length && 0xD800 <= icon.charCodeAt(0) && icon.charCodeAt(0) <= 0xDBFF) { // Mehr-Byte-Unicode
		else if(typeof(icon) == "string" && icon.length < 3) { // Kurzer String oder Emoji
			var html = "<div style='position: absolute; font-size: 3em; transform: translate(-50%, -50%)'>"+icon+"</div>"
			var thisicon = L.divIcon({className:"JStext-icon", html: html, iconAnchor: [0, 0] });
			marker[0] = L.marker(coord, {icon: thisicon, title: title});
		}
		else {
			marker[0] = L.marker(coord, {title: title});
		}
	}
	else {
		marker[0] = L.marker(coord, {title: title});
	}
	marker[0].addTo(this.map);
	if(this.makemap.parameters.shwptooltip) if(title && title.length) marker[0].bindTooltip(title,{ permanent: true, direction: 'top', offset: tooltipoffset });
	return marker;
} // setMarker
  
JS.Map.prototype.setClusterMarker = function(coord,icon,title,label) { 
	var url = icon.icon.url;
	var w = icon.icon.size.width + icon.icon.size.widthUnit;
	var h = icon.icon.size.height + icon.icon.size.heightUnit;
	var marker = [];
	var html = "<div style='background-image:url("+url+");background-repeat: no-repeat;width:"+w+";height:"+h+"'><div>"+label+"</div></div>";
	var thisicon = L.divIcon({className:"JScluster-icon", html: html, iconAnchor: [icon.icon.anchor.x, icon.icon.anchor.y] });
	marker[0] = L.marker(coord, {icon: thisicon, title: title, zIndexOffset: 500 } ); 
	marker[0].addTo(this.map);
	return marker;
} // setClusterMarker
  
JS.Map.prototype.setDistanceMarker = function(coord,icon,title,label) { 
	var url = icon.icon.url;
	var w = icon.icon.size.width + icon.icon.size.widthUnit;
	var h = icon.icon.size.height + icon.icon.size.heightUnit;
	var marker = [];
	var html = "<div style='padding-top:1em;background-image:url("+url+");background-repeat: no-repeat;width:"+w+";height:"+h+"'><div>"+label+"</div></div>";
	var thisicon = L.divIcon({className:"JScluster-icon", html: html, iconAnchor: [icon.icon.anchor.x, icon.icon.anchor.y] });
	marker[0] = L.marker(coord, {icon: thisicon, title: title, zIndexOffset: 500 } ); 
	marker[0].addTo(this.map);
	return marker;
} // setDistanceMarker
  
JS.Map.prototype.setDirectionMarker = function(coord,direction,color) {
	var marker = [];
	var dir = direction - Math.PI/2;
	var html = "<div style='color:"+color+"; transform: translate(-50%,-50%) rotate("+dir+"rad)'>"+this.makemap.parameters.arrowsymbol+"</div>";
	var thisicon = L.divIcon({className: "JSdirection-marker", iconAnchor: [0, 0], html: html });
	marker[0] = L.marker(coord, {icon: thisicon, zIndexOffset: 500} ); 
	marker[0].addTo(this.map);
	return marker;
} // setDirectionMarker
  
JS.Map.prototype.Marker = function(coord,icon,title) { 
	return this.setMarker(coord,icon,title); 
} // Marker

JS.Map.prototype.Marker_Link = function(coord,icon,titel,url,popup_Pars) { 
	var dieses = this;
	var marker = this.setMarker(coord,icon,titel);
	var text = coord.info;
	marker[0].on('click', function(o) {
		let notCanceled = dieses.makemap.fireEvent(dieses.makemap,dieses.makemap.events.click_Marker_Link,{marker:marker[0],coord:coord,titel:titel,text:text,clickEvent:o});
		if(notCanceled) JS.openurl(url,popup_Pars);
	});
	dieses.makemap.fireEvent(dieses.makemap,dieses.makemap.events.created_Marker_Link,{marker:marker[0],coord:coord,titel:titel,text:text});
	return marker;
} // Marker_Link

JS.Map.prototype.Marker_Text = function(coord,icon,titel) {
	var dieses = this;
	var mapcenter,clk_ev;
	var marker = this.setMarker(coord,icon,titel);
	var text = coord.info;
	marker[0].on("click", function(o) {
		var retval = true;
		if(typeof(JS.gpxmap.callback)=="function") 
			retval = JS.gpxmap.callback({type:"click_Marker_Text",coord:coord,titel:titel,text:text,id:dieses.id});
		let notCanceled = dieses.makemap.fireEvent(dieses.makemap,dieses.makemap.events.click_Marker_Text,{marker:marker[0],coord:coord,titel:titel,text:text,clickEvent:o});
		retval = notCanceled && retval;
		if(retval) {
			var mapcenter = dieses.map.getCenter();
			var infowindow = dieses.infowindow("<div>"+text+"</div>", coord);
			dieses.map.on("popupclose", function() { 
				dieses.map.setView(mapcenter);
			});
		}
	});

	dieses.makemap.fireEvent(dieses.makemap,dieses.makemap.events.created_Marker_Text,{marker:marker[0],coord:coord,titel:titel,text:text});

	return marker;
} // Marker_Text

JS.Map.prototype.Marker_Bild = function(coord,icon,bild) { 
	var dieses = this;
	var mapcenter,minibild;
	var marker = this.setMarker(coord,icon);
	var img = new Image();
	img.loaded = false;
	var bild_icon;
	
	marker[0].on("mouseover", function() {
		if(img.loaded) {
			minibild = L.marker(coord, {icon: bild_icon}).addTo(dieses.map);
		}
		else {
			img.onload = function() { 
				img.loaded = true;
				var w = img.width, h = img.height, mw, mh;
				if(w>h) { mw = dieses.makemap.parameters.groesseminibild; mh = Math.round(h*mw/w); }
				else    { mh = dieses.makemap.parameters.groesseminibild; mw = Math.round(w*mh/h); }
				bild_icon = L.icon({
					iconUrl: bild,
					iconSize: [mw, mh],
					iconAnchor: [23, 0]
				});
				minibild = L.marker(coord, {icon: bild_icon}).addTo(dieses.map);
			}
			img.onerror = function() {
				JS.Debug_Info(this.src,"konnte nicht geladen werden!",false);
			}
			img.src = bild;
		}
	});
	marker[0].on('mouseout', function() { 
		if(minibild) {
			minibild.remove(); 
			minibild = null;
		}
		img.onload = null;
	});
	
	var text = coord.info;
	marker[0].on("click", function(o) {
		var retval = true;
		if(typeof(JS.gpxmap.callback)=="function") 
			retval = JS.gpxmap.callback({type:"click_Marker_Bild",marker:marker[0],coord:coord,src:bild,text:text,id:dieses.id});
		let notCanceled = dieses.makemap.fireEvent(dieses.makemap,dieses.makemap.events.click_Marker_Bild,{marker:marker[0],coord:coord,src:bild,text:text,clickEvent:o});
		retval = notCanceled && retval;
		if(retval) {
			if(img.loaded) {
				afterimgload();
			}
			else {
				img.onload = function() { 
					img.loaded = true;
					afterimgload();
				}
				img.onerror = function() {
					JS.Debug_Info(this.src,"konnte nicht geladen werden!",false);
				}
				img.src = bild;
			}
		}
	});

	var afterimgload = function() {
		var w = img.width, h = img.height;
		var mapdiv = dieses.map.getContainer();
		var mw = mapdiv.offsetWidth-200, mh = mapdiv.offsetHeight-200;
		if(mw<50 || mh<50) return;
		if(w>mw) { h = Math.round(h*mw/w); w = mw; }; 
		if(h>mh) { w = Math.round(w*mh/h); h = mh; }
		var container = document.createElement("div");
		container.style.padding = "10px";
		container.style.width = (w) + "px";
		container.style.height = (h+50) + "px";
		container.style.backgroundColor = "white";
		container.style.overflow = "auto";
		container.innerHTML = "<img src='"+bild+"' width="+w+" height="+h+"><br>"+text;
		if(coord.link && coord.link.length) {
			container.onclick = function() { JS.openurl(coord.link,""); };
			container.style.cursor = "pointer";
		}
		var mapcenter = dieses.map.getCenter();
		var infowindow = dieses.infowindow(container, coord); 
		dieses.map.on("popupclose", function() { dieses.map.setView(mapcenter);	});
		if(container.clientHeight<container.scrollHeight) container.style.width = (w+20) + "px";
	}

	if(typeof(JS.gpxmap.callback)=="function") 
		JS.gpxmap.callback({type:"created_Marker_Bild",marker:marker[0],coord:coord,src:bild,text:text,id:dieses.id});
	dieses.makemap.fireEvent(dieses.makemap,dieses.makemap.events.created_Marker_Bild,{marker:marker[0],coord:coord,src:bild,text:text});

	return marker;
} // Marker_Bild 
 
JS.Map.prototype.Marker_Cluster = function(cluster,wpts,strings) {
	var dieses = this;
	var marker,latmin,latmax,lonmin,lonmax,title;
	var zbb;
	var title = cluster.members.length+" "+strings.wpts+":"; // " Wegpunkte:";
	var label = cluster.members.length+"";
	for(var i=0;i<cluster.members.length;i++) {
		var  t = wpts[cluster.members[i]].name;
		if (t.indexOf("data:image")!=-1) t = strings.pwpt; // "Bildwegpunkt";
		else if (JS.checkImageName(t)) t = t.substring(t.lastIndexOf("/")+1,t.lastIndexOf("."));
		title += "\n- " + t;
	}
	title += "\n"+strings.clkz; // "\nZum Zoomen klicken";
	
	var marker = this.setClusterMarker(cluster,JS.icons.Cluster,title,label);

	marker[0].on("click", function() {
		if(dieses.cluster_zoomhistory.length==0) {
			var zbbe = document.createElement("button");
			zbbe.innerHTML = "&#x21b5";
			zbbe.style.color = "black"; //"#444";
			zbbe.style.backgroundColor = "white";
			zbbe.style.fontWeight ="bold";
			zbbe.style.fontSize = "24px";
			//zbbe.style.margin = "10px 10px 0 0";
			zbbe.style.lineHeight = 0;
			zbbe.style.width = "28px";
			zbbe.style.height = "28px";
			zbbe.style.border = "none";
			zbbe.style.borderRadius = "2px";
			zbbe.style.cursor = "pointer";
			zbbe.title = strings.zb; // "Zurueck zoomen";
			zbbe.onclick = function() {
				this.blur();
				dieses.map.fitBounds(dieses.cluster_zoomhistory.pop());
				if(dieses.cluster_zoomhistory.length==0) zbb.remove();;			
			};
			L.Control.Zbbutton = L.Control.extend({
				onAdd: function(map) {
					return zbbe;
				}
			});
			var zbb = new L.Control.Zbbutton({ position: 'topright' });
			zbb.addTo(dieses.map);
		}

		dieses.cluster_zoomhistory.push(dieses.map.getBounds());   
		latmin = lonmin = 1000;
		latmax = lonmax = -1000;
		for(var i=0;i<cluster.members.length;i++) {
			var wp = wpts[cluster.members[i]];
			if(wp.lat<latmin) latmin = wp.lat;
			if(wp.lon<lonmin) lonmin = wp.lon;
			if(wp.lat>latmax) latmax = wp.lat;
			if(wp.lon>lonmax) lonmax = wp.lon;
		}
		dieses.rescale({latmin:latmin,lonmin:lonmin,latmax:latmax,lonmax:lonmax});
	}); 

	return marker;
} // Marker_Cluster

JS.RemoveElement = function(element) { 
	element.remove();
} // JS.RemoveElement    
 
JS.MoveMarker = (function() {
	var MoveMarker_O = function() {
		var marker, Map;
		this.init = function(mp,icon) { 
			if(mp) {
				Map = mp;
				marker = Map.setMarker({lat:0,lon:0},icon)[0]; 
				if(!this.moveinfofenster) this.moveinfofenster = JS.Infofenster(Map.map);
				this.moveinfofenster.show();
			}
		}
		this.pos = function(coord,infotext,maxzoomemove) { 
			if(Map) {
				marker.setLatLng(coord);
				this.moveinfofenster.content(infotext);
				if(Map.map.getZoom() >= maxzoomemove) Map.map.setView(coord);
				else this.moveinfofenster.pos(coord); 
			}      
		}
		this.remove = function() { 
			if(Map) {
				marker.remove();
				this.moveinfofenster.remove();
				this.moveinfofenster = null;
			}
		}
	} // MoveMarker_O
	return new MoveMarker_O();
})(); // JS.MoveMarker

JS.Infofenster = function(map){
	var Infofenster_O = function() {
		this.fenstercontainer = document.createElement("div");
		this.fenstercontainer.style.backgroundColor = "white";
		this.fenstercontainer.style.border = "1px solid gray";
		this.fenstercontainer.style.borderRadius = "3px";
		this.fenstercontainer.style.padding = ".3em";
		//this.fenstercontainer.style.maxWidth = "10em";
		this.fenstercontainer.style.position = "absolute";
		this.fenstercontainer.style.top = "10px";
		this.fenstercontainer.style.left =  "50px";
		this.fenstercontainer.style.zIndex = "1000";
		JS.addClass("JSinfofenster",this.fenstercontainer);
		map.getContainer().appendChild(this.fenstercontainer);
	}
	Infofenster_O.prototype.content = function(content) { 
		this.fenstercontainer.innerHTML = content;
	}
	Infofenster_O.prototype.hide = function() { 
		this.fenstercontainer.hidden = true;
	}
	Infofenster_O.prototype.show = function() {
		this.fenstercontainer.hidden = false;
	}
	Infofenster_O.prototype.remove = function() {
		map.getContainer().removeChild(this.fenstercontainer);
	}
	Infofenster_O.prototype.pos = function(coord) {
		var xy = map.latLngToContainerPoint(coord);
		this.fenstercontainer.style.top = xy.y+"px";
		this.fenstercontainer.style.left = xy.x+"px";
	}
	return new Infofenster_O();
}// JS.Infofenster

JS.getTimezone = function(gpxdaten,cb) { 
}

JS.platzgenug = function(mapdiv) {
	//var docwidth = document.body.offsetWidth;
	var docheight = document.body.offsetHeight;
	var screenwidth = window.innerWidth;
	var screenheight = window.innerHeight;
	var mapwidth = mapdiv.offsetWidth;
	var mapheight = mapdiv.offsetHeight;
	var genugplatz = mapwidth/screenwidth < 0.8;
	genugplatz |= docheight <= screenheight;
	genugplatz |= mapheight/screenheight < 0.8;
	genugplatz = genugplatz?true:false;
	return genugplatz;
}

JS.handle_touch_action = function(dieses,genugplatz) { 
	if(genugplatz && dieses.makemap.parameters.scrollwheelzoom) dieses.map.scrollWheelZoom.enable();
	else if(!(genugplatz && dieses.makemap.parameters.scrollwheelzoom)) dieses.map.scrollWheelZoom.disable();
	if(genugplatz && dieses.map.tap && dieses.map.tap.enable) dieses.map.tap.enable();
	else if(!genugplatz && dieses.map.tap && dieses.map.tap.disable) dieses.map.tap.disable();
	dieses.map.options.tap = genugplatz;
	//dieses.map.touchZoom.enable();
	/*if(genugplatz)*/ //dieses.map.dragging.enable();
	//else if(!(genugplatz)) dieses.map.dragging.disable();
	if(genugplatz) dieses.map.keyboard.enable();
	else if(!genugplatz) dieses.map.keyboard.disable();
	if(genugplatz) dieses.map.getContainer().style.touchAction = "none";
	else dieses.map.getContainer().style.touchAction = "auto";
}
	
// Ende gpxmap_add1.js
