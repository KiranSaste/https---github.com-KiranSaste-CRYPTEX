'use strict';


// add event on element

const addEventOnElem = function (elem, type, callback) {
    if (elem.length > 1) {
        for (let i = 0; i < elem.length; i++) {
            elem[i].addEventListener(type, callback);

        }
    } else {
        elem.addEventListener(type, callback);
    }
}




// navbar toggle

const navbar = document.querySelector("[data-navbar]");
const navbarLinks = document.querySelectorAll("[data-nav-link]");
const navToggler = document.querySelector("[data-nav-toggler]");

const toggleNavbar = function () {
    navbar.classList.toggle("active");
    navToggler.classList.toggle("active");
    document.body.classList.toggle("active");
}

addEventOnElem(navToggler, "click", toggleNavbar);


// 12/02/2025  26:37 work done upto navbar 

// strat 13/02/2025 morning

const closeNavbar = function () {
    navbar.classList.remove("active");
    navToggler.classList.remove("active");
    document.body.classList.remove("active");
}

addEventOnElem(navbarLinks, "click", closeNavbar);



// header active video code
/** 
 const header = document.querySelector("[data-header]");

 
const activeHeader = function () {
    if (window.scrollY > 300){
        header.classList.add("active");

    }else {
        header.classList.remove("active");
    }    
}

addEventOnElem( window, "scroll", activeHeader);

activeHeader();
*/
// =============================================================================

// header active copilot code
const header = document.querySelector("[data-header]");

const activeHeader = () => {
    console.log("Scroll event detected"); // Debugging log
    if (window.scrollY > 300) {
        header.classList.add("active");
        console.log("Header activated"); // Debugging log
    } else {
        header.classList.remove("active");
        console.log("Header deactivated"); // Debugging log
    }
}

addEventOnElem(window, "scroll", activeHeader);

// Initial check in case the page is already scrolled
activeHeader();

/*
**toggle active on add to fav 
*/

const addToFavBtns = document.querySelectorAll("[data-add-to-fav]");

const toggleActive = function () {

    this.classList.toggle("active");
    /** OR
     * for (let i = 0; i < adToFavBtns.length; i++){
         adToFavBtns[i].classList.toggle("active");
     } */
}

addEventOnElem(addToFavBtns, "click", toggleActive);


/**
 * scroll revereal effect
 */

const sections = document.querySelectorAll("[data-section]");

const scrollReveal = function () {
    for (let i = 0; i < sections.length; i++) {
        if (sections[i].getBoundingClientRect().top < window.innerHeight / 1.5) {
            sections[i].classList.add("active");
        } else {
            sections[i].classList.remove("active");
        }

    }
}
scrollReveal();

addEventOnElem(window, "scroll", scrollReveal);

// Settingup API for real time  trend card 

// document.addEventListener("DOMContentLoaded", function () {
//     function fetchCryptoPrices() {
//         fetch("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether,bnb&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true")
//             .then(response => response.json())
//             .then(data => {
//                 const coinLinks = {
//                     bitcoin: "https://www.binance.us/buy-sell-crypto",
//                     ethereum: "https://www.binance.us/buy-sell-crypto",
//                     tether: "https://www.binance.us/buy-sell-crypto",
//                     bnb: "https://www.binance.us/buy-sell-crypto"
//                 };

//                 document.getElementById("bitcoinvalue").innerHTML = `<a href="${coinLinks.bitcoin}" target="_blank">$${data.bitcoin.usd.toFixed(2)}</a>`;
//                 document.getElementById("ethereumvalue").innerHTML = `<a href="${coinLinks.ethereum}" target="_blank">$${data.ethereum.usd.toFixed(2)}</a>`;
//                 document.getElementById("tethervalue").innerHTML = `<a href="${coinLinks.tether}" target="_blank">$${data.tether.usd.toFixed(2)}</a>`;
//                 document.getElementById("bnbvalue").innerHTML = `<a href="${coinLinks.bnb}" target="_blank">$${data.bnb.usd.toFixed(2)}</a>`;


//                 // $.ajax({
//                 //         success: function (data) {
//                 //             $("#bitcoinvalue").text("$" + data.bitcoin.usd.toFixed(2));
//                 //             $("#ethereumvalue").text("$" + data.ethereum.usd.toFixed(2));
//                 //             $("#tethervalue").text("$" + data.tether.usd.toFixed(2));
//                 //             $("#bnbvalue").text("$" + data.bnb.usd.toFixed(2));
//                 //         }
//                 //     })
                            
//                 // Updating price change percentage (24h)
//                 document.getElementById("bitcoinchange").textContent = `${"USD" + data.bitcoin.usd_24h_change.toFixed(2)}%`;
//                 document.getElementById("ethereumchange").textContent = `${"USD" + data.ethereum.usd_24h_change.toFixed(2)}%`;
//                 document.getElementById("tetherchange").textContent = `${"USD" + data.tether.usd_24h_change.toFixed(2)}%`;
//                 document.getElementById("bnbchange").textContent = `${"USD" + data.bnb.usd_24h_change.toFixed(2)}%`;

//                 // Apply color based on price change
//                 ["bitcoin", "ethereum", "tether", "bnb"].forEach(coin => {
//                     let changeElement = document.getElementById(`${coin}change`);
//                     let changeValue = parseFloat(changeElement.textContent);
//                     changeElement.classList.remove("badge-red", "badge-green");
//                     changeElement.classList.add(changeValue >= 0 ? "badge-green" : "badge-red");
//                 });
//             })
//             .catch(error => {
//                 console.error("Error fetching prices:", error);
//             });
//     }

