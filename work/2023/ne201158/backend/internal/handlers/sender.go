package handlers

import (
	"github.com/funobu/zunavi/internal/domains"
	"github.com/glassonion1/logz"
	"github.com/labstack/echo/v4"
	"golang.org/x/net/websocket"
	"log"
)

type SendHandler struct {
	clients map[string]*domains.Client
}

func NewSendHandler(clients map[string]*domains.Client) *SendHandler {
	return &SendHandler{clients: clients}
}

func (h *SendHandler) SubscribeZunavi(c echo.Context) error {
	s := websocket.Server{
		Handler: websocket.Handler(func(conn *websocket.Conn) {
			defer func(conn *websocket.Conn) {
				err := conn.Close()
				if err != nil {

				}
			}(conn)

			connID := c.Param("id")
			h.clients[connID] = domains.NewMessageManager(conn)
			for {
				message := <-h.clients[c.Param("id")].Messages
				logz.Debugf(c.Request().Context(), "send message: %v", message.ID)
				if err := websocket.JSON.Send(h.clients[connID].Connection, message); err != nil {
					log.Println(err)
				}
			}
		}),
	}

	s.ServeHTTP(c.Response(), c.Request())
	return nil
}
