package main

import (
	"context"
	"github.com/funobu/zunavi/internal/domains"
	"github.com/funobu/zunavi/internal/handlers"
	"github.com/funobu/zunavi/internal/infrastructures"
	"github.com/funobu/zunavi/internal/usecases"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	"log"
	"net/http"
	"os"
	"os/signal"
)

func main() {
	ctx, cancel := signal.NotifyContext(context.Background(), os.Interrupt)
	defer cancel()

	if err := startMessageSender(ctx); err != nil {
		log.Println(err)
		os.Exit(0)
	}
}

func startMessageSender(ctx context.Context) error {
	// TODO: ユーザごとにデータを分ける
	// Shared data
	var currentAddress string
	geoDataList := make([]*domains.GeoData, 0)

	// Dependency Injection
	mapService := infrastructures.NewGoogleMapService(ctx, os.Getenv("GOOGLE_MAP_API_KEY"))
	messagePublishToSender := infrastructures.NewRedisMessagePublisher(os.Getenv("PUBSUB_ADDR"))
	messageReceiver := usecases.NewMessageReceiver(messagePublishToSender)
	calculateAddress := usecases.NewCalculateAddress(mapService, currentAddress, geoDataList)

	go calculateAddress.CalculateAddressWorker(ctx)

	e := echo.New()
	e.Use(middleware.CORSWithConfig(middleware.CORSConfig{
		AllowOrigins: []string{"*"},
		AllowMethods: []string{http.MethodGet, http.MethodPost},
	}))

	sendHandler := handlers.NewReceiveHandler(messageReceiver)
	e.POST("/message", sendHandler.ReceiveMessage)
	e.POST("/geo", sendHandler.ReceiveLatLng)
	if err := e.Start(":" + os.Getenv("RECEIVER_API_PORT")); err != nil {
		return err
	}

	return nil
}
