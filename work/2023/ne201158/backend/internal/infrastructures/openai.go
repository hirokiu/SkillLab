package infrastructures

import (
	"context"
	"github.com/funobu/zunavi/internal/interfaces/access"
	"github.com/sashabaranov/go-openai"
)

type OpenAIChatService struct {
	client *openai.Client
}

func NewOpenAIChatService(APIKey string) access.AIChatService {
	client := openai.NewClient(APIKey)
	return &OpenAIChatService{client: client}
}

func (o OpenAIChatService) Ask(ctx context.Context, text string) (string, error) {
	resp, err := o.client.CreateChatCompletion(ctx, openai.ChatCompletionRequest{
		Model: openai.GPT3Dot5Turbo0613,
		Messages: []openai.ChatCompletionMessage{
			{
				Role: openai.ChatMessageRoleSystem,
				Content: `
あなたの名前はずんだもんです。一人称は「ボク」です。
性別は女性です。おっとりおだやか、前向きで明るい母性の塊のような性格です。
どんな相手、物事にも基本的に肯定から入ります。語尾には必ず「なのだー。」をつけてください。
また、回答は100文字以内で簡潔にお願いします。
以上の設定を忠実に守り、あなたはずんだもんとして振る舞ってください。
				 `,
			},
			{
				Role:    openai.ChatMessageRoleUser,
				Content: text,
			},
		},
	})
	if err != nil {
		return "", err
	}

	return resp.Choices[0].Message.Content, nil
}
