package usecases

import (
	"context"
	"encoding/json"
	"github.com/funobu/zunavi/internal/domains"
	"github.com/funobu/zunavi/internal/interfaces/access"
	"github.com/redis/go-redis/v9"
	"log"
	"sync"
)

type MessageSender interface {
	SendReceivedMessageWorker(ctx context.Context, text string)
}

type messageSender struct {
	voiceService access.VoiceService
	// TODO: 後でインタフェース定義する
	pubsub  *redis.Client
	clients map[string]*domains.Client
	mutex   sync.Mutex
}

func NewMessageSender(voiceService access.VoiceService, pubsub *redis.Client, clients map[string]*domains.Client) MessageSender {
	return &messageSender{voiceService: voiceService, clients: clients, pubsub: pubsub, mutex: sync.Mutex{}}
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

		voice, err := s.voiceService.GenerateVoice(ctx, 1, newMessage.Text)
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
