const chromaApi = {
    "login": "/api/v2/auth/identity",
    "listCollections": "/api/v2/tenants/default_tenant/databases/default_database/collections",
    "detailsCollection": "/api/v2/tenants/default_tenant/databases/default_database/collections/{collection_name}",
    "countDocuments": "/api/v2/tenants/default_tenant/databases/default_database/collections/{collection_id}/count",
    "listDocuments": "/api/v2/tenants/default_tenant/databases/default_database/collections/{collection_id}/get",
}

document.addEventListener('DOMContentLoaded', function() {
    const connectBtn = document.getElementById('connectBtn');
    const hostInput = document.getElementById('host');
    const portInput = document.getElementById('port');
    const collectionSelect = document.getElementById('collection');
    const resultsDiv = document.getElementById('results');
    const collectionInfoDiv = document.getElementById('collectionInfo');
    
    let isConnected = false;
    let currentHost = '';
    let currentPort = '';

    // Load saved connection settings
    chrome.storage.local.get(['host', 'port', 'isConnected'], function(result) {
        if (result.host) hostInput.value = result.host;
        if (result.port) portInput.value = result.port;
        isConnected = result.isConnected || false;
        if (isConnected) {
            currentHost = result.host;
            currentPort = result.port;
        }
        updateConnectionStatus();
    });

    function updateConnectionStatus() {
        connectBtn.textContent = isConnected ? 'Disconnect' : 'Connect';
        connectBtn.className = isConnected ? 'connected' : '';
        collectionSelect.disabled = !isConnected;
    }

    // Load available collections
    async function loadCollections() {
        try {
            showMessage('Loading collections...', 'info');
            const response = await fetch(`http://${currentHost}:${currentPort}${chromaApi.listCollections}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const data = await response.json();
                collectionSelect.innerHTML = '<option value="" id="">Select a collection...</option>';
                
                if (data && Array.isArray(data)) {
                    // Sort collections alphabetically
                    data.sort((a, b) => a.name.localeCompare(b.name));
                    
                    for (const collection of data) {
                        const option = document.createElement('option');
                        option.value = collection.name;
                        option.id = collection.id;
                        
                        // Get collection details
                        try {
                            const detailsUrl = chromaApi.detailsCollection.replace('{collection_name}', collection.name);
                            const detailsResponse = await fetch(`http://${currentHost}:${currentPort}${detailsUrl}`, {
                                method: 'GET',
                                headers: {
                                    'Content-Type': 'application/json'
                                },
                            });
                            
                            if (detailsResponse.ok) {
                                const details = await detailsResponse.json();
                                const count = details.ids ? details.ids.length : 0;
                                option.textContent = `${collection.name} (${count} items)`;
                            } else {
                                option.textContent = collection.name;
                            }
                        } catch (error) {
                            option.textContent = collection.name;
                        }
                        
                        collectionSelect.appendChild(option);
                    }
                    showMessage('Collections loaded successfully', 'success');
                } else {
                    showMessage('No collections found', 'info');
                }
            } else {
                const errorData = await response.text();
                throw new Error(errorData);
            }
        } catch (error) {
            console.error('Error loading collections:', error);
            showMessage('Error loading collections: ' + error.message, 'error');
        }
    }

    // Connect to ChromaDB
    connectBtn.addEventListener('click', async function() {
        if (isConnected) {
            // Disconnect logic
            isConnected = false;
            currentHost = '';
            currentPort = '';
            chrome.storage.local.set({ isConnected: false });
            collectionSelect.innerHTML = '<option value="">Select a collection...</option>';
            resultsDiv.innerHTML = '';
            collectionInfoDiv.innerHTML = '<p class="info-message">Select a collection to view details</p>';
            updateConnectionStatus();
            showMessage('Disconnected from ChromaDB', 'info');
            return;
        }

        const host = hostInput.value || 'localhost';
        const port = portInput.value || '8021';

        // Save connection settings
        chrome.storage.local.set({
            host: host,
            port: port
        });

        try {
            showMessage('Connecting to ChromaDB...', 'info');
            isConnected = true;
            currentHost = host;
            currentPort = port;
            chrome.storage.local.set({ isConnected: true });
            updateConnectionStatus();
            showMessage('Successfully connected to ChromaDB!', 'success');
            // Load collections after successful connection
            await loadCollections();
        } catch (error) {
            console.error('Connection error:', error);
            showMessage('Error connecting to ChromaDB: ' + error.message, 'error');
        }
    });

    // Handle collection selection
    collectionSelect.addEventListener('change', async function() {
        if (this.value) {
            // Load collection details
            await loadCollectionDetails(this.value);
            // Automatically load items when collection is selected
            await executeQuery();
        } else {
            collectionInfoDiv.innerHTML = '<p class="info-message">Select a collection to view details</p>';
            resultsDiv.innerHTML = '';
        }
    });

    async function loadCollectionDetails(collectionName) {
        try {
            const detailsUrl = chromaApi.detailsCollection.replace('{collection_name}', collectionName);
            const response = await fetch(`http://${currentHost}:${currentPort}${detailsUrl}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const details = await response.json();
                
                // Get document count using countDocuments API
                const countUrl = chromaApi.countDocuments.replace('{collection_id}', details.id);
                const countResponse = await fetch(`http://${currentHost}:${currentPort}${countUrl}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                if (countResponse.ok) {
                    const countData = await countResponse.json();
                    details.documentCount = countData || 0;
                } else {
                    details.documentCount = 0;
                }

                displayCollectionInfo(details);
            } else {
                throw new Error('Failed to load collection details');
            }
        } catch (error) {
            console.error('Error loading collection details:', error);
            collectionInfoDiv.innerHTML = `<p class="message error">Error loading collection details: ${error.message}</p>`;
        }
    }

    function displayCollectionInfo(details) {
        let html = '';
        
        // Collection dimension
        html += `
            <div class="info-item">
                <div class="info-label">Collection Dimension</div>
                <div class="info-value">${details.dimension || 'N/A'}</div>
            </div>
        `;

        // Collection ID
        html += `
            <div class="info-item">
                <div class="info-label">Collection ID</div>
                <div class="info-value">${details.id || 'N/A'}</div>
            </div>
        `;
        // Document count
        html += `
            <div class="info-item">
                <div class="info-label">Document Count</div>
                <div class="info-value">${details.documentCount || 0} documents</div>
            </div>
        `;

        // Collection metadata
        if (details.metadata) {
            html += `
                <div class="info-item">
                    <div class="info-label">Metadata</div>
                    <div class="info-value">
                        <pre>${JSON.stringify(details.metadata, null, 2)}</pre>
                    </div>
                </div>
            `;
        }

        

        collectionInfoDiv.innerHTML = html;
    }

    // Execute query
    async function executeQuery() {
        if (!isConnected) {
            showMessage('Please connect to ChromaDB first', 'error');
            return;
        }

        const collection = collectionSelect.selectedOptions[0];

        if (!collection) {
            showMessage('Please select a collection', 'error');
            return;
        }

        try {
            showMessage('Loading documents...', 'info');
            let endpoint = `http://${currentHost}:${currentPort}${chromaApi.listDocuments.replace('{collection_id}', collection.id)}`;
            let requestBody = {
                "include": [
                    "embeddings", "documents", "metadatas", "distances"
                ],
                "offset": 0,
                "limit": 10
            };

            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody)
            });

            if (response.ok) {
                const data = await response.json();
                displayResults(data);
            } else {
                const errorData = await response.text();
                showMessage(`Query failed: ${errorData}`, 'error');
            }
        } catch (error) {
            showMessage('Error executing query: ' + error.message, 'error');
        }
    }

    function showMessage(message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = message;
        
        resultsDiv.innerHTML = '';
        resultsDiv.appendChild(messageDiv);

        if (type === 'info') {
            setTimeout(() => {
                if (resultsDiv.contains(messageDiv)) {
                    messageDiv.remove();
                }
            }, 3000);
        }
    }

    function displayResults(data) {
        if (!data || !data.ids || data.ids.length === 0) {
            showMessage('No results found', 'info');
            return;
        }

        let html = '<ul class="results-list">';
        for (let i = 0; i < data.ids.length; i++) {
            html += `
                <li class="result-item">
                    <div class="result-header">
                        <span class="result-number">#${i + 1}</span>
                        <span class="result-id">ID: ${data.ids[i]}</span>
                        ${data.distances ? `<span class="result-distance">Distance: ${data.distances[i].toFixed(4)}</span>` : ''}
                    </div>
                    <div class="result-content">
                        ${data.documents ? `<div class="result-document">${data.documents[i]}</div>` : ''}
                        ${data.metadatas ? `<div class="result-metadata"><pre>${JSON.stringify(data.metadatas[i], null, 2)}</pre></div>` : ''}
                    </div>
                </li>
            `;
        }
        html += '</ul>';
        resultsDiv.innerHTML = html;
    }
}); 