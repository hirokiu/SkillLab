package access

import "context"

type AIChatService interface {
	Ask(ctx context.Context, text string) (string, error)
}

type VoiceService interface {
	GenerateVoice(ctx context.Context, characterID int, text string) ([]byte, error)
}

type MapService interface {
	GetAddressFromLatLng(ctx context.Context, lat, lng float64) (string, error)
}
