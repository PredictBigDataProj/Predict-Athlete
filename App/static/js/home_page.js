document.addEventListener("DOMContentLoaded", function () {
  anime({
    targets: "#team-member-left",
    translateX: ["-100%", "0%"],
    opacity: [0, 1],
    easing: "easeOutExpo",
    duration: 1200,
    delay: 300,
  });

  anime({
    targets: "#team-member-right",
    translateX: ["100%", "0%"],
    opacity: [0, 1],
    easing: "easeOutExpo",
    duration: 1200,
    delay: 600,
  });
});

document.addEventListener("DOMContentLoaded", function () {
  var map = L.map("map", {
    center: [20, 0],
    zoom: 2,
    worldCopyJump: true,
  });

  var bounds = [
    [-90, -180],
    [90, 180],
  ];
  map.setMaxBounds(bounds);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "Map data © OpenStreetMap contributors",
  }).addTo(map);

  var leagues = [
    {
      name: "Superliga (DEN 1) [Denmark]",
      country: "Denmark",
      lat: 55.6759,
      lng: 12.5655,
      link: "/league/den1-denmark",
    },
    {
      name: "Pro League (BEL 1) [Belgium]",
      country: "Belgium",
      lat: 50.8503,
      lng: 4.3517,
      link: "/league/bel1-belgium",
    },
    {
      name: "Série A (BRA 1) [Brazil]",
      country: "Brazil",
      lat: -23.5505,
      lng: -46.6333,
      link: "/league/bra1-brazil",
    },
    {
      name: "Eredivisie (NED 1) [Netherlands]",
      country: "Netherlands",
      lat: 52.3676,
      lng: 4.9041,
      link: "/league/ned1-netherlands",
    },
    {
      name: "Premier League (ENG 1) [England]",
      country: "England",
      lat: 51.5,
      lng: -0.1,
      link: "/league/eng1-england",
    },
    {
      name: "Championship (ENG 2) [England]",
      country: "England",
      lat: 52.4862,
      lng: -1.8904,
      link: "/league/eng2-england",
    },
    {
      name: "Ligue 1 (FRA 1) [France]",
      country: "France",
      lat: 48.8566,
      lng: 2.3522,
      link: "/league/fra1-france",
    },
    {
      name: "Ligue 2 (FRA 2) [France]",
      country: "France",
      lat: 45.75,
      lng: 4.85,
      link: "/league/fra2-france",
    },
    {
      name: "Bundesliga (GER 1) [Germany]",
      country: "Germany",
      lat: 52.52,
      lng: 13.405,
      link: "/league/ger1-germany",
    },
    {
      name: "2. Bundesliga (GER 2) [Germany]",
      country: "Germany",
      lat: 50.1109,
      lng: 8.6821,
      link: "/league/ger2-germany",
    },
    {
      name: "Serie A (ITA 1) [Italy]",
      country: "Italy",
      lat: 41.9028,
      lng: 12.4964,
      link: "/league/ita1-italy",
    },
    {
      name: "Serie B (ITA 2) [Italy]",
      country: "Italy",
      lat: 45.4642,
      lng: 9.19,
      link: "/league/ita2-italy",
    },
    {
      name: "Major League Soccer (MLS 1) [USA]",
      country: "USA",
      lat: 40.7128,
      lng: -74.006,
      link: "/league/mls1-usa",
    },
    {
      name: "La Liga (ESP 1) [Spain]",
      country: "Spain",
      lat: 40.4168,
      lng: -3.7038,
      link: "/league/esp1-spain",
    },
    {
      name: "La Liga 2 (ESP 2) [Spain]",
      country: "Spain",
      lat: 39.4699,
      lng: -0.3763,
      link: "/league/esp2-spain",
    },
    {
      name: "Allsvenskan (SWE 1) [Sweden]",
      country: "Sweden",
      lat: 59.3293,
      lng: 18.0686,
      link: "/league/swe1-sweden",
    },
    {
      name: "Super League (GRE 1) [Greece]",
      country: "Greece",
      lat: 37.9838,
      lng: 23.7275,
      link: "/league/gre1-greece",
    },
    {
      name: "Ekstraklasa (POL 1) [Poland]",
      country: "Poland",
      lat: 52.2297,
      lng: 21.0122,
      link: "/league/pol1-poland",
    },
    {
      name: "K League 1 (KOR 1) [South Korea]",
      country: "South Korea",
      lat: 37.5665,
      lng: 126.978,
      link: "/league/kor1-southkorea",
    },
    {
      name: "Super League (CSL 1) [China]",
      country: "China",
      lat: 39.9042,
      lng: 116.4074,
      link: "/league/csl1-china",
    },
    {
      name: "Primeira Liga (POR 1) [Portugal]",
      country: "Portugal",
      lat: 38.7169,
      lng: -9.1399,
      link: "/league/por1-portugal",
    },
    {
      name: "Super League (ISL 1) [India]",
      country: "India",
      lat: 28.6139,
      lng: 77.209,
      link: "/league/isl1-india",
    },
    {
      name: "Pro League (SAU 1) [Saudi Arabia]",
      country: "Saudi Arabia",
      lat: 24.7136,
      lng: 46.6753,
      link: "/league/sau1-saudiarabia",
    },
    {
      name: "A-League Men (AUS 1) [Australia]",
      country: "Australia",
      lat: -33.8688,
      lng: 151.2093,
      link: "/league/aus1-australia",
    },
    {
      name: "Liga Profesional de Fútbol (ARG 1) [Argentina]",
      country: "Argentina",
      lat: -34.6037,
      lng: -58.3816,
      link: "/league/arg1-argentina",
    },
    {
      name: "Liga Pro (ECU 1) [Ecuador]",
      country: "Ecuador",
      lat: -0.1807,
      lng: -78.4678,
      link: "/league/ecu1-ecuador",
    },
    {
      name: "Primera División (PAR 1) [Paraguay]",
      country: "Paraguay",
      lat: -25.2637,
      lng: -57.5759,
      link: "/league/par1-paraguay",
    },
    {
      name: "Primera División (URY 1) [Uruguay]",
      country: "Uruguay",
      lat: -34.9011,
      lng: -56.1645,
      link: "/league/ury1-uruguay",
    },
    {
      name: "Pro League (UAE 1) [UAE]",
      country: "UAE",
      lat: 25.276987,
      lng: 55.296249,
      link: "/league/uae1-uae",
    },
    {
      name: "Primera Division (VEN 1) [Venezuela]",
      country: "Venezuela",
      lat: 10.4806,
      lng: -66.9036,
      link: "/league/ven1-venezuela",
    },
    {
      name: "Primera Division (PER 1) [Peru]",
      country: "Peru",
      lat: -12.0464,
      lng: -77.0428,
      link: "/league/per1-peru",
    },
    {
      name: "3. Liga (GER 3) [Germany]",
      country: "Germany",
      lat: 51.1657,
      lng: 10.4515,
      link: "/league/ger3-germany",
    },
    {
      name: "Hrvatska nogometna liga (CRO 1) [Croatia]",
      country: "Croatia",
      lat: 45.1,
      lng: 15.2,
      link: "/league/cro1-croatia",
    },
    {
      name: "1. Division (CYP 1) [Cyprus]",
      country: "Cyprus",
      lat: 35.1264,
      lng: 33.4299,
      link: "/league/cyp1-cyprus",
    },
    {
      name: "Veikkausliiga (FIN 1) [Finland]",
      country: "Finland",
      lat: 60.1699,
      lng: 24.9384,
      link: "/league/fin1-finland",
    },
    {
      name: "Liga I (ROM 1) [Romania]",
      country: "Romania",
      lat: 44.4268,
      lng: 26.1025,
      link: "/league/rom1-romania",
    },
    {
      name: "Premier League (UKR 1) [Ukraine]",
      country: "Ukraine",
      lat: 50.4501,
      lng: 30.5236,
      link: "/league/ukr1-ukraine",
    },
    {
      name: "Primera Division (CHI 1) [Chile]",
      country: "Chile",
      lat: -33.4489,
      lng: -70.6693,
      link: "/league/chi1-chile",
    },
    {
      name: "Categoría Primera A (COL 1) [Colombia]",
      country: "Colombia",
      lat: 4.711,
      lng: -74.0721,
      link: "/league/col1-colombia",
    },
    {
      name: "Primera División (BOL 1) [Bolivia]",
      country: "Bolivia",
      lat: -16.5,
      lng: -68.1193,
      link: "/league/bol1-bolivia",
    },
    {
      name: "First League (CZE 1) [Czech Republic]",
      country: "Czech Republic",
      lat: 49.8175,
      lng: 15.472,
      link: "/league/cze1-czechrepublic",
    },
    {
      name: "Super League (SWI 1) [Switzerland]",
      country: "Switzerland",
      lat: 46.8182,
      lng: 8.2275,
      link: "/league/swi1-switzerland",
    },
    {
      name: "Süper Lig (TUR 1) [Turkey]",
      country: "Turkey",
      lat: 38.9637,
      lng: 35.2433,
      link: "/league/tur1-turkey",
    },
    {
      name: "Bundesliga (AU 1) [Austria]",
      country: "Austria",
      lat: 47.5162,
      lng: 14.5501,
      link: "/league/au1-austria",
    },
    {
      name: "Nemzeti Bajnokság I (HUN 1) [Hungary]",
      country: "Hungary",
      lat: 47.1625,
      lng: 19.5033,
      link: "/league/hun1-hungary",
    },
    {
      name: "Premier Division (IRL 1) [Ireland]",
      country: "Ireland",
      lat: 53.4129,
      lng: -8.2439,
      link: "/league/irl1-ireland",
    },
    {
      name: "Eliteserien (NOR 1) [Norway]",
      country: "Norway",
      lat: 60.472,
      lng: 8.4689,
      link: "/league/nor1-norway",
    },
    {
      name: "Premiership (SP 1) [Scotland]",
      country: "Scotland",
      lat: 56.4907,
      lng: -4.2026,
      link: "/league/sp1-scotland",
    },
    {
      name: "League One (ENG 3) [England]",
      country: "England",
      lat: 51.5074,
      lng: -0.1278,
      link: "/league/eng3-england",
    },
    {
      name: "League Two (ENG 4) [England]",
      country: "England",
      lat: 51.5074,
      lng: -0.1278,
      link: "/league/eng4-england",
    },
  ];

  var countries = {};

  leagues.forEach(function (league) {
    if (!countries[league.country]) {
      countries[league.country] = [];
    }
    countries[league.country].push(league);
  });

  for (var country in countries) {
    var countryLeagues = countries[country];

    var lat = countryLeagues[0].lat;
    var lng = countryLeagues[0].lng;

    var linksHtml = countryLeagues
      .map(function (league) {
        return `<a href="${league.link}">${league.name}</a><br>`;
      })
      .join("");

    L.marker([lat, lng]).addTo(map).bindPopup(`<strong>${country}</strong>
                  <br>${linksHtml}`);
  }
});

function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
  document.getElementById("main-content").style.marginLeft = "250px";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  document.getElementById("main-content").style.marginLeft = "0";
}

document.addEventListener("DOMContentLoaded", function () {
  setTimeout(function () {
    let flashMessages = document.querySelectorAll(".flash-message");
    flashMessages.forEach(function (msg) {
      msg.style.opacity = "0";
      setTimeout(() => (msg.style.display = "none"), 500);
    });
  }, 3000);
});
