package main

import (
	"context"
	"log"
	"os"
)

func main() {
	if len(os.Args) != 2 {
		log.Println("Usage: ./main <sender or receiver>")
		os.Exit(1)
	}
}

func startMessageSender(ctx context.Context) error {
	return nil
}

func startMessageReceiver(ctx context.Context) error {
	return nil
}
