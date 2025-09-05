package domains

import "fmt"

type GeoData struct {
	ID        string  `json:"id"`
	Latitude  float64 `json:"latitude"`
	Longitude float64 `json:"longitude"`
}

func PredictNextLocation(data []*GeoData) (*GeoData, error) {
	if len(data) < 2 {
		return nil, fmt.Errorf("insufficient data to make prediction")
	}

	// Change in latitude and longitude between the last two data points
	deltaLat := data[len(data)-1].Latitude - data[len(data)-2].Latitude
	deltaLon := data[len(data)-1].Longitude - data[len(data)-2].Longitude

	// Predict the next location
	nextLat := data[len(data)-1].Latitude + deltaLat
	nextLon := data[len(data)-1].Longitude + deltaLon

	return &GeoData{
		ID:        fmt.Sprintf("%d", len(data)+1),
		Latitude:  nextLat,
		Longitude: nextLon,
	}, nil
}
