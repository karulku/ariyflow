from flask import Flask, jsonify, render_template, send_from_directory, request
from flask_socketio import SocketIO, emit
from threading import Thread
import time

app = Flask(__name__)
socketio = SocketIO(app=app)

def sendTimer():
    while True:
        socketio.emit("time", {"time":time.time()})
        time.sleep(1)

@app.route('/')
def default():
    return render_template('./home.html')

@app.route("/qian-ru-shi-lab2")
def qian_ru_shi_lab2():
    return send_from_directory("qian-ru-shi-lab2", "index.html")

@app.route("/test", methods=["GET", "POST"])
def test():
    if request.method == "POST":
        data = request.data
        return jsonify({"resp":"hello", "data":data.decode("utf-8")})
    elif request.method == "GET":
        return "abc"
    else:
        return "a" 

@socketio.on("connect")
def handle_connect():
    print("Client connected")
    Thread(target=sendTimer).start()

@socketio.on("message")
def handle_message(msg):
    print(f"Receive message: {msg}")
    socketio.emit("update_board", msg)
    

# 用于嵌入式小班匿名评分
@app.route("/pingfen", methods=["GET", "POST"])
def pingfen():
    if request.method == "GET":
        token_list = []
        with open("./tmp_token_list.txt", mode="r", encoding="utf-8") as file:
            token_list = file.readlines()
            token_list = [token.strip() for token in token_list]
        
        for token in token_list:
            if(request.args.get("token") == token):
                print(f"token: {token}")
                # token_list.remove(token)
                # with open("./tmp_token_list.txt", mode="w", encoding="utf-8") as file:
                #     for t in token_list:
                #         file.write(t+"\n")
                
                return render_template("pingfen.html")
        
        return render_template("home.html")
    
    elif request.method == "POST":
        data = request.form.to_dict()
        print(data)
        with open("./score.csv", mode="a", encoding="utf-8") as file:
            score_list = [data[d] for d in data]
            file.write(",".join(score_list)+"\n")
        return render_template("finish.html")
    else:
        return render_template("home.html")

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)