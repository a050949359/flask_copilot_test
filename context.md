# 專案 context

## db.py
- 提供資料庫初始化函式 `init_db()`，建立 user 與 message 兩個資料表。

## resource/user.py
- 定義 `User` Resource，提供 user 的新增與查詢 API。

## resource/message.py
- 定義 `Message` Resource，提供 message 的 CRUD API。

## app.py
- 主程式，初始化 Flask app，註冊 API Resource，啟動伺服器。

## models.py
- 目前未使用，可作為 ORM 或資料結構定義用途。
