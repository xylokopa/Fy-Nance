// gpxmap_add2.js

"use strict";

window.JS = window.JS || {};
window.JS.gpxmap = window.JS.gpxmap || {};

// Definition der Icons, bei eigenen Icons nur Kleinbuchstaben verwenden.
JS.Icons = function(baseurl) {
	this.DefShadow	= { shadow: { anchor: {x:10,y:35}, url: baseurl+"Icons/shadow50.png" } };
	this.Bild				= { icon:   { anchor: {x: 6,y:31}, url: baseurl+"Icons/scenic.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	//this.MoveMarker	= { icon:   { anchor: {x: 6,y: 6}, url: baseurl+"Icons/marker.gif" } };
	this.MoveMarker	= { icon:   { anchor: {x: 6,y: 6}, url: baseurl+"Icons/marker.svg", 
											scaledSize: { width: 11, height: 11, widthUnit: "px", heightUnit: "px" },
											size: { width: 11, height: 11, widthUnit: "px", heightUnit: "px" } } };
	//this.Cluster		= { icon:   { anchor: {x:16,y:16}, url: baseurl+"Icons/cluster.png" } };
	this.Cluster 		= { icon:   { anchor: {x:16,y:16}, url: baseurl+"Icons/cluster.svg", 
											scaledSize: { width: 31, height: 31, widthUnit: "px", heightUnit: "px" },
											size: { width: 31, height: 31, widthUnit: "px", heightUnit: "px" } } };
	this.Streckenmarker 		= { icon:   { anchor: {x:11,y:11}, url: baseurl+"Icons/streckenmarker.svg", 
											scaledSize: { width: 21, height: 21, widthUnit: "px", heightUnit: "px" },
											size: { width: 21, height: 21, widthUnit: "px", heightUnit: "px" } } };
	this.Kreis			= { icon:   { anchor: {x:38,y:38}, url: baseurl+"Icons/kreis.png" } };
	this.marker_bw	= { icon:   { anchor: {x:12,y:37}, url: baseurl+"Icons/marker-icon_bw.png" } };
	this.CL   			= { icon:   { anchor: {x:26,y:26}, url: baseurl+"Icons/current_location.svg", 
											scaledSize: { width: 51, height: 51, widthUnit: "px", heightUnit: "px" },
											size: { width: 51, height: 51, widthUnit: "px", heightUnit: "px" } } };
	this.lodging		= { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/hotel2.png" },
	//this.lodging		= { icon:   { anchor: {x:15,y:31}, url: baseurl+"Icons/hotel.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	this.hotel = this.lodging;
	this.museum			= { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/museum.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	this.residence	= { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/villa.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	this.library		= { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/library.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	this.park				= { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/park.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	this.castle			= { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/castle.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	this.airport		= { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/airport.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	this.church			= { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/church2.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	this.bridge			= { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/bridge.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	this.bar				= { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/bar.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	this.restaurant	= { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/restaurant.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	this.start			= { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/start.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	this.finish			= { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/finish.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	this.cycling		= { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/cycling.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	this.hiking			= { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/hiking.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	this.flag				= { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/flag.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	this.harbor			= { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/harbor.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	this.anchor			= this.harbor;
	this.campground	= { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/tent.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	this.summit     = { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/peak.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	this.railway    = { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/train.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	this["shopping center"] = { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/shoppingmall.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	this["ground transportation"] = { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/subway.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	this["scenic area"] = { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/photo.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	this["boat ramp"]   = { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/boat.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	this.circle_red 		= { icon:   { anchor: {x:8,y:6}, url: baseurl+"Icons/circle_red.svg", 
											scaledSize: { width: 15, height: 15, widthUnit: "px", heightUnit: "px" },
											size: { width: 15, height: 15, widthUnit: "px", heightUnit: "px" } } };
	this.circle_green		= { icon:   { anchor: {x:8,y:8}, url: baseurl+"Icons/circle_green.svg", 
											scaledSize: { width: 15, height: 15, widthUnit: "px", heightUnit: "px" },
											size: { width: 15, height: 15, widthUnit: "px", heightUnit: "px" } } };
	this.square_red 		= { icon:   { anchor: {x:8,y:8}, url: baseurl+"Icons/square_red.svg", 
											scaledSize: { width: 15, height: 15, widthUnit: "px", heightUnit: "px" },
											size: { width: 15, height: 15, widthUnit: "px", heightUnit: "px" } } };
	this.square_green		= { icon:   { anchor: {x:8,y:8}, url: baseurl+"Icons/square_green.svg", 
											scaledSize: { width: 15, height: 15, widthUnit: "px", heightUnit: "px" },
											size: { width: 15, height: 15, widthUnit: "px", heightUnit: "px" } } };
											// Mit Dank an Hern Kuhn:
	this.video          = { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/video.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	this.panorama       = { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/panorama.png" },
											shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };

	//this.myicon       = { icon:   { anchor: {x:15,y:36}, url: baseurl+"Icons/myicon.png" },
	//                  shadow: { anchor: {x:10,y:31}, url: baseurl+"Icons/shadow.png" } };
	// Most Icons from https://mapicons.mapsmarker.com/
} ;   

JS.gpxmap.setparameters = function() {  
	JS.gpxmap.parameters = {};
	JS.gpxmap.parameters.mapapi = (typeof(Mapapi)!="undefined") ? Mapapi : "osm";   // gm oder osm
	JS.gpxmap.parameters.doclang = (typeof(Doclang)!="undefined") ? Doclang : "auto"; // de, fr oder en
	JS.gpxmap.parameters.unit = (typeof(Unit)!="undefined") ? Unit : "si"; // enus oder en oder us oder air oder water = airwater
	JS.gpxmap.parameters.showmaptypecontroll = (typeof(Showmaptypecontroll)!="undefined") ? Showmaptypecontroll : true;
	JS.gpxmap.parameters.scrollwheelzoom = (typeof(Scrollwheelzoom)!="undefined") ? Scrollwheelzoom : true;
	JS.gpxmap.parameters.fullscreenbutton = (typeof(Fullscreenbutton)!="undefined") ? Fullscreenbutton : false;
	JS.gpxmap.parameters.currentlocationbutton = (typeof(Currentlocationbutton)!="undefined") ? Currentlocationbutton : false;
	JS.gpxmap.parameters.trafficbutton = (typeof(Trafficbutton)!="undefined") ? Trafficbutton : false;
	JS.gpxmap.parameters.trafficonload = (typeof(Trafficonload)!="undefined") ? Trafficonload : true;
	JS.gpxmap.parameters.legende = (typeof(Legende)!="undefined") ? Legende : true;
	JS.gpxmap.parameters.legende_fnm = (typeof(Legende_fnm)!="undefined") ? Legende_fnm  : true;
	JS.gpxmap.parameters.legende_fnm_lm = (typeof(Legende_fnm_lm)!="undefined") ? Legende_fnm_lm  : false;
	JS.gpxmap.parameters.legende_rr = (typeof(Legende_rr)!="undefined") ? Legende_rr  : true;
	JS.gpxmap.parameters.legende_trk = (typeof(Legende_trk)!="undefined") ? Legende_trk : true;
	JS.gpxmap.parameters.legende_rte = (typeof(Legende_rte)!="undefined") ? Legende_rte : true;
	JS.gpxmap.parameters.legende_wpt = (typeof(Legende_wpt)!="undefined") ? Legende_wpt : true;
	JS.gpxmap.parameters.legende_info = (typeof(Legende_info)!="undefined") ? Legende_info : false;
	JS.gpxmap.parameters.gpxtracks = (typeof(Gpxtracks)!="undefined") ? Gpxtracks : true; 
	JS.gpxmap.parameters.gpxrouten = (typeof(Gpxrouten)!="undefined") ? Gpxrouten : true; 
	JS.gpxmap.parameters.gpxwegpunkte = (typeof(Gpxwegpunkte)!="undefined") ? Gpxwegpunkte : true;
	JS.gpxmap.parameters.tracks_verbinden = (typeof(Tracks_verbinden)!="undefined") ? Tracks_verbinden : false;    
	JS.gpxmap.parameters.tracks_dateiuebergreifend_verbinden = (typeof(Tracks_dateiuebergreifend_verbinden)!="undefined") ? Tracks_dateiuebergreifend_verbinden : false;
	JS.gpxmap.parameters.tracksort = (typeof(Tracksort)!="undefined") ? Tracksort : true;
	JS.gpxmap.parameters.dateitrenner = (typeof(Dateitrenner)!="undefined") ? Dateitrenner : ",";
	JS.gpxmap.parameters.readspeed = (typeof(Readspeed)!="undefined") ? Readspeed : true;
	JS.gpxmap.parameters.speedfaktor = (typeof(Speedfaktor)!="undefined") ? Speedfaktor : 3.6; // 3.6 bei m/s, 1,609344 bei mph, 1 bei km/h
	JS.gpxmap.parameters.hfaktor = (typeof(Hfaktor)!="undefined") ? Hfaktor : 1; // Höhe
	JS.gpxmap.parameters.sfaktor = (typeof(Sfaktor)!="undefined") ? Sfaktor : 1; // Steigung
	JS.gpxmap.parameters.vfaktor = (typeof(Vfaktor)!="undefined") ? Vfaktor : 1; // Geschwindigkeit
	JS.gpxmap.parameters.wfaktor = (typeof(Wfaktor)!="undefined") ? Wfaktor : 1; // Weg
	JS.gpxmap.parameters.tfaktor = (typeof(Tfaktor)!="undefined") ? Tfaktor : 1; // Temperatur
	JS.gpxmap.parameters.toffset = (typeof(Toffset)!="undefined") ? Toffset : 0; // Temperatur
	JS.gpxmap.parameters.unwraplon = (typeof(Unwraplon)!="undefined") ? Unwraplon : true;
	JS.gpxmap.parameters.trackover = (typeof(Trackover)!="undefined") ? Trackover : true;
	JS.gpxmap.parameters.trackclick = (typeof(Trackclick)!="undefined") ? Trackclick : true;
	JS.gpxmap.parameters.trackmarker = (typeof(Trackmarker)!="undefined") ? Trackmarker : "";
	JS.gpxmap.parameters.routemarker = (typeof(Routemarker)!="undefined") ? Routemarker : "";
	JS.gpxmap.parameters.shwpname = (typeof(Shwpname)!="undefined") ? Shwpname : true;
	JS.gpxmap.parameters.shwptooltip = (typeof(Shwptooltip)!="undefined") ? Shwptooltip : false;
	JS.gpxmap.parameters.shwpcmt = (typeof(Shwpcmt)!="undefined") ? Shwpcmt : true;
	JS.gpxmap.parameters.shwpdesc = (typeof(Shwpdesc)!="undefined") ? Shwpdesc : false;
	JS.gpxmap.parameters.shwptime = (typeof(Shwptime)!="undefined") ? Shwptime : false;
	JS.gpxmap.parameters.shwpshadow = (typeof(Shwpshadow)!="undefined") ? Shwpshadow : true;
	JS.gpxmap.parameters.wpcluster = (typeof(Wpcluster)!="undefined") ? Wpcluster : false;
	JS.gpxmap.parameters.bildpfad = (typeof(Bildpfad)!="undefined") ? Bildpfad : "";
	JS.gpxmap.parameters.gpxpfad = (typeof(Gpxpfad)!="undefined") ? Gpxpfad : ""; 
	JS.gpxmap.parameters.defaulticon = (typeof(Defaulticon)!="undefined") ? Defaulticon : ""; 
	JS.gpxmap.parameters.bildwegpunkticon = (typeof(Bildwegpunkticon)!="undefined") ? Bildwegpunkticon : "Bild"; // Bei "" Icon aus sym-Tag
	JS.gpxmap.parameters.shtrcmt = (typeof(Shtrcmt)!="undefined") ? Shtrcmt : false;
	JS.gpxmap.parameters.shtrdesc = (typeof(Shtrdesc)!="undefined") ? Shtrdesc : false;
	JS.gpxmap.parameters.shtrx = (typeof(Shtrx)!="undefined") ? Shtrx : true;
	JS.gpxmap.parameters.shtrt = (typeof(Shtrt)!="undefined") ? Shtrt : true;
	JS.gpxmap.parameters.shtrtwob = (typeof(Shtrtwob)!="undefined") ? Shtrtwob : false;
	JS.gpxmap.parameters.shtrtabs = (typeof(Shtrtabs)!="undefined") ? Shtrtabs : false;
	JS.gpxmap.parameters.shtrtabs_k = JS.gpxmap.parameters.shtrtabs_p = false;
	if(JS.gpxmap.parameters.shtrtabs==true) JS.gpxmap.parameters.shtrtabs_k = JS.gpxmap.parameters.shtrtabs_p = true;
	if(typeof(JS.gpxmap.parameters.shtrtabs)=="string" && JS.gpxmap.parameters.shtrtabs.indexOf("k")>-1 ) JS.gpxmap.parameters.shtrtabs_k = true;
	if(typeof(JS.gpxmap.parameters.shtrtabs)=="string" && JS.gpxmap.parameters.shtrtabs.indexOf("p")>-1 ) JS.gpxmap.parameters.shtrtabs_p = true;
	JS.gpxmap.parameters.shtrtges = (typeof(Shtrtges)!="undefined") ? Shtrtges : false;
	JS.gpxmap.parameters.shtrtgeswob = (typeof(Shtrtgeswob)!="undefined") ? Shtrtgeswob : false;
	JS.gpxmap.parameters.shtrv = (typeof(Shtrv)!="undefined") ? Shtrv : true;
	JS.gpxmap.parameters.shtrpace = (typeof(Shtrpace)!="undefined") ? Shtrpace : false;
	JS.gpxmap.parameters.shtrh = (typeof(Shtrh)!="undefined") ? Shtrh : true;
	JS.gpxmap.parameters.shtrrr = (typeof(Shtrrr)!="undefined") ? Shtrrr : true;
	JS.gpxmap.parameters.shtrs = (typeof(Shtrs)!="undefined") ? Shtrs : true;
	JS.gpxmap.parameters.shtrhr = (typeof(Shtrhr)!="undefined") ? Shtrhr : true;
	JS.gpxmap.parameters.shtrcad = (typeof(Shtrcad)!="undefined") ? Shtrcad : true;
	JS.gpxmap.parameters.shtratemp = (typeof(Shtratemp)!="undefined") ? Shtratemp : true;
	JS.gpxmap.parameters.shtrvmitt = (typeof(Shtrvmitt)!="undefined") ? Shtrvmitt : false;
	JS.gpxmap.parameters.shtrvmittwob = (typeof(Shtrvmittwob)!="undefined") ? Shtrvmittwob : false;
	JS.gpxmap.parameters.shtrvmittpace = (typeof(Shtrvmittpace)!="undefined") ? Shtrvmittpace : false;
	JS.gpxmap.parameters.shtrvmittpacewob = (typeof(Shtrvmittpacewob)!="undefined") ? Shtrvmittpacewob : false;
	JS.gpxmap.parameters.movevmin = (typeof(Movevmin)!="undefined") ? Movevmin : 1;
	JS.gpxmap.parameters.arrowtrack = (typeof(Arrowtrack)!="undefined") ? Arrowtrack : false;
	JS.gpxmap.parameters.arrowtrackcol = (typeof(Arrowtrackcol)!="undefined") ? Arrowtrackcol : "";
	JS.gpxmap.parameters.shrtcmt = (typeof(Shrtcmt)!="undefined") ? Shrtcmt : false;
	JS.gpxmap.parameters.shrtdesc = (typeof(Shrtdesc)!="undefined") ? Shrtdesc : false;
	JS.gpxmap.parameters.shtrstart = (typeof(Shtrstart)!="undefined") ? Shtrstart : false;
	JS.gpxmap.parameters.shtrziel = (typeof(Shtrziel)!="undefined") ? Shtrziel : false;
	JS.gpxmap.parameters.shrtstart = (typeof(Shrtstart)!="undefined") ? Shrtstart : false;
	JS.gpxmap.parameters.shrtziel = (typeof(Shrtziel)!="undefined") ? Shrtziel : false;
	JS.gpxmap.parameters.arrowroute = (typeof(Arrowroute)!="undefined") ? Arrowroute : false
	JS.gpxmap.parameters.arrowroutecol = (typeof(Arrowroutecol)!="undefined") ? Arrowroutecol : "";
	JS.gpxmap.parameters.arrowsymbol = (typeof(Arrowsymbol)!="undefined") ? Arrowsymbol : "➤"; 
	JS.gpxmap.parameters.groesseminibild	= (typeof(Groesseminibild)!="undefined") ? Groesseminibild : 60; // in Pixel, max. 149
	JS.gpxmap.parameters.displaycolor = (typeof(Displaycolor)!="undefined") ? Displaycolor : false;
	JS.gpxmap.parameters.laengen3d = (typeof(Laengen3d)!="undefined") ? Laengen3d : false;
	JS.gpxmap.parameters.usegpxbounds = (typeof(Usegpxbounds)!="undefined") ? Usegpxbounds : false;
	JS.gpxmap.parameters.hglattlaen = (typeof(Hglattlaen)!="undefined") ? Hglattlaen : 500; // in Meter
	JS.gpxmap.parameters.vglattlaen = (typeof(Vglattlaen)!="undefined") ? Vglattlaen : 100; // in Meter
	JS.gpxmap.parameters.vglatt = (typeof(Vglatt)!="undefined") ? Vglatt : false;
	JS.gpxmap.parameters.hglatt = (typeof(Hglatt)!="undefined") ? Hglatt : false;
	JS.gpxmap.parameters.tdiff = (typeof(Tdiff)!="undefined") ? Tdiff : 0; // in Stunden
	JS.gpxmap.parameters.tkorr = (typeof(Tkorr)!="undefined") ? Tkorr : true;
	JS.gpxmap.parameters.maxzoomemove = (typeof(Maxzoomemove)!="undefined") ? Maxzoomemove : 30; // 1 ... , 30: aus
	JS.gpxmap.parameters.plotframecol = (typeof(Plotframecol)!="undefined") ? Plotframecol : "black";
	JS.gpxmap.parameters.plotgridcol = (typeof(Plotgridcol)!="undefined") ? Plotgridcol : "gray";
	JS.gpxmap.parameters.plotlabelcol = (typeof(Plotlabelcol)!="undefined") ? Plotlabelcol : "black";
	JS.gpxmap.parameters.plotmarkercol = (typeof(Plotmarkercol)!="undefined") ? Plotmarkercol : "black";
	JS.gpxmap.parameters.profilfillopac = (typeof(Profilfillopac)!="undefined") ? Profilfillopac : 0; //   0 ... 1, 0:aus
	JS.gpxmap.parameters.trcolmod = (typeof(Trcolmod)!="undefined") ? Trcolmod : ""; // h s v hr cad
	JS.gpxmap.parameters.tcols = (typeof(Tcols)!="undefined") ? Tcols : ["#ff0000","#00ff00","#0000ff","#eeee00","#ff00ff","#00ffff","#000000"]; // Trackfarben in #rrggbb für rot grün blau
	JS.gpxmap.parameters.rcols = (typeof(Rcols)!="undefined") ? Rcols : ["#800000","#008000","#000080","#808000","#800080","#008080","#808080"]; // Routenfarben
	JS.gpxmap.parameters.ocol = (typeof(Ocol)!="undefined") ? Ocol : "#000000";   // Track- und Routenfarbe bei Mouseover
	JS.gpxmap.parameters.owidth = (typeof(Owidth)!="undefined") ? Owidth : 3.0;  // Linienstärke Track und Route bei Mouseover
	JS.gpxmap.parameters.twidth = (typeof(Twidth)!="undefined") ? Twidth : 2.0;  // Linienstärke Track
	JS.gpxmap.parameters.rwidth = (typeof(Rwidth)!="undefined") ? Rwidth : 2.0;  // Linienstärke Route
	JS.gpxmap.parameters.topac = (typeof(Topac)!="undefined") ? Topac : 0.8;   // Transparenz Trackfarbe
	JS.gpxmap.parameters.ropac = (typeof(Ropac)!="undefined") ? Ropac : 0.8;   // Transparenz Routenfarbe
	JS.gpxmap.parameters.linktarget = (typeof(Linktarget)!="undefined") ? Linktarget : "";
	JS.gpxmap.parameters.popup_Pars = (typeof(Popup_Pars)!="undefined") ? Popup_Pars : "width=900,height=790,screenX=970,screenY=0,status=yes,scrollbars=yes";
	
	if(JS.gpxmap.parameters.tracks_dateiuebergreifend_verbinden) JS.gpxmap.parameters.tracks_verbinden = true;
	if(typeof(JS.gpxmap.parameters.tcols)=="string") JS.gpxmap.parameters.tcols = JS.gpxmap.parameters.tcols.split(",");
	if(typeof(JS.gpxmap.parameters.rcols)=="string") JS.gpxmap.parameters.rcols = JS.gpxmap.parameters.rcols.split(",");

	if(JS.debuginfo) {
		var t = "";
		for(var o in JS.gpxmap.parameters) t += "<br>&nbsp;&nbsp;" + o + ": " + JS.gpxmap.parameters[o];
		JS.Debug_Info("Start","Globale Steuervariablen: "+t+"<br>",false);
	}
}

JS.gpxmap.units = {};
JS.gpxmap.units.si =  {
	way: "km",
	speed: "km/h",
	alt: "m",
	pace: "min/km",
	temp: "°C"
};
JS.gpxmap.units.enus = JS.gpxmap.units.us = JS.gpxmap.units.en =  {
	way: "miles",
	speed: "mph",
	alt: "ft",
	pace: "min/mile",
	temp: "°C"
};
JS.gpxmap.units.us.temp = "°F";
JS.gpxmap.units.airwater = JS.gpxmap.units.water =  {
	way: "sm",
	speed: "kn",
	alt: "ft",
	pace: "min/sm",
	temp: "°C"
};
JS.gpxmap.units.air =  {
	way: "NM",
	speed: "kn",
	alt: "ft",
	pace: "min/NM",
	temp: "°C"
};

JS.gpxmap.strings = {};
JS.gpxmap.strings.de = {
	lenght: "Length",
	way: "Dist.       ",
	duration: "Dur",
	tstart: "Start    ",
	time: "Clock",
	time_unit: "h",
	altdiff: "Gain     ",
	alt: "h",
	in: " in ",
	grade: "Slope   ",
	grade_unit: "%",
	avspeed: "V<sub>m</sub>",
	speed2: "Speed",
	speed: "V",
	pace: "Pace",
	hr2: "Pulse",
	hr: "HF",
	hr_unit: "1/min",
	cad: "Kadenz",  
	cad_unit: "UpM",
	temp: "Temp",
	wpt: "Waypnt",
	wpts: "Waypts",
	pwpt: "PicWaypnt",
	trk: "Inf",
	trks: "Trks",
	rte: "R",
	rtes: "Rs",
	inmo: "moving",
	// wait: "Wait.<br />Data loading.",
	wait: "",  // Wartebild nehmen
	clkz: "Click to zoom",
	zb: "Zoom back",
	frage_datenschutz_gm: "Google_Api OK?",
	antwort_datenschutz_gm: "Google API denied",
	frage_datenschutz_osm: "OSM-Maps OK?",
	antwort_datenschutz_osm: "OSM denied",
	fullScreen: "Full Screen",
	normalSize: "Normal Size",
	showCurrentLocation: "Show act.Pos.",
	hideCurrentLocation: "Hide act.Pos.",
	showTrafficLayer: "Show traffic",
	hideTrafficLayer: "Hide traffic",
	noMap: "No Map",
	file: "Data",
	showhide: "",
	zoom: "",
	all: "All",
	showlist: ""
}
JS.gpxmap.strings.en = {
	lenght: "Length",
	way: "Way",
	duration: "Duration",
	tstart: "Start time",
	time: "Time",
	time_unit: "hours",
	altdiff: "Elevation difference",
	alt: "Elevation", //"Altitude",
	//alt_unit: "m",
	in: " in ",
	grade: "Slope",
	grade_unit: "%",
	avspeed: "V<sub>m</sub>",
	speed2: "Speed",
	speed: "V",
	pace: "Pace",
	hr2: "Heart rate",
	hr: "HR",
	hr_unit: "1/min",
	cad: "Cadence", 
	cad_unit: "rpm",
	temp: "Temperature",
	wpt: "Waypoint",
	wpts: "Waypoints",
	pwpt: "Picture Waypoint",
	trk: "Track",
	trks: "Tracks",
	rte: "Route",
	rtes: "Routes",
	inmo: "in motion",
	// wait: "Please wait.<br />Loading data.",
	wait: "",  // Wartebild nehmen
	clkz: "Click to zoom",
	zb: "Zoom back",
	frage_datenschutz_gm: "Google API OK?",
	antwort_datenschutz_gm: "Google API denied",
	frage_datenschutz_osm: "OSM maps OK?",
	antwort_datenschutz_osm: "OSM maps denied.",
	fullScreen: "Full Screen",
	normalSize: "Normal Size",
	showCurrentLocation: "Show current location",
	hideCurrentLocation: "Hide current location",
	showTrafficLayer: "Show traffic",
	hideTrafficLayer: "Hide traffic",
	noMap: "No Map",
	file: "File",
	showhide: "show/hide",
	zoom: "zoom to element",
	all: "All",
	showlist: "show list, use the arrow keys to navigate in the list"
}
/* // Autoscale in den Profilen abschalten
JS.Scaling = {   // nur paarweise verwenden
	hmin:0,hmax:1000,  // Hoehenplot
	smin:-30,smax:30,  // Steigungsplot
	vmin:0,vmax:100,   // Geschwindigkeitsplot
	hrmin:50,hrmax:200,   // Herzfrequenz
	cadmin:0,cadmax:150,   // Trittfrequenz
	atempmin:-30,atempmax:50,   // Temperatur
	hardscaling:false   // Skalierwerte bindend (true) oder Minwerte(false)
}; */
// gpxmap_add2.js
