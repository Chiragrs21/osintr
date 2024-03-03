const fetch = require('node-fetch');

async function submitUrlForScan(url, apiKey) {
    const headers = {
        'Content-Type': 'application/json',
        'API-Key': apiKey
    };
    const payload = {
        url: url,
        visibility: 'public',
        tags: ['example']
    };
    const response = await fetch('https://urlscan.io/api/v1/scan/', {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(payload)
    });
    const data = await response.json();
    return data;
}

async function getScanResults(scanId, apiKey) {
    const headers = {
        'API-Key': apiKey
    };
    const url = `https://urlscan.io/api/v1/result/${scanId}/`;
    const response = await fetch(url, {
        headers: headers
    });
    const data = await response.json();
    if (data.status === 'completed') {
        return data;
    } else {
        console.log('Scan still in progress. Waiting 5 seconds before checking again...');
        await new Promise(resolve => setTimeout(resolve, 5000));
        return getScanResults(scanId, apiKey); // Recursive call
    }
}

// Example usage
const apiKey = '21ed5f8c-bd50-42ea-8b0e-6d5eb22fd36a';
const url = 'https://example.com';

(async () => {
    const scanData = await submitUrlForScan(url, apiKey);
    if (scanData) {
        const scanId = scanData.uuid;
        console.log(`Scan submitted successfully. Scan ID: ${scanId}`);
        const scanResults = await getScanResults(scanId, apiKey);
        if (scanResults) {
            console.log(JSON.stringify(scanResults, null, 4));
        }
    }
})();
