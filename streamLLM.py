import time

from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import LLMResult
from typing import Union

# チャット更新間隔(秒)
CHAT_UPDATE_INTERVAL_SEC = 3

class StreamingCallbackHandler(BaseCallbackHandler):
    last_send_time = time.time()
    message = ""

    #def __init__(self, channel: str, ts: str):
    #    self.channel = channel
    #    self.ts = ts

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

    def on_llm_end(self, response: LLMResult, **kwargs: any) -> None:
        """Run when LLM ends running."""
        timenow = time.strftime("%H:%M:%S")
        #app.client.chat_update(channel=self.channel, ts=self.ts, text=self.message)
        print(f"{timenow}: {self.message}")
        self.message = ""

    def on_llm_error(
            self, error: Union[Exception, KeyboardInterrupt], **kwargs: any
    ) -> None:
        """Run when LLM errors."""


from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

API_KEY = "EMPTY"
API_BASE = "http://192.168.50.80:8080/v1"
MODEL = "gpt-3.5-turbo"

from langchain.prompts import (
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)

llm = ChatOpenAI(model_name=MODEL, 
                  openai_api_key=API_KEY, 
                  openai_api_base=API_BASE,
                  streaming=True, 
                 # callbacks=[StreamingStdOutCallbackHandler()] ,
                  callbacks=[StreamingCallbackHandler()] ,
                  temperature=0)

messages = [
    SystemMessage(content="あなたは老人ホームの介護スタッフのWANCOです．あなたの相手は老人ホームで生活する高齢者です．優しく接しましょう．"),
    HumanMessage(content="こんにちは，腰が痛いんだけれど，どうしたらよいかアドバイスしてください．")
]
resp = llm(messages)

# テンプレートの準備
template = """あなたは人間と友好的に会話するAIです。
AIはおしゃべりで、その文脈から多くの具体的な詳細を提供します。
AIが質問に対する答えを知らない場合、正直に「知らない」と言います。"""

# chatプロンプトテンプレートの準備
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(template),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

from langchain.chains import ConversationChain
#from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

# チャットモデルの準備
#llm = ChatOpenAI(temperature=0)

# メモリの準備
memory = ConversationBufferMemory(return_messages=True)

# 会話チェーンの準備
conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)

conversation.predict(input="鈴木太郎だけど，腰が痛いのですがどうしたらよいでしょう？")

conversation.predict(input="私の名前をおぼえていますか．私はどんな状態ですか？")