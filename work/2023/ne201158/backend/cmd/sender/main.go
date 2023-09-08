package main

import (
	"context"
	"github.com/funobu/zunavi/internal/domains"
	"github.com/funobu/zunavi/internal/handlers"
	"github.com/funobu/zunavi/internal/infrastructures"
	"github.com/funobu/zunavi/internal/usecases"
	"github.com/labstack/echo/v4"
	"github.com/redis/go-redis/v9"
	"log"
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
	messageClients := make(map[string]*domains.Client, 0)

	pubsub := redis.NewClient(&redis.Options{
		Addr:     os.Getenv("PUBSUB_ADDR"),
		Password: "",
		DB:       0,
	})

	voiceService := infrastructures.NewVoicevoxVoiceService(os.Getenv("VOICER_ADDR"))
	aiChatService := infrastructures.NewOpenAIChatService(os.Getenv("OPENAI_API_KEY"))
	messageSender := usecases.NewMessageSender(voiceService, aiChatService, pubsub, messageClients)
	go messageSender.SendReceivedMessageWorker(ctx, "zundamon_chat")

	// a
	e := echo.New()
	sendHandler := handlers.NewSendHandler(messageClients)
	e.GET("/zunavi/:id", sendHandler.SubscribeZunavi)
	if err := e.Start(":" + os.Getenv("SENDER_API_PORT")); err != nil {
		return err
	}

	return nil
}
