package handlers

import (
	"github.com/funobu/zunavi/internal/usecases"
	"github.com/labstack/echo/v4"
	"log"
)

type ReceiveHandler struct {
	receiver usecases.MessageReceiver
}

func NewReceiveHandler(receiver usecases.MessageReceiver) *ReceiveHandler {
	return &ReceiveHandler{receiver: receiver}
}

func (h *ReceiveHandler) ReceiveMessage(c echo.Context) error {
	text := c.FormValue("text")
	if text == "" {
		return c.String(400, "Bad Request")
	}

	if err := h.receiver.ReceiveMessage(c.Request().Context(), text); err != nil {
		log.Println("メッセージの送信に失敗しました。")
		return c.String(500, "Internal Server Error")
	}

	return c.String(201, "Successfully send message!")
}
