// Wallet page functionality

document.addEventListener('DOMContentLoaded', function() {
    // Copy wallet address to clipboard
    const copyAddressBtn = document.querySelector('.input-group .btn-outline-light');
    if (copyAddressBtn) {
        copyAddressBtn.addEventListener('click', function() {
            const addressInput = document.querySelector('.input-group input[readonly]');
            navigator.clipboard.writeText(addressInput.value)
                .then(() => {
                    // Change button text temporarily
                    const originalText = copyAddressBtn.textContent;
                    copyAddressBtn.textContent = 'Copied!';
                    setTimeout(() => {
                        copyAddressBtn.textContent = originalText;
                    }, 2000);
                })
                .catch(err => {
                    console.error('Failed to copy: ', err);
                });
        });
    }

    // Handle cryptocurrency selection in deposit modal
    const cryptoSelect = document.getElementById('cryptoSelect');
    if (cryptoSelect) {
        cryptoSelect.addEventListener('change', function() {
            const selectedCrypto = this.value;
            let walletAddress = '';
            let qrData = '';
            
            // Set dummy addresses based on selected crypto
            switch(selectedCrypto) {
                case 'Bitcoin (BTC)':
                    walletAddress = 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh';
                    break;
                case 'Ethereum (ETH)':
                    walletAddress = '0x71C7656EC7ab88b098defB751B7401B5f6d8976F';
                    break;
                case 'Tether (USDT)':
                    walletAddress = 'TEZzaVUBmMGEPRjwHQYgXWXoYhFiN35Lm2';
                    break;
                case 'Cardano (ADA)':
                    walletAddress = 'addr1qxzj5lq7lwsjmmku6q5adkj7xnu3u84ty3zz8lm6s55q6r0p6kd0xck3pp3xn4twggtsfvllvjh2e3t9rf5mwqn4qygsxrf7t8';
                    break;
                case 'Solana (SOL)':
                    walletAddress = '5FHwkrdxD5AKmrgvnRoAYd5LLpuqBJF2tQz6xTijPpo3';
                    break;
            }
            
            // Update UI
            const addressInput = document.querySelector('.input-group input[readonly]');
            if (addressInput) {
                addressInput.value = walletAddress;
            }
            
            // Update QR code
            const qrImage = document.querySelector('.modal-body .mt-3 img');
            if (qrImage) {
                qrImage.src = `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${walletAddress}`;
            }
            
            // Update alert message
            const alertMsg = document.querySelector('.modal-body .alert');
            if (alertMsg) {
                const cryptoName = selectedCrypto.split(' ')[0];
                const cryptoTicker = selectedCrypto.match(/\((.*?)\)/)[1];
                alertMsg.innerHTML = `<i class="fas fa-info-circle me-2"></i> Only send ${cryptoName} (${cryptoTicker}) to this address. Sending any other cryptocurrency may result in permanent loss.`;
            }
        });
    }

    // Handle withdraw amount calculation
    const withdrawAmount = document.getElementById('withdrawAmount');
    const withdrawCrypto = document.getElementById('withdrawCrypto');
    if (withdrawAmount && withdrawCrypto) {
        const updateFeeAndReceive = function() {
            const amount = parseFloat(withdrawAmount.value) || 0;
            let fee = 0;
            let receiveAmount = 0;
            
            // Calculate fee based on selected crypto (dummy values)
            switch(withdrawCrypto.value) {
                case 'Bitcoin (BTC)':
                    fee = 0.0005;
                    break;
                case 'Ethereum (ETH)':
                    fee = 0.003;
                    break;
                case 'Tether (USDT)':
                    fee = 5;
                    break;
            }
            
            // Calculate receive amount
            receiveAmount = Math.max(0, amount - fee);
            
            // Update UI
            const feeInput = document.querySelector('.modal-body input[value*="BTC"]:read-only');
            if (feeInput) {
                const ticker = withdrawCrypto.value.match(/\((.*?)\)/)[1];
                feeInput.value = `${fee} ${ticker}`;
            }
            
            const receiveInput = document.querySelector('.modal-body input[value="0.00 BTC"]:read-only');
            if (receiveInput) {
                const ticker = withdrawCrypto.value.match(/\((.*?)\)/)[1];
                receiveInput.value = `${receiveAmount.toFixed(6)} ${ticker}`;
            }
        };
        
        withdrawAmount.addEventListener('input', updateFeeAndReceive);
        withdrawCrypto.addEventListener('change', function() {
            // Update available balance text
            const availableText = document.querySelector('.modal-body small.text-muted');
            if (availableText) {
                let availableAmount = '';
                const ticker = this.value.match(/\((.*?)\)/)[1];
                
                switch(this.value) {
                    case 'Bitcoin (BTC)':
                        availableAmount = '0.856';
                        break;
                    case 'Ethereum (ETH)':
                        availableAmount = '4.235';
                        break;
                    case 'Tether (USDT)':
                        availableAmount = '870.50';
                        break;
                }
                
                availableText.textContent = `Available: ${availableAmount} ${ticker}`;
            }
            
            // Update input group text
            const inputGroupText = document.querySelector('.input-group-text');
            if (inputGroupText) {
                const ticker = this.value.match(/\((.*?)\)/)[1];
                inputGroupText.textContent = ticker;
            }
            
            updateFeeAndReceive();
        });
        
        // Max button functionality
        const maxButton = document.querySelector('.btn-sm.btn-link');
        if (maxButton) {
            maxButton.addEventListener('click', function() {
                let maxAmount = 0;
                
                switch(withdrawCrypto.value) {
                    case 'Bitcoin (BTC)':
                        maxAmount = 0.856;
                        break;
                    case 'Ethereum (ETH)':
                        maxAmount = 4.235;
                        break;
                    case 'Tether (USDT)':
                        maxAmount = 870.50;
                        break;
                }
                
                withdrawAmount.value = maxAmount;
                updateFeeAndReceive();
            });
        }
    }
}); 