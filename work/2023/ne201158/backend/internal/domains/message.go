package domains

type Message struct {
	ID      string `json:"id"`
	Text    string `json:"text"`
	Address string `json:"address"`
	File    []byte `json:"file"`
}
