package usecases

import (
	"context"
	"fmt"
	"github.com/funobu/zunavi/internal/domains"
	"github.com/funobu/zunavi/internal/interfaces/access"
	"github.com/glassonion1/logz"
	"sync"
	"time"
)

type CalculateAddress interface {
	CalculateAddressWorker(ctx context.Context)
	SetCurrentLatLng(ctx context.Context, lat, lng float64)
}

type calculateAddress struct {
	mapService     access.MapService
	currentAddress string
	geoDataList    []*domains.GeoData
	mutex          sync.Mutex
}

func NewCalculateAddress(mapService access.MapService, currentAddress string, geoDataList []*domains.GeoData) CalculateAddress {
	return &calculateAddress{mapService: mapService, currentAddress: currentAddress, geoDataList: geoDataList, mutex: sync.Mutex{}}
}

func (c *calculateAddress) CalculateAddressWorker(ctx context.Context) {
	ticker := time.NewTicker(1 * time.Minute)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			fmt.Println("Ticker stopped")
			return
		case <-ticker.C:
			nextData, err := domains.PredictNextLocation(c.geoDataList)
			if err != nil {
				logz.Errorf(ctx, "failed to predict next location: %v", err)
				continue
			}
			address, err := c.mapService.GetAddressFromLatLng(ctx, nextData.Latitude, nextData.Longitude)
			if err != nil {
				logz.Errorf(ctx, "failed to get address from latlng: %v", err)
				continue
			}

			c.mutex.Lock()
			c.currentAddress = address
			c.mutex.Unlock()
		}
	}
}

func (c *calculateAddress) SetCurrentLatLng(ctx context.Context, lat, lng float64) {
	c.mutex.Lock()
	c.geoDataList = append(c.geoDataList, &domains.GeoData{
		Latitude:  lat,
		Longitude: lng,
	})
	c.mutex.Unlock()
}
