package infrastructures

import (
	"context"
	"encoding/json"
	"github.com/funobu/zunavi/internal/domains"
	"github.com/funobu/zunavi/internal/interfaces/output"
	"github.com/redis/go-redis/v9"
	"log"
)

type RedisMessagePublisher struct {
	client *redis.Client
}

func NewRedisMessagePublisher(addr string) output.ToReceiver {
	return &RedisMessagePublisher{client: redis.NewClient(&redis.Options{
		Addr:     addr,
		Password: "",
		DB:       0,
	})}
}

func (r RedisMessagePublisher) SendMessage(ctx context.Context, message *domains.Message) error {
	byteMessage, err := json.Marshal(message)
	if err != nil {
		log.Println(err)
		return err
	}

	if _, err := r.client.Publish(ctx, "zundamon_chat", byteMessage).Result(); err != nil {
		log.Println(err)
		return err
	}

	return nil
}
