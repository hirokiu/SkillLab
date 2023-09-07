package usecases

import (
	"context"
	"github.com/funobu/zunavi/internal/domains"
	"github.com/funobu/zunavi/internal/interfaces/output"
	"github.com/oklog/ulid/v2"
)

type MessageReceiver interface {
	ReceiveMessage(ctx context.Context, text string) error
}

type messageReceiver struct {
	toReceiver output.ToReceiver
}

func NewMessageReceiver(toReceiver output.ToReceiver) MessageReceiver {
	return &messageReceiver{toReceiver: toReceiver}
}

func (s messageReceiver) ReceiveMessage(ctx context.Context, text string) error {
	newMessage := &domains.Message{
		ID:   ulid.Make().String(),
		Text: text,
	}

	// TODO: PubSubへの送信失敗時のハンドリング
	// Senderに非同期でメッセージを送信する
	return s.toReceiver.SendMessage(ctx, newMessage)
}
