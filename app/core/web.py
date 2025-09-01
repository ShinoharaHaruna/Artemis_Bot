from flask import Flask, jsonify

# 初始化 Flask 应用
# Initialize Flask app
web_app = Flask(__name__)


@web_app.route("/health", methods=["GET"])
def health_check():
    """
    提供一个简单的 health check 接口。
    Provides a simple health check endpoint.
    """
    # 返回一个 JSON 响应，表示服务状态良好
    # Return a JSON response indicating the service is healthy
    return jsonify({"status": "ok"}), 200
