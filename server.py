from flask import Flask, request, jsonify
from scapy.all import sniff, Dot11

# Initializing the Flask app and the WiFi analyzer instance.
app = Flask(__name__)
analyzer = WiFiAnalyzer()

class WiFiChannel:
    """Representing a WiFi channel with its band, channel number, and interference."""
    def __init__(self, band, channel, interference):
        self.band = band  # e.g., '2.4GHz', '5GHz', '6GHz'
        self.channel = channel  # Channel number
        self.interference = interference  # Interference level

class WiFiAnalyzer:
    """Class to manage and analyze WiFi channels."""

    def __init__(self):
        # Maintains a list of channels added for analysis.
        self.channels = []

    def addChannel(self, band, channel, interference):
        """Add a channel to the list."""
        self.channels.append(WiFiChannel(band, channel, interference))

    def removeChannel(self, band, channel):
        """Remove a channel from the list based on band and channel number."""
        self.channels = [ch for ch in self.channels if ch.band != band or ch.channel != channel]

    def getBestChannel(self, band):
        """Identify the best channel for a specific band based on interference."""
        suitableChannels = [ch for ch in self.channels if ch.band == band]
        if not suitableChannels:
            return None
        # Sorting channels by interference to pick the best one.
        suitableChannels.sort(key=lambda ch: ch.interference)
        return suitableChannels[0].channel

    def getBestChannelsPerBand(self):
        """Get the best channels across all bands."""
        bands = ['2.4GHz', '5GHz', '6GHz']
        bestChannels = {}
        for band in bands:
            bestChannels[band] = self.getBestChannel(band)
        return bestChannels

    @staticmethod
    def monitorNetworkPackets(interface="wlan0", timeout=10):
        """Capture packets to detect nearby devices based on probe requests."""
        packets = sniff(iface=interface, timeout=timeout, filter="type mgt subtype probe-req")
        nearbyDevices = set()
        for packet in packets:
            if packet.haslayer(Dot11):
                nearbyDevices.add(packet.addr2)
        return list(nearbyDevices)

    @staticmethod
    def detectNearbyNetworks(interface="wlan0", timeout=10):
        """Capture Beacon frames to learn about nearby WiFi networks."""
        packets = sniff(iface=interface, timeout=timeout, filter="type mgt subtype beacon")
        networks = {}
        for packet in packets:
            if packet.haslayer(Dot11):
                bssid = packet[Dot11].addr2  # MAC address
                ssid = packet[Dot11].info.decode("utf-8", errors="ignore")  # Network name
                networks[bssid] = ssid
        return networks

    @staticmethod
    def detectDeauth(interface="wlan0", timeout=10):
        """Detect deauthentication packets, indicative of possible attacks."""
        packets = sniff(iface=interface, timeout=timeout, filter="type mgt subtype deauth")
        detected = len(packets) > 0
        return {"detected": detected, "count": len(packets)}

# Flask routes follow:
# ...

if __name__ == "__main__":
    app.run(debug=True)
