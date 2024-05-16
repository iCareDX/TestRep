# TestRep
## streamLLM.py
Streaming出力
on_llm_new_token関数をオーバーロード
###時間ごとにチャンクを区切って，それを順次出力
###文節ごとにチャンクを区切ってやる必要があります．

def on_llm_new_token(self, token: str, **kwargs: any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        now = time.time()
        timenow = time.strftime("%H:%M:%S")
        self.message += token
        if now - self.last_send_time > CHAT_UPDATE_INTERVAL_SEC:
            self.last_send_time = now
         #   app.client.chat_update(channel=self.channel, ts=self.ts, text=f"{self.message}...")
            print(f"{timenow}: {self.message}")
            self.message = ""
