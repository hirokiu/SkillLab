package output

import (
	"context"
	"github.com/funobu/zunavi/internal/domains"
)

type ToReceiver interface {
	SendMessage(ctx context.Context, message *domains.Message) error
}
