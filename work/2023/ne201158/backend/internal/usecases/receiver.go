package usecases

import (
	"context"
	"github.com/funobu/zunavi/internal/interfaces/access"
	"github.com/funobu/zunavi/internal/interfaces/output"
)

type MessageReceiver interface {
	Ask(ctx context.Context, text string) error
}

type messageReceiver struct {
	aiService  access.AIChatService
	toReceiver output.ToReceiver
}

func NewMessageReceiver(aiService access.AIChatService, toReceiver output.ToReceiver) MessageReceiver {
	return &messageReceiver{aiService: aiService, toReceiver: toReceiver}
}

func (s messageReceiver) Ask(ctx context.Context, text string) error {
	// ここでtextをAIに投げて、結果を受け取って、toReceiverに渡す
	result, err := s.aiService.Ask(ctx, text)
	if err != nil {
		return err
	}

	return s.toReceiver.SendMessage(ctx, result)
}
