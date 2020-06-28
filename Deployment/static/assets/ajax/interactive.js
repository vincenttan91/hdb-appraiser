var global = 0;

function scrollTo(hash) {
    var anchor = "#" + hash;
    $('html, body').animate({
    scrollTop: $(anchor).offset().top
    }, 1500);
}

function generateDynamicTable(allListings){
    if(allListings.length>0){
        var table = document.createElement("table");
        table.classList.add("table", "table-bordered", "table-dark");
        // table.classList.add("mx-auto");
        // table.style.width = '95%';
        var col = ['Address', 'Floor Area', 'Remaining Lease', 'Price per Sqft', 'Price']; // define an empty array

        var tHead = document.createElement("thead");	
        var hRow = document.createElement("tr");
        
        for (var i = 0; i < col.length; i++) {
                var th = document.createElement("th");
                th.innerHTML = col[i];
                hRow.appendChild(th);
        }
        tHead.appendChild(hRow);
        table.appendChild(tHead);
        
        var tBody = document.createElement("tbody");	
        for (var i = 0; i < allListings.length; i++) {
                var bRow = document.createElement("tr"); // CREATE ROW FOR EACH RECORD .
                for (var j = 0; j < col.length; j++) {
                    var td = document.createElement("td");
                    td.innerHTML = allListings[i][col[j]];
                    bRow.appendChild(td);}
                tBody.appendChild(bRow)}

        table.appendChild(tBody);	
        var divContainer = document.getElementById("listingTable");
        divContainer.innerHTML = "";
        divContainer.appendChild(table);   
    }	
}

function getDetails() {
    var address = $("input#address").val();
    var level = $("input#level").val();
    var area = parseInt($("input#area").val() / 10.7639);
    var lease = $("input#lease").val();
    $this = $("#sendMessageButton");
    $this.prop("disabled", true);
    $.ajax({
        url: `https://hdb-appraiser.herokuapp.com/getDetail?address=${address}&level=${level}&area=${area}&lease=${lease}`,
        timeout: 120000,
        dataType: "json",
        type: "GET",
        cache: false,
        complete: function (data) {
            var response = data['responseJSON'];
            if (response['message']==="invalid address") {
                $("#success").html("<div class='alert alert-danger'>");
                $("#success > .alert-danger").html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;").append("</button>");
                $("#success > .alert-danger").append($("<strong>").text("Sorry, but it seems like the postcode cannot be found."));
                $("#success > .alert-danger").append("</div>");
                $("#contactForm").trigger("reset");
            } else {
                $("#success").html("<div class='alert alert-success'>");
                $("#success > .alert-success").html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;").append("</button>");
                $("#success > .alert-success").append("<strong>Your submission has been received. Please wait while our little elves work on the calculation...</strong>");
                $("#success > .alert-success").append("</div>");

                var price = response['price'];
                var latitude = response['attr']['latitude'];
                var longitude = response['attr']['longitude'];

                document.querySelector(".price").innerText = `Evaluation: SGD ${price}`;
                var hiddenElement = document.getElementsByClassName("hidden");
                if (hiddenElement.length > 0) {
                    hiddenElement[0].classList.remove('hidden');
                }
                if(global==0) { 
                    scrollTo("results");
                }
                getListings(latitude, longitude, price);}

            setTimeout(function () {
                $this.prop("disabled", false);
            }, 1000);
        },
    });
}

function getListings(latitude, longitude, price) {
    $.ajax({
        url: `https://hdb-appraiser.herokuapp.com/getListings?latitude=${latitude}&longitude=${longitude}`,
        timeout: 120000,
        dataType: "json",
        type: "GET",
        cache: false,
        complete: function (data) {
            var response = data['responseJSON'];

            if(global!=0) { 
                global.remove();
            }

            var mymap = L.map('mapid').setView([latitude, longitude], 15);
            var accessToken = "pk.eyJ1IjoiaGRiLWFwcHJhaXNzZXIiLCJhIjoiY2tiajYydzZ5MGx4dDJxcG03bTFta2tpcSJ9.dB07Ewj-FbvqP0NK5NKtmQ"
            L.tileLayer(`https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=${accessToken}`, {
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                maxZoom: 18,
                id: 'mapbox/streets-v11',
                tileSize: 512,
                zoomOffset: -1
            }).addTo(mymap);

            var homeIcon = L.icon({iconUrl:'../static/assets/img/marker.png', iconSize:[60, 65], iconAnchor:[30, 30], popupAnchor:[0, -30]});

            var home = L.marker([latitude, longitude], {icon: homeIcon}).addTo(mymap);
            home.bindPopup("<b>Your property is here!</b><br>Esimated Price: " + `SGD ${price}`).openPopup();

            if (response['response']==="invalid address") {
                alert("Sorry, but there seems to be no listings near the property. Please try again with another postal code.");
                window.location = '/';
            } else {
                var listings = response['nearby'];
                for (var i = 0; i < listings.length; i++) {
                    var loc = listings[i];
                    var marker = L.marker([loc['Latitude'], loc['Longitude']]).addTo(mymap);
                    var popupText = `Address: ${loc['Address']}` + `<br>Remaining Lease: ${loc['Remaining Lease']}` + `<br>Price per Sqft: ${loc['Price per Sqft']}` + `<br>Listing Price: ${loc['Price']}`;
                    marker.bindPopup(popupText);}

                generateDynamicTable(listings);

                window.global = mymap;

                document.getElementsByClassName("navbar-nav")[0].style.display = "flex";
                document.getElementsByClassName("loader")[0].style.display = "none";
                document.getElementsByClassName("loader")[1].style.display = "none";
            }
        }
    });
}

$(function () {
    $("#contactForm input,#contactForm textarea,#contactForm button")
    .jqBootstrapValidation({
        preventSubmit: true,
        submitSuccess: function ($form, event) {
            event.preventDefault();
            getDetails();
        },
        filter: function () {
            return $(this).is(":visible");
        },
    });

    $('a[data-toggle="tab"]').click(function (e) {
        e.preventDefault();
        $(this).tab("show");
    });
});

$("#name").focus(function () {
    $("#success").html("");
});