//     fetchCryptoPrices();
//     setInterval(fetchCryptoPrices, 6000); // Update every 6 seconds
// });





$(document).ready(function () {
    function fetchCryptoPrices() {
        $.ajax({
            url: "https://api.coingecko.com/api/v3/simple/price",
            method: "GET",
            data: {
                ids: "bitcoin,ethereum,tether,bnb,solana,xrp,cardano,avalanche",
                vs_currencies: "usd",
                include_market_cap: true,
                include_24hr_vol: true,
                include_24hr_change: true
            },
            success: function (data) {
                $("#bitcoinvalue").text("$" + data.bitcoin.usd.toFixed(2));
                $("#ethereumvalue").text("$" + data.ethereum.usd.toFixed(2));
                $("#tethervalue").text("$" + data.tether.usd.toFixed(2));
                $("#bnbvalue").text("$" + data.bnb.usd.toFixed(2));
            },
            error: function (error) {
                console.error("Error fetching prices:", error);
            }
        });
    }

    fetchCryptoPrices();
    setInterval(fetchCryptoPrices, 6000); // Update every 6 seconds
});




//  Fetch live prices for table content


document.addEventListener("DOMContentLoaded", function () {
    function fetchMarketData() {
        fetch('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,tether,bnb,solana,xrp,cardano,avalanche&order=market_cap_desc&per_page=10&page=1&sparkline=false&price_change_percentage=24h')
            .then(response => response.json())
            .then(data => {
            const coinLinks = {
                bitcoin: "https://www.binance.us/buy-sell-crypto/btc",
                ethereum: "https://www.binance.us/buy-sell-crypto/eth",
                tether: "https://www.binance.us/buy-sell-crypto/usdt",
                bnb: "https://www.binance.us/buy-sell-crypto/bnb",
                solana: "https://www.binance.us/buy-sell-crypto/sol",
                cardano: "https://www.binance.us/buy-sell-crypto/ada"
            };
            
            let tableBody = document.querySelector(".table-body");
            tableBody.innerHTML = ""; // Clear existing table data
            
            data.forEach((coin, index) => {
                let row = `
                <tr class="table-row">
                    <td class="table-data">
                    <button class="add-to-fav" aria-label="Add to favourite" data-add-to-fav>
                        <ion-icon name="star-outline" aria-hidden="true" class="icon-outline"></ion-icon>
                        <ion-icon name="star" aria-hidden="true" class="icon-fill"></ion-icon>
                    </button>
                    </td>
                    <th class="table-data rank" scope="row">${index + 1}</th>
                    <td class="table-data">
                    <div class="wrapper">
                        <img src="${coin.image}" width="20" height="20" alt="${coin.name} logo" class="img">
                        <h3>
                        <a href="${coinLinks[coin.id] || '#'}" class="coin-name">${coin.name} <span class="span">${coin.symbol.toUpperCase()}</span></a>
                        </h3>
                    </div>
                    </td>
                    <td class="table-data last-price">$${coin.current_price ? coin.current_price.toFixed(2) : 'N/A'}</td>
                    <td class="table-data ${coin.price_change_percentage_24h >= 0 ? 'last-update-green' : 'last-update-red'}">
                    ${coin.price_change_percentage_24h ? coin.price_change_percentage_24h.toFixed(2) : 'N/A'}%
                    </td>

                    <td class="table-data market-cap">$${coin.market_cap ? coin.market_cap.toLocaleString() : 'N/A'}</td>

                    <td class="table-data">
                    <img src="../static/images/chart-${index % 2 + 1}.svg" width="100" height="40" alt="chart" class="chart">
                    </td>
                    <td class="table-data">
                    <button class="btn btn-outline">Trade</button>
                    </td>
                </tr>
                `;
                tableBody.innerHTML += row;
            });
            })
            .catch(error => {
            console.error("Error fetching market data:", error);
            });
            
        }

        fetchMarketData();
    setInterval(fetchMarketData, 6000); // Update every 6 seconds
});



/**
 * Fetching combine live data for table and trend card
 */

// document.addEventListener("DOMContentLoaded", function () {
//     function fetchCryptoPrices() {
//         fetch("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether,bnb&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true")
//             .then(response => response.json())
//             .then(data => {
//                 const coinLinks = {
//                     bitcoin: "https://www.binance.us/buy-sell-crypto",
//                     ethereum: "https://www.binance.us/buy-sell-crypto",
//                     tether: "https://www.binance.us/buy-sell-crypto",
//                     bnb: "https://www.binance.us/buy-sell-crypto"
//                 };

//                 ["bitcoin", "ethereum", "tether", "bnb"].forEach(coin => {
//                     if (data[coin]) {
//                         document.getElementById(`${coin}value`).innerHTML = `<a href="${coinLinks[coin]}" target="_blank">$${data[coin].usd.toFixed(2)}</a>`;
//                         document.getElementById(`${coin}change`).textContent = `${data[coin].usd_24h_change.toFixed(2)}%`;

//                         // Apply color based on price change
//                         let changeElement = document.getElementById(`${coin}change`);
//                         let changeValue = parseFloat(changeElement.textContent);
//                         changeElement.classList.remove("badge-red", "badge-green");
//                         changeElement.classList.add(changeValue >= 0 ? "badge-green" : "badge-red");
//                     }
//                 });
//             })
//             .catch(error => console.error("Error fetching prices:", error));
//     }

//     fetchCryptoPrices();
//     setInterval(fetchCryptoPrices, 6000); // Update every 6 seconds
// });

