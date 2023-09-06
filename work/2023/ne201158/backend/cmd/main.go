package main

import (
	"fmt"
	"github.com/labstack/echo/v4"
	voicevoxcorego "github.com/sh1ma/voicevoxcore.go"
	"log"
	"os"
)

func main() {
	e := echo.New()

	e.GET("/", func(c echo.Context) error {
		text := "ずんだもんなのだ"

		core := voicevoxcorego.New()
		initializeOptions := voicevoxcorego.NewVoicevoxInitializeOptions(0, 0, false, "/tmp/voicevox_core/open_jtalk_dic_utf_8-1.11")
		err := core.Initialize(initializeOptions)
		if err != nil {
			return c.String(500, err.Error())
		}
		log.Println("Initialized core")

		err = core.LoadModel(3)
		if err != nil {
			return c.String(500, err.Error())
		}
		log.Println("Loaded model")

		ttsOptions := voicevoxcorego.NewVoicevoxTtsOptions(false, true)
		log.Println("Generating...")
		result, err := core.Tts(text, 1, ttsOptions)
		if err != nil {
			fmt.Println(err)
		}
		log.Println("Success!")
		f, _ := os.Create("out.wav")
		_, err = f.Write(result)
		if err != nil {
			fmt.Println(err)
		}
		log.Println("Saved to out.wav")
		return c.String(200, "ok")
	})

	e.Logger.Fatal(e.Start(":" + os.Getenv("API_PORT")))

}
