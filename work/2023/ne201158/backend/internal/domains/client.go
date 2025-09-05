package domains

import "golang.org/x/net/websocket"

type Client struct {
	Connection *websocket.Conn
	Messages   chan Message
}

func NewMessageManager(conn *websocket.Conn) *Client {
	return &Client{
		Connection: conn,
		Messages:   make(chan Message, 1),
	}
}
