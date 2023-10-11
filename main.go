package main

import (
	"fmt"
	"github.com/gofiber/fiber/v2"
	"strconv"
	"sync"
)

type WiFiChannel struct {
	ChannelNumber      int     `json:"channel_number"`
	FrequencyBand      float64 `json:"frequency_band"`
	Usage              int     `json:"usage"`
	Interference       int     `json:"interference"`
	Noise              int     `json:"noise"`
	TransmissionPower  int     `json:"transmission_power"`
	ChannelWidth       int     `json:"channel_width"`
}

var (
	channels     = make(map[string]WiFiChannel)
	mux          = &sync.Mutex{}
	channelMutex = &sync.RWMutex{} 
)

func generateChannelID(channel WiFiChannel) string {
	return fmt.Sprintf("%d-%.1f", channel.ChannelNumber, channel.FrequencyBand)
}

func calculateChannelScore(channel WiFiChannel) int {
	// Example scoring function, you can modify based on requirements
	return channel.Usage - channel.Interference + channel.Noise - channel.TransmissionPower + channel.ChannelWidth
}

func AddOrUpdateChannel(c *fiber.Ctx) error {
	channel := new(WiFiChannel)
	if err := c.BodyParser(channel); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Cannot parse JSON"})
	}

	mux.Lock()
	channelID := generateChannelID(*channel)
	channels[channelID] = *channel
	mux.Unlock()

	return c.Status(fiber.StatusOK).JSON(fiber.Map{"message": "Channel added/updated successfully."})
}

func RemoveChannel(c *fiber.Ctx) error {
	channelNumber, _ := strconv.Atoi(c.Params("channelNumber"))
	frequencyBand, _ := strconv.ParseFloat(c.Params("frequencyBand"), 64)
	channelID := fmt.Sprintf("%d-%.1f", channelNumber, frequencyBand)

	mux.Lock()
	delete(channels, channelID)
	mux.Unlock()

	return c.Status(fiber.StatusOK).JSON(fiber.Map{"message": "Channel removed successfully."})
}

func DisplayChannels(c *fiber.Ctx) error {
	mux.Lock()
	defer mux.Unlock()
	return c.JSON(channels)
}

func BestChannelSummary(c *fiber.Ctx) error {
	bestChannel := WiFiChannel{}
	bestScore := int(^uint(0) >> 1) // Initialize to highest possible int value

	channelMutex.RLock()
	for _, channel := range channels {
		score := calculateChannelScore(channel)
		if score < bestScore {
			bestScore = score
			bestChannel = channel
		}
	}
	channelMutex.RUnlock()

	if bestScore == int(^uint(0)>>1) {
		return c.Status(fiber.StatusOK).JSON(fiber.Map{"message": "No channel data available."})
	}

	return c.Status(fiber.StatusOK).JSON(bestChannel)
}

func main() {
	app := fiber.New()

	api := app.Group("/api")

	api.Post("/channel", AddOrUpdateChannel)
	api.Delete("/channel/:channelNumber/:frequencyBand", RemoveChannel)
	api.Get("/channels", DisplayChannels)
	api.Get("/bestChannelSummary", BestChannelSummary)

	app.Listen(":3000")
}
