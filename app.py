
from flask import Flask ,render_template ,request ,session,redirect,url_for,flash
app = Flask(__name__)
app.secret_key ="hanan_2004"

products=[
    {"id":1,"name":"Classic Dress","price":500,"brand":"zara","image":"black.jpg"},
    {"id":2,"name":" Dress","price":1000,"brand":"zara","image":"dress1.jpg"},
    {"id":3,"name":"white Dress","price":900,"brand":"tommy","image":"white.jpg"},
    {"id":4,"name":" Dress 2piece","price":600,"brand":"H&M","image":"skirt.jpg"},
    {"id":5,"name":"Classic Dress","price":1100,"brand":"chanel","image":"btengany.jpg"}

]
brands=[
    {"id":1,"name":"Zara"},{"id":2,"name":"H&M"},{"id":3,"name":"Nike"},{"id":4,"name":"Tommy"},
    {"id":5,"name":"Chanel"}
]
@app.route("/")
def home():
    count =len(session.get('cart',[]))
    return render_template ("project.html",products=products,brands=brands,cart_count=count)


@app.route('/search',methods=['POST'])
def search():
    query   = request.form.get('User_query')
    result = [p for p in products if query.lower()in p['name'].lower()or query.lower() in p['brand'].lower()]
    return render_template ("project.html",products=result,brands=brands)    
@app.route('/filter/<brand_name>')
def filter_brand(brand_name):
    result = [p for p in products if p['brand'].lower()== brand_name.lower()]
    return render_template ("project.html",products=result,brands=brands)
@app.route('/add/<int:product_id>',methods=['GET','POST'])
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart']={}
    id_str =str(product_id)
    if id_str in session['cart']:
        session['cart'][id_str] +=1
    else:
        session['cart'][id_str]=1
    session.modified=True
    return redirect(request.referrer or url_for('home'))
@app.route('/cart')
def view_cart():
    cart_ids = session.get('cart',{})
    items_in_cart=[]
    total_price = 0
    for product_id_str,quantity in cart_ids.items():
        for p in products:
           if str (p['id'])== product_id_str:
              item_data = p.copy()
              item_data['quantity']=quantity
              items_in_cart.append(item_data)
              total_price +=p['price']*quantity
              break
    return render_template ("cart.html",items=items_in_cart,total=total_price)
@app.route('/decrease/<int:product_id>')
def decrease_cart(product_id):
    if 'cart' in session:
     id_str =str(product_id)
     if id_str in session['cart']:
        if session['cart'][id_str]>1:
          session['cart'][id_str] -=1
    session.modified=True
    return redirect(request.referrer or url_for('home'))
@app.route('/remove/<int:product_id>')
def remove_to_cart(product_id):
    cart = session.get('cart',{})
    if 'cart' in session:
      id_str= str(product_id)
      if id_str in session['cart']:
        session['cart'].pop(id_str)
        session.modified=True
    return redirect(url_for('view_cart'))

@app.route('/checkout')
def checkout():
    cart_ids = session.get('cart',[])
    items_in_cart=[]
    total_price = 0
    for p in products:
        quantity = cart_ids.get(str(p["id"]),0)
        if quantity > 0 :
            total_price +=p['price'] *quantity
    return render_template("payment.html",total=total_price)
@app.route('/complate_order',methods=['GET','POST'])
def complate_order():

    if request.method=='POST':
        method = request.form.get('payment_method')
        print(f"User chose to pay via:{method}")

    session['cart']={}
    session.modified=True
    return redirect(url_for('home'))

app.run(debug=True)