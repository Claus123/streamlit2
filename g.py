import os
from openai import OpenAI
from plyer import notification  # plyerのnotificationモジュールをインポート

# ファイルから入力テキストを読み込む
with open('入力.txt', 'r', encoding='utf-8') as file:
    input_text = file.read().strip()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": input_text,
        }
    ],
    model="gpt-4-0125-preview",
)

# 'content' の部分のみを抽出してファイルに書き込む
output_content = chat_completion.choices[0].message.content
with open('出力.txt', 'w', encoding='utf-8') as file:
    file.write(output_content)

# ファイルへの書き込みが完了したらデスクトップ上で通知をする
notification.notify(
    title='完了通知',
    message='ファイルへの書き込みが完了しました。',
    app_name='通知アプリ',
    timeout=5  # 通知を表示する時間 (秒)
)