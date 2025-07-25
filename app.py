from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

app = Flask(__name__)
CORS(app)

# Hugging Face API設定
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_TOKEN}"
}

def format_prompt(boke, tsukkomi):
    return f"""
あなたはお笑い評論家です。以下の「ボケ」と「ツッコミ」を読んでください。

ボケ：
「{boke}」

ツッコミ：
「{tsukkomi}」

このツッコミの評価を100点満点で行ってください。また、その理由もユーモラスに1〜2文で説明してください。

【評価例の形式】
点数: 85点
講評: 着眼点は面白いが、ややベタすぎる印象。もうひとひねりあれば高得点だったかも！
"""

@app.route("/rate", methods=["POST"])
def rate():
    data = request.json
    prompt = format_prompt(data["boke"], data["tsukkomi"])

    response = requests.post(
        HUGGINGFACE_API_URL,
        headers=headers,
        json={"inputs": prompt}
    )

    try:
        result = response.json()
        output = result[0]["generated_text"]
    except Exception as e:
        print("APIレスポンスエラー:", e)
        print("response.text:", response.text)
        output = "AIの応答が失敗しました。もう一度お試しください。"

    return jsonify({"result": output})

if __name__ == "__main__":
    app.run(debug=True)
