import json

class WiFiChannel:
    """This class represents a WiFi channel."""

    def __init__(
        self,
        channelNumber,
        usage,
        interference,
        noise,
        transmissionPower,
        channelWidth,
        frequencyBand,
    ):
        """
        Initializes a new instance of the WiFiAnalyzer class.

        Args:
            channelNumber (int): The channel number.
            usage (float): The percentage of channel usage.
            interference (float): The percentage of channel interference.
            noise (float): The percentage of channel noise.
            transmissionPower (float): The transmission power in dBm.
            channelWidth (float): The channel width in MHz.
            frequencyBand (str): The frequency band (e.g. 2.4 GHz, 5 GHz).
        """
        self.channelNumber = channelNumber
        self.usage = usage
        self.interference = interference
        self.noise = noise
        self.transmissionPower = transmissionPower
        self.channelWidth = channelWidth
        self.frequencyBand = frequencyBand

    def score(self):
        """Calculate a score based on various parameters."""
        width_factor = (
            1 if self.channelWidth == 20 else 1.5 if self.channelWidth == 40 else 2
        )
        return (
            -self.usage - self.interference - self.noise + self.transmissionPower
        ) * width_factor

    def update(self, **kwArgs):
        """Update channel parameters dynamically."""
        for key, value in kwArgs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __str__(self):
        return (
            f"Channel {self.channelNumber} ({self.frequencyBand}GHz): Usage({self.usage}), "
            f"Interference({self.interference}), Noise({self.noise}), Transmission Power({self.transmissionPower}), "
            f"Channel Width({self.channelWidth}MHz)"
        )


class WiFiAnalyzer:
    """
    This class represents a WiFi analyzer.

    Attributes:
        channels (dict): A dictionary containing WiFi channels.
        history (list): A list of actions performed by the analyzer.
    """

    def __init__(self):
        with open("channels.json", "r+", encoding="utf-8") as f:
            self.channels = json.load(f)
        # self.channels = {}
        self.history = []

    def save_channels_database(self):
        """Save the channels database to a JSON file."""
        with open("channels.json", "w", encoding="utf-8") as file_key:
            channels_dict = {}
            for key, value in self.channels.items():
                channels_dict[str(key)] = value.__dict__

            json.dump(channels_dict, file_key, indent=4)

    def add_or_update_channel(self, channelNumber, frequencyBand, **kwArgs):
        """Add or update a WiFi channel with dynamic parameters."""
        channel_key = (channelNumber, frequencyBand)
        if channel_key in self.channels:
            self.channels[channel_key].update(**kwArgs)
            self.log_action(f"Updated Channel {channelNumber} on {frequencyBand}GHz.")
            self.save_channels_database()
        else:
            self.channels[channel_key] = WiFiChannel(
                channelNumber, frequencyBand=frequencyBand, **kwArgs
            )
            self.log_action(f"Added Channel {channelNumber} on {frequencyBand}GHz.")
            self.save_channels_database()

    def remove_channel(self, channelNumber, frequencyBand):
        """Remove a channel."""
        channel_key = (channelNumber, frequencyBand)
        if channel_key in self.channels:
            del self.channels[channel_key]
            self.log_action(f"Removed Channel {channelNumber} on {frequencyBand}GHz.")
            self.save_channels_database()

    def display_channels(self):
        """Display channels sorted by their scores."""
        sorted_channels = sorted(
            self.channels.values(), key=lambda c: c.score(), reverse=True
        )
        for channel in sorted_channels:
            print(channel)

    def best_channel(self):
        """Determine the best channel based on the current data."""
        return max(self.channels.values(), key=lambda c: c.score(), default=None)

    def best_channel_per_band(self):
        """Compute the best channel for each frequency band and return as JSON."""
        best_channels = {"2.4GHz": None, "5GHz": None, "6GHz": None}

        for (channelNumber, frequencyBand), channel in self.channels.items():
            frequency_key = f"{frequencyBand}GHz"
            if (
                best_channels[frequency_key] is None
                or channel.score() > best_channels[frequency_key].score()
            ):
                best_channels[frequency_key] = channel

        # Convert the results into a JSON-compatible format
        json_output = {
            frequency: channel if channel else None
            for frequency, channel in best_channels.items()
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
    """This function provides a command-line interface for the WiFiAnalyzer class."""
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
            channelNumber = int(input("Enter channel number: "))
            frequencyBand = float(
                input("Choose frequency band (2.4, 5, or 6 in GHz): ")
            )
            usage = int(input("Enter usage: "))
            interference = int(input("Enter interference: "))
            noise = int(input("Enter noise: "))
            transmissionPower = int(input("Enter transmission power: "))
            channelWidth = int(
                input("Enter channel width (20, 40, 80, or 160 in MHz): ")
            )
            analyzer.add_or_update_channel(
                channelNumber,
                frequencyBand,
                usage=usage,
                interference=interference,
                noise=noise,
                transmissionPower=transmissionPower,
                channelWidth=channelWidth,
            )

        elif choice == "2":
            channelNumber = int(input("Enter channel number to remove: "))
            frequencyBand = float(
                input("Enter frequency band for the channel (2.4, 5, or 6 in GHz): ")
            )
            analyzer.remove_channel(channelNumber, frequencyBand)

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
