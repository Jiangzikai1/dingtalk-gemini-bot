from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import json

app = Flask(__name__)

# 配置 Gemini API
# 从环境变量获取 Key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# 选择模型，这里使用 gemini-1.5-flash，因为它速度快且免费额度高
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # 1. 解析钉钉发来的数据
        data = request.json
        print(f"Received data: {data}")
        
        # 钉钉的消息内容在 text.content 中
        # 这里的 strip() 是为了去除可能存在的空格
        user_content = data.get('text', {}).get('content', '').strip()
        
        if not user_content:
            return jsonify({"msgtype": "text", "text": {"content": "收到空消息"}}), 200

        # 2. 调用 Gemini API
        response = model.generate_content(user_content)
        ai_reply = response.text

        # 3. 构造钉钉需要的返回格式
        # 钉钉机器人支持 markdown 格式，这样代码显示更友好
        return jsonify({
            "msgtype": "markdown",
            "markdown": {
                "title": "Gemini 回复",
                "text": f"### Gemini 回复：\n\n{ai_reply}"
            },
            "at": {
                "isAtAll": False
            }
        })

    except Exception as e:
        return jsonify({
            "msgtype": "text",
            "text": {
                "content": f"发生错误: {str(e)}"
            }
        }), 200

if __name__ == '__main__':
    app.run(debug=True)
