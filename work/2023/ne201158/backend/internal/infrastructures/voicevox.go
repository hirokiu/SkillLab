package infrastructures

import (
	"context"
	"github.com/funobu/zunavi/internal/infrastructures/generated"
	"github.com/funobu/zunavi/internal/interfaces/access"
	"github.com/glassonion1/logz"
	"io"
	"log"
)

type VoicevoxVoiceService struct {
	client *generated.Client
}

func NewVoicevoxVoiceService(voicerAddr string) access.VoiceService {
	client, err := generated.NewClient(voicerAddr)
	if err != nil {
		log.Println(err)
		return nil
	}
	return &VoicevoxVoiceService{client: client}
}

func (v VoicevoxVoiceService) GenerateVoice(ctx context.Context, characterID int, text string) ([]byte, error) {
	audioQueryRes, err := v.client.AudioQueryAudioQueryPost(ctx, &generated.AudioQueryAudioQueryPostParams{
		Text:    text,
		Speaker: characterID,
	})
	if err != nil {
		logz.Errorf(ctx, "failed to generate audio query: %v", err)
		return nil, err
	}

	defer audioQueryRes.Body.Close()

	audioQueryResp, err := generated.ParseAudioQueryAudioQueryPostResponse(audioQueryRes)
	if err != nil {
		return nil, err
	}

	audioRes, err := v.client.SynthesisSynthesisPost(ctx, &generated.SynthesisSynthesisPostParams{
		Speaker: characterID,
	}, generated.SynthesisSynthesisPostJSONRequestBody{
		AccentPhrases:      audioQueryResp.JSON200.AccentPhrases,
		SpeedScale:         audioQueryResp.JSON200.SpeedScale,
		PitchScale:         audioQueryResp.JSON200.PitchScale,
		IntonationScale:    audioQueryResp.JSON200.IntonationScale,
		VolumeScale:        audioQueryResp.JSON200.VolumeScale,
		PrePhonemeLength:   audioQueryResp.JSON200.PrePhonemeLength,
		PostPhonemeLength:  audioQueryResp.JSON200.PostPhonemeLength,
		OutputSamplingRate: audioQueryResp.JSON200.OutputSamplingRate,
		OutputStereo:       audioQueryResp.JSON200.OutputStereo,
		Kana:               audioQueryResp.JSON200.Kana,
	})
	if err != nil {
		logz.Errorf(ctx, "failed to generate voice: %v", err)
		return nil, err
	}

	defer audioRes.Body.Close()

	if audioRes.Header.Get("Content-Type") != "audio/wav" {
		logz.Errorf(ctx, "failed to generate voice data: %v", err)
		return nil, err
	}

	audioByte, err := io.ReadAll(audioRes.Body)
	if err != nil {
		log.Println(err)
		return nil, err
	}

	return audioByte, nil
}
