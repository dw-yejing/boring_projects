# ChromaDB Manager: A Simple GUI for Chroma Based on Chrome Browser Extension

## Introduction

ChromaDB Manager is a Chrome browser extension that provides a data query tool for ChromaDB (a popular vector database). It offers a user-friendly interface that allows direct connection to local ChromaDB instances, viewing collection information, and shard data. This tool is particularly suitable for developers to quickly view and verify data in ChromaDB, enabling basic database operations without writing code.

## Key Features

- Fully open source, source code and Chrome extension package available on [Github](https://github.com/dw-yejing/boring_projects/tree/main/chromadb_chrome_plugin)
- Simple host and port configuration interface
- Support for local ChromaDB instances
- Collection list
- Collection details (vector dimensions, index information, metadata, etc.)
- Document count
- Document query

## Use Cases

1.**Development and Debugging**

- Quickly view data in ChromaDB
- Verify vector data correctness
- Check collection configuration and metadata

2.**Data Validation**

- View document content and embedding vectors
- Check data integrity

3.**Teaching and Demonstration**

- Intuitively display ChromaDB data structure
- Demonstrate basic concepts of vector databases
- Aid in understanding vector retrieval principles

## Usage Instructions

1. Start ChromaDB in Server mode

   ```bash

   chroma run --port 8000 --path /path/chromadb

   ```
2. Install the extension

   - Download chromadb_chrome_plugin locally
   - Open Chrome browser and go to the extensions management page (chrome://extensions/)
   - Enable "Developer mode"
   - Click "Load unpacked extension" and select the downloaded folder
3. Using the extension

   - Click the extension icon to open the interface
   - Enter ChromaDB host (default: localhost) and port (default: 8000)
   - Click "Connect" to establish connection
   - Select a collection to view its details and documents

## Interface Preview

![chroma_query](https://dw-yejing.github.io/images/blogs/chroma_query.png)
