import json

class WiFiChannel:
    def __init__(self, channel_number, usage, interference, noise, transmission_power, channel_width, frequency_band):
        self.channel_number = channel_number
        self.usage = usage
        self.interference = interference
        self.noise = noise
        self.transmission_power = transmission_power
        self.channel_width = channel_width
        self.frequency_band = frequency_band

    def score(self):
        """Calculate a score based on various parameters."""
        width_factor = 1 if self.channel_width == 20 else 1.5 if self.channel_width == 40 else 2
        return (-self.usage - self.interference - self.noise + self.transmission_power) * width_factor

    def update(self, **kwargs):
        """Update channel parameters dynamically."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __str__(self):
        return (f"Channel {self.channel_number} ({self.frequency_band}GHz): Usage({self.usage}), "
                f"Interference({self.interference}), Noise({self.noise}), Transmission Power({self.transmission_power}), "
                f"Channel Width({self.channel_width}MHz)")


class WiFiAnalyzer:
    def __init__(self):
        self.channels = {}
        self.history = []

    def add_or_update_channel(self, channel_number, frequency_band, **kwargs):
        """Add or update a WiFi channel with dynamic parameters."""
        channel_key = (channel_number, frequency_band)
        if channel_key in self.channels:
            self.channels[channel_key].update(**kwargs)
            self.log_action(f"Updated Channel {channel_number} on {frequency_band}GHz.")
        else:
            self.channels[channel_key] = WiFiChannel(channel_number, frequency_band=frequency_band, **kwargs)
            self.log_action(f"Added Channel {channel_number} on {frequency_band}GHz.")

    def remove_channel(self, channel_number, frequency_band):
        """Remove a channel."""
        channel_key = (channel_number, frequency_band)
        if channel_key in self.channels:
            del self.channels[channel_key]
            self.log_action(f"Removed Channel {channel_number} on {frequency_band}GHz.")

    def display_channels(self):
        """Display channels sorted by their scores."""
        sorted_channels = sorted(self.channels.values(), key=lambda c: c.score(), reverse=True)
        for channel in sorted_channels:
            print(channel)

    def best_channel(self):
        """Determine the best channel based on the current data."""
        return max(self.channels.values(), key=lambda c: c.score(), default=None)

    def best_channel_per_band(self):
        """Compute the best channel for each frequency band and return as JSON."""
        best_channels = {
            "2.4GHz": None,
            "5GHz": None,
            "6GHz": None
        }
        for (channel_number, frequency_band), channel in self.channels.items():
            frequency_key = f"{frequency_band}GHz"
            if best_channels[frequency_key] is None or channel.score() > best_channels[frequency_key].score():
                best_channels[frequency_key] = channel
        
        # Convert the results into a JSON-compatible format
        json_output = {
            frequency: channel.__str__() if channel else None for frequency, channel in best_channels.items()
        }
        return json.dumps(json_output, indent=4)

    def log_action(self, message):
        """Log actions for history."""
        self.history.append(message)

    def display_history(self):
        """Display a log of all actions."""
        for entry in self.history:
            print(entry)

    def summary(self):
        """Provide a summary of the best channel."""
        best = self.best_channel()
        if best:
            print(f"\nThe best WiFi channel is {best}.\n")
        else:
            print("\nNo channel data available.\n")


def main():
    analyzer = WiFiAnalyzer()
    
    while True:
        print("\nOptions:")
        print("1. Add/Update Channel")
        print("2. Remove Channel")
        print("3. Display Channels")
        print("4. Best Channel Summary")
        print("5. Best Channels per Band (JSON output)")
        print("6. Display History")
        print("7. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            channel_number = int(input("Enter channel number: "))
            frequency_band = float(input("Choose frequency band (2.4, 5, or 6 in GHz): "))
            usage = int(input("Enter usage: "))
            interference = int(input("Enter interference: "))
            noise = int(input("Enter noise: "))
            transmission_power = int(input("Enter transmission power: "))
            channel_width = int(input("Enter channel width (20, 40, 80, or 160 in MHz): "))
            analyzer.add_or_update_channel(channel_number, frequency_band, usage=usage, interference=interference, 
                                           noise=noise, transmission_power=transmission_power, channel_width=channel_width)
            
        elif choice == "2":
            channel_number = int(input("Enter channel number to remove: "))
            frequency_band = float(input("Enter frequency band for the channel (2.4, 5, or 6 in GHz): "))
            analyzer.remove_channel(channel_number, frequency_band)
            
        elif choice == "3":
            analyzer.display_channels()

        elif choice == "4":
            analyzer.summary()

        elif choice == "5":
            print(analyzer.best_channel_per_band())

        elif choice == "6":
            analyzer.display_history()

        elif choice == "7":
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
