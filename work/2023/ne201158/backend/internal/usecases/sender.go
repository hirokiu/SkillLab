package usecases

import (
	"context"
	"encoding/json"
	"github.com/funobu/zunavi/internal/domains"
	"github.com/funobu/zunavi/internal/interfaces/access"
	"github.com/glassonion1/logz"
	"github.com/redis/go-redis/v9"
	"log"
	"sync"
)

type MessageSender interface {
	SendReceivedMessageWorker(ctx context.Context, text string)
}

type messageSender struct {
	aiChatService access.AIChatService
	voiceService  access.VoiceService
	// TODO: 後でインタフェース定義する
	pubsub  *redis.Client
	clients map[string]*domains.Client
	mutex   sync.Mutex
}

func NewMessageSender(voiceService access.VoiceService, aiChatService access.AIChatService, pubsub *redis.Client, clients map[string]*domains.Client) MessageSender {
	return &messageSender{voiceService: voiceService, aiChatService: aiChatService, clients: clients, pubsub: pubsub, mutex: sync.Mutex{}}
}

func (s *messageSender) SendReceivedMessageWorker(ctx context.Context, subID string) {
	subscribe := s.pubsub.Subscribe(ctx, subID)
	defer subscribe.Close()

	ch := subscribe.Channel()
	for subscription := range ch {
		var newMessage domains.Message
		if err := json.Unmarshal([]byte(subscription.Payload), &newMessage); err != nil {
			log.Println(err)
			continue
		}
		logz.Debugf(ctx, "received message: %v", newMessage.Text)

		resp, err := s.aiChatService.Ask(ctx, newMessage.Text)
		if err != nil {
			log.Println(err)
			continue
		}
		logz.Debugf(ctx, "openai response: %v", resp)

		voice, err := s.voiceService.GenerateVoice(ctx, 1, resp)
		if err != nil {
			log.Println(err)
			continue
		}

		newMessage.File = voice

		for _, client := range s.clients {
			s.mutex.Lock()
			client.Messages <- newMessage
			s.mutex.Unlock()
		}

	}

}
