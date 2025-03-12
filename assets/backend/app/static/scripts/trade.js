document.addEventListener("DOMContentLoaded", function () {
    const priceElement = document.getElementById("live-price");
    const buyOrders = document.getElementById("buy-orders");
    const sellOrders = document.getElementById("sell-orders");

    async function fetchMarketData() {
        try {
            const response = await fetch("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usdt");
            const data = await response.json();
            priceElement.textContent = `$${data.bitcoin.usdt}`;
        } catch (error) {
            console.error("Error fetching market data", error);
        }
    }
    
    async function fetchOrderBook() {
        try {
            const response = await fetch("https://api.binance.com/api/v3/depth?symbol=BTCUSDT&limit=10");
            const data = await response.json();
            buyOrders.innerHTML = data.bids.map(order => `<p style='color:green;'>${order[0]} USDT - ${order[1]} BTC</p>`).join("");
            sellOrders.innerHTML = data.asks.map(order => `<p style='color:red;'>${order[0]} USDT - ${order[1]} BTC</p>`).join("");
        } catch (error) {
            console.error("Error fetching order book", error);
        }
    }
    
    function placeOrder(type) {
        alert(`${type.toUpperCase()} order placed!`);
    }
    
    fetchMarketData();
    fetchOrderBook();
    setInterval(fetchMarketData, 5000);
    setInterval(fetchOrderBook, 5000);
});
