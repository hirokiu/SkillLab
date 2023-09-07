package domains

type Message struct {
	ID   string `json:"id"`
	Text string `json:"text"`
	File []byte `json:"file"`
}
