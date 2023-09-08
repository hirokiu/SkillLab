package handlers

import (
	"context"
	"github.com/funobu/zunavi/internal/usecases"
	"github.com/glassonion1/logz"
	"github.com/labstack/echo/v4"
	"log"
	"strconv"
)

type ReceiveHandler struct {
	receiver          usecases.MessageReceiver
	calAddressService usecases.CalculateAddress
}

func NewReceiveHandler(receiver usecases.MessageReceiver, calAddressService usecases.CalculateAddress) *ReceiveHandler {
	return &ReceiveHandler{receiver: receiver, calAddressService: calAddressService}
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

func (h *ReceiveHandler) ReceiveLatLng(c echo.Context) error {
	lat := c.FormValue("lat")
	lng := c.FormValue("lng")
	if lat == "" || lng == "" {
		return c.String(400, "Bad Request")
	}

	latitude, err := strconv.ParseFloat(lat, 64)
	if err != nil {
		logz.Warningf(c.Request().Context(), "failed to parse latitude: %v", err)
		return c.String(400, "Bad Request")
	}
	longitude, err := strconv.ParseFloat(lng, 64)
	if err != nil {
		logz.Warningf(c.Request().Context(), "failed to parse longitude: %v", err)
		return c.String(400, "Bad Request")
	}
	h.calAddressService.SetCurrentLatLng(context.Background(), latitude, longitude)

	return c.String(201, "Successfully send message!")
}
