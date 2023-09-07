package output

import "context"

type ToReceiver interface {
	SendMessage(ctx context.Context, message string) error
}
