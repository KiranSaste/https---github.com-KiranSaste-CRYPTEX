document.addEventListener("DOMContentLoaded", function () {
    const marketDataTable = document.getElementById("market-data");
    const searchBar = document.getElementById("search-bar");

    async function fetchMarketData() {
        try {
            const response = await fetch("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false");
            const data = await response.json();

            marketDataTable.innerHTML = "";
            data.forEach((coin, index) => {
                const row = `
                    <tr>
                        <td>${index + 1}</td>
                        <td><img src="${coin.image}" width="20"> ${coin.name} (${coin.symbol.toUpperCase()})</td>
                        <td>$${coin.current_price.toFixed(2)}</td>
                        <td class="${coin.price_change_percentage_24h >= 0 ? 'green' : 'red'}">${coin.price_change_percentage_24h.toFixed(2)}%</td>
                        <td>$${coin.market_cap.toLocaleString()}</td>
                        <td><button class="trade-btn" onclick="window.location.href='trade.html'">Trade</button></td>
                    </tr>
                `;
                marketDataTable.innerHTML += row;
            });

        } catch (error) {
            console.error("Error fetching market data:", error);
        }
    }

    searchBar.addEventListener("input", function () {
        const query = searchBar.value.toLowerCase();
        document.querySelectorAll("#market-data tr").forEach(row => {
            row.style.display = row.textContent.toLowerCase().includes(query) ? "" : "none";
        });
    });

    fetchMarketData();
    setInterval(fetchMarketData, 6000);
});
