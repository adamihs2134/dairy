from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 日記モデル
class Diary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    entry = db.Column(db.Text, nullable=False)
    goal = db.Column(db.Text, nullable=False)


DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # フォームから送られたデータを取得
    date = request.form['date']
    entry = request.form['entry']
    goal = request.form['goal']

    # 日記内容をファイルに保存
    with open(os.path.join(DATA_DIR, "diary.txt"), "a", encoding="utf-8") as file:
        file.write(f"日付: {date}\n")
        file.write(f"日記内容: {entry}\n")
        file.write(f"目標: {goal}\n")
        file.write("-" * 30 + "\n")

    return f"日記を保存しました！ 日付: {date}, 目標: {goal}"

@app.route('/diary')
def diary():
    # diary.txtの内容を読み込んで表示
    diary_entries = []
    try:
        with open(os.path.join(DATA_DIR, "diary.txt"), "r", encoding="utf-8") as file:
            diary_entries = file.readlines()
    except FileNotFoundError:
        diary_entries = ["まだ日記がありません。"]

    return render_template('diary.html', diary_entries=diary_entries)

if __name__ == '__main__':
    app.run(debug=True)
