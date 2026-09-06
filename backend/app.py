from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3, secrets
from encryption.crypto import encrypt_password, decrypt_password

app=Flask(__name__)
CORS(app)
DB="database/password_manager.db"
TOKENS={}

def db():
    conn=sqlite3.connect(DB)
    conn.row_factory=sqlite3.Row
    return conn

def auth_required(fn):
    @wraps(fn)
    def wrapper(*args,**kwargs):
        token=request.headers.get("Authorization","").replace("Bearer ","")
        if token not in TOKENS:return jsonify(error="Unauthorized"),401
        request.user_id=TOKENS[token]
        return fn(*args,**kwargs)
    return wrapper

@app.post("/api/register")
def register():
    data=request.json or {}
    if not all(data.get(k) for k in ("name","email","password")): return jsonify(error="All fields are required"),400
    conn=db()
    try:
        conn.execute("INSERT INTO users(name,email,password_hash) VALUES(?,?,?)",(data["name"],data["email"],generate_password_hash(data["password"])))
        conn.commit()
    except sqlite3.IntegrityError:return jsonify(error="Email already registered"),409
    finally:conn.close()
    return jsonify(message="Registration successful"),201

@app.post("/api/login")
def login():
    data=request.json or {};conn=db()
    user=conn.execute("SELECT * FROM users WHERE email=?",(data.get("email"),)).fetchone();conn.close()
    if not user or not check_password_hash(user["password_hash"],data.get("password","")):return jsonify(error="Invalid email or password"),401
    token=secrets.token_urlsafe(32);TOKENS[token]=user["id"]
    return jsonify(token=token,name=user["name"])

@app.get("/api/passwords")
@auth_required
def get_passwords():
    q=request.args.get("q","%").strip()
    q=f"%{q}%"
    conn=db();rows=conn.execute("SELECT * FROM vault WHERE user_id=? AND (site LIKE ? OR username LIKE ?) ORDER BY id DESC",(request.user_id,q,q)).fetchall();conn.close()
    return jsonify(passwords=[{"id":r["id"],"site":r["site"],"username":r["username"],"password":decrypt_password(r["encrypted_password"]),"notes":r["notes"]} for r in rows])

@app.post("/api/passwords")
@auth_required
def add_password():
    d=request.json or {}
    if not all(d.get(k) for k in ("site","username","password")):return jsonify(error="Site, username and password are required"),400
    conn=db();conn.execute("INSERT INTO vault(user_id,site,username,encrypted_password,notes) VALUES(?,?,?,?,?)",(request.user_id,d["site"],d["username"],encrypt_password(d["password"]),d.get("notes","")));conn.commit();conn.close()
    return jsonify(message="Password saved"),201

@app.get("/api/passwords/<int:pid>")
@auth_required
def one(pid):
    conn=db();r=conn.execute("SELECT * FROM vault WHERE id=? AND user_id=?",(pid,request.user_id)).fetchone();conn.close()
    if not r:return jsonify(error="Not found"),404
    return jsonify(id=r["id"],site=r["site"],username=r["username"],password=decrypt_password(r["encrypted_password"]),notes=r["notes"])

@app.put("/api/passwords/<int:pid>")
@auth_required
def edit(pid):
    d=request.json or {};conn=db()
    r=conn.execute("SELECT id FROM vault WHERE id=? AND user_id=?",(pid,request.user_id)).fetchone()
    if not r:conn.close();return jsonify(error="Not found"),404
    conn.execute("UPDATE vault SET site=?,username=?,encrypted_password=?,notes=? WHERE id=? AND user_id=?",(d["site"],d["username"],encrypt_password(d["password"]),d.get("notes",""),pid,request.user_id));conn.commit();conn.close()
    return jsonify(message="Password updated")

@app.delete("/api/passwords/<int:pid>")
@auth_required
def delete(pid):
    conn=db();conn.execute("DELETE FROM vault WHERE id=? AND user_id=?",(pid,request.user_id));conn.commit();conn.close()
    return jsonify(message="Password deleted")

if __name__=="__main__":
    app.run(debug=True)
