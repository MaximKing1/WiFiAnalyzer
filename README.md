# 📡 WiFi Analyzer 📶

WiFi Analyzer is a powerful tool built to analyze and optimize your WiFi channels. Built with Express.js and TypeScript, this tool offers an extensive set of features to help ensure your WiFi remains efficient and secure.

## 🌟 Features

- **WiFi Channel Analysis 📊**: Analyze interference on WiFi channels to identify the best channels for optimal performance.
- **Network Monitoring 👁️**: Keep an eye on the network traffic and detect potential threats.
- **Nearby Network Detection 🔍**: Discover networks in your vicinity.
- **Deauth Packet Detection 🚫**: Protect your network by detecting potential deauth attacks.
- **General Network Insights 🌐**: An overarching analysis function to get a holistic view of your network.

## 🐍 Getting Started with Python

1. **Setup**:
    - Ensure you have Python 3.x installed on your system.
    - Install the required Python packages using pip:
      ```
      pip install Flask scapy
      ```

2. **Running the Server**:
    - Navigate to the directory containing your Python script.
    - Start the server using:
      ```
      python server.py
      ```
    - By default, Flask runs on `http://localhost:5000`, but you can change the port if needed.

3. **Interact with the Python API**:
    - Similar to the TypeScript API, you can use tools like Postman or a frontend application to make requests to the Python server. Given that the endpoints are not yet defined for the Python version, you would need to define them to expose its functionalities.



## 🚀 Getting Started

1. **Setup**:
    - Install the necessary Node.js packages: `npm install`
    - Run the TypeScript build: `tsc`

2. **Running the Server**:
    - Start the server: `node dist/index.js`
    - The server will be running on `http://localhost:3000`

3. **Interact with the API**:
    - Use tools like Postman, or your frontend application to make requests to the server.

## 📌 Endpoints:

- `GET` `/bestChannels`: Get the best channels across all bands.
- `POST` `/addChannel`: Add a new channel for analysis.
- `DELETE` `/removeChannel`: Remove a channel from the list.
- `GET` `/monitorNetworkPackets`: Monitor and capture network packets.
- `GET` `/detectNearbyNetworks`: Detect all networks nearby.
- `GET` `/detectDeauth`: Detect any deauth packets for security.
- `GET` `/generalNetworkAnalysis`: Get a general analysis of the network.

## 💡 Future Improvements:

- Implement actual network packet sniffing for Node.js.
- Integrate with frontend applications for better visualization.

## 🤝 Contribution:

Feel free to fork this repository, and submit your pull requests! Any contributions, no matter how minor, are greatly appreciated. Let's make WiFi analysis better together!

