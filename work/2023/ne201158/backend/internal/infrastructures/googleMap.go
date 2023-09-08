package infrastructures

import (
	"context"
	"github.com/funobu/zunavi/internal/interfaces/access"
	"github.com/glassonion1/logz"
	"googlemaps.github.io/maps"
)

type GoogleMapService struct {
	client *maps.Client
}

func NewGoogleMapService(ctx context.Context, apiKey string) access.MapService {
	client, err := maps.NewClient(maps.WithAPIKey(apiKey))
	if err != nil {
		logz.Criticalf(ctx, "failed to create google map client: %v", err)
	}
	return &GoogleMapService{client: client}
}

func (g GoogleMapService) GetAddressFromLatLng(ctx context.Context, lat, lng float64) (string, error) {
	req := &maps.GeocodingRequest{
		LatLng: &maps.LatLng{
			Lat: lat,
			Lng: lng,
		},
	}

	results, err := g.client.ReverseGeocode(ctx, req)
	if err != nil {
		return "", err
	}

	return results[0].FormattedAddress, nil
}
