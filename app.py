from flask import Flask,render_template,request
import sqlite3 as sql

app=Flask(__name__)

l=[]
@app.route("/")
def show():
    conn=sql.connect("shop.db")
    cur=conn.cursor()
    cur.execute("select * from buyer")
    a=cur.fetchall()
    for i in a:
        dict={"user_name":i[0],"mobile":i[1],"amount":i[2]}
        l.append(dict)
    return render_template("show.html",data=l)

l2=[]
@app.route("/price")
def price():
    conn=sql.connect("shop.db")
    cur=conn.cursor()
    cur.execute("select * from product")
    a=cur.fetchall()
    for i in a:
        dict={"product_name":i[0],"price":i[1]}
        l2.append(dict)
    return render_template("product.html",data=l2)

@app.route("/update",methods=["POST","GET"])
def update():
    if request.form.get("user_name")!=None:
        name=request.form.get("user_name")
        mobile=request.form.get("mobile_no")
        product=request.form.get("product_name")
        quantity=request.form.get("quantity")
        conn=sql.connect("shop.db")
        cur=conn.cursor()
        cur.execute("insert into purchase(user_name,mobile_no,product_name,quantity) values (?,?,?,?)",(name,mobile,product,quantity))
        conn.commit()

        cur.execute("select price from product where product_name=?",(product,))
        minus=cur.fetchall()
        minus=minus[0][0]
        quantity=int(quantity)
        minus=minus*quantity

        cur.execute("update buyer set amount=amount-? where mobile=?",(minus,mobile))
        conn.commit()

        l3=[]
        conn=sql.connect("shop.db")
        cur=conn.cursor()
        cur.execute("select * from buyer")
        a=cur.fetchall()
        for i in a:
            dict={"user_name":i[0],"mobile":i[1],"amount":i[2]}
            l3.append(dict)

        return render_template("show.html",data=l3)
    
    return render_template("index.html")


if __name__=="__main__":
    app.run(debug=True)