from flask import Flask, render_template, request, abort

app = Flask(__name__)

# ------------------------------------------------------------------
# CENTRAL PRODUCT CATALOG (in production, this would come from a DB)
# ------------------------------------------------------------------
def p(name, brand, price, mrp, rating, emoji, bg):
    """Helper to build a product dict quickly."""
    discount = round((mrp - price) / mrp * 100)
    return {
        "name": name, "brand": brand,
        "price": price, "mrp": mrp, "discount": discount,
        "rating": rating, "emoji": emoji, "bg": bg,
    }

CATEGORY_DATA = {
    "fashion": {
        "title": "Fashion",
        "icon": "👕",
        "subcategories": ["Men", "Women", "Kids", "Footwear", "Watches", "Bags"],
        "products": [
            p("Men Slim Fit Jeans", "Levis", 1299, 2999, 4.3, "👖", "#e3f2fd"),
            p("Women Floral Kurti", "Libas", 699, 1999, 4.5, "👗", "#fce4ec"),
            p("Running Shoes", "Nike", 3499, 6999, 4.4, "👟", "#e8f5e9"),
            p("Analog Watch", "Titan", 2499, 4999, 4.6, "⌚", "#fff3e0"),
            p("Leather Handbag", "Caprese", 1799, 3999, 4.2, "👜", "#f3e5f5"),
            p("Kids T-Shirt", "Allen Solly", 499, 999, 4.1, "👕", "#e0f7fa"),
            p("Sunglasses", "Fastrack", 899, 1799, 4.0, "🕶️", "#e1f0ff"),
            p("Cotton Saree", "Fabindia", 2199, 4499, 4.7, "🥻", "#fce4ec"),
        ],
    },
    "mobiles": {
        "title": "Mobiles",
        "icon": "📱",
        "subcategories": ["5G Phones", "Budget", "Flagship", "Accessories", "Cases", "Powerbanks"],
        "products": [
            p("Galaxy S25 5G", "Samsung", 54999, 69999, 4.6, "📱", "#e3f2fd"),
            p("iPhone 16 Pro", "Apple", 119900, 129900, 4.8, "📱", "#f3e5f5"),
            p("OnePlus 13R", "OnePlus", 39999, 45999, 4.5, "📱", "#e8f5e9"),
            p("Redmi Note 14", "Xiaomi", 14999, 18999, 4.3, "📱", "#fff3e0"),
            p("Vivo T5x 5G", "Vivo", 16999, 21999, 4.4, "📱", "#e0f7fa"),
            p("OPPO K14x 5G", "OPPO", 16999, 20999, 4.2, "📱", "#e1f0ff"),
            p("Realme Narzo 80", "Realme", 12999, 15999, 4.1, "📱", "#fce4ec"),
            p("Phone Case", "Spigen", 499, 999, 4.5, "🛡️", "#e8f5e9"),
        ],
    },
    "electronics": {
        "title": "Electronics",
        "icon": "💻",
        "subcategories": ["Laptops", "TVs", "Cameras", "Headphones", "Speakers", "Gaming"],
        "products": [
            p("MacBook Air M3", "Apple", 99900, 114900, 4.8, "💻", "#e3f2fd"),
            p('43" Smart TV', "Xiaomi", 19499, 29999, 4.4, "📺", "#e8f5e9"),
            p("Sony WH-1000XM5", "Sony", 26999, 34999, 4.7, "🎧", "#f3e5f5"),
            p("DSLR Camera", "Canon", 45999, 55999, 4.6, "📷", "#fff3e0"),
            p("Bluetooth Speaker", "JBL", 3999, 5999, 4.5, "🔊", "#e0f7fa"),
            p("Gaming Console", "Sony PS5", 49999, 54999, 4.9, "🎮", "#e1f0ff"),
            p("Wireless Mouse", "Logitech", 899, 1499, 4.4, "🖱️", "#fce4ec"),
            p("Mechanical Keyboard", "Keychron", 6999, 8999, 4.6, "⌨️", "#e8f5e9"),
        ],
    },
    "beauty": {
        "title": "Beauty",
        "icon": "💄",
        "subcategories": ["Makeup", "Skincare", "Haircare", "Fragrance", "Men's Grooming"],
        "products": [
            p("Matte Lipstick", "Maybelline", 349, 599, 4.4, "💄", "#fce4ec"),
            p("Vitamin C Serum", "Minimalist", 599, 799, 4.5, "🧴", "#e3f2fd"),
            p("Face Wash", "Cetaphil", 399, 599, 4.6, "🧼", "#e8f5e9"),
            p("Hair Dryer", "Philips", 1299, 1999, 4.3, "💇", "#f3e5f5"),
            p("Perfume", "Fogg", 499, 899, 4.2, "🧴", "#fff3e0"),
            p("Beard Trimmer", "Philips", 1499, 2499, 4.5, "✂️", "#e0f7fa"),
            p("Kajal", "Lakme", 199, 349, 4.4, "👁️", "#e1f0ff"),
            p("Body Lotion", "Nivea", 299, 449, 4.5, "🧴", "#fce4ec"),
        ],
    },
    "home": {
        "title": "Home",
        "icon": "🛋️",
        "subcategories": ["Furniture", "Decor", "Kitchen", "Bedding", "Lighting"],
        "products": [
            p("Sofa Set 3+1+1", "Godrej", 24999, 39999, 4.5, "🛋️", "#e3f2fd"),
            p("Dining Table", "Nilkamal", 12999, 18999, 4.3, "🍽️", "#e8f5e9"),
            p("Bedsheet Set", "Bombay Dyeing", 899, 1499, 4.4, "🛏️", "#fce4ec"),
            p("LED Bulb Pack", "Philips", 499, 899, 4.6, "💡", "#fff3e0"),
            p("Wall Clock", "Ajanta", 299, 599, 4.2, "🕰️", "#f3e5f5"),
            p("Cushion Covers", "Home Centre", 599, 999, 4.3, "🪑", "#e0f7fa"),
            p("Non-stick Pan", "Prestige", 899, 1499, 4.5, "🍳", "#e1f0ff"),
            p("Storage Box", "Cello", 399, 699, 4.1, "📦", "#fce4ec"),
        ],
    },
    "appliances": {
        "title": "Appliances",
        "icon": "📺",
        "subcategories": ["Refrigerators", "Washing Machines", "ACs", "Microwaves", "Fans"],
        "products": [
            p("Double Door Fridge", "LG", 28999, 39999, 4.6, "🧊", "#e3f2fd"),
            p("Front Load Washer", "Bosch", 32999, 45999, 4.7, "🧺", "#e8f5e9"),
            p("1.5T Split AC", "Daikin", 38999, 52999, 4.5, "❄️", "#f3e5f5"),
            p("Convection Microwave", "Samsung", 12999, 18999, 4.4, "🍲", "#fff3e0"),
            p("Ceiling Fan", "Havells", 2499, 3999, 4.3, "🌀", "#e0f7fa"),
            p("Water Purifier", "Kent", 12999, 17999, 4.5, "💧", "#e1f0ff"),
            p("Air Purifier", "Mi", 8999, 12999, 4.4, "🌬️", "#fce4ec"),
            p("Vacuum Cleaner", "Eureka Forbes", 8999, 12999, 4.5, "🧹", "#e8f5e9"),
        ],
    },
    "toys": {
        "title": "Toys",
        "icon": "🧸",
        "subcategories": ["Action Figures", "Board Games", "Puzzles", "Soft Toys", "Educational"],
        "products": [
            p("Teddy Bear 24in", "Hamleys", 799, 1499, 4.5, "🧸", "#fce4ec"),
            p("LEGO Set 500pc", "LEGO", 2499, 3999, 4.8, "🧱", "#e3f2fd"),
            p("Monopoly Board", "Hasbro", 999, 1799, 4.4, "🎲", "#e8f5e9"),
            p("RC Car", "Toy Kingdom", 1499, 2499, 4.2, "🚗", "#fff3e0"),
            p("Puzzle 1000pc", "Funskool", 599, 999, 4.3, "🧩", "#f3e5f5"),
            p("Doll House", "Barbie", 2999, 4499, 4.6, "🏠", "#e0f7fa"),
            p("Science Kit", "Smartivity", 899, 1499, 4.5, "🔬", "#e1f0ff"),
            p("Play Doh Set", "Hasbro", 499, 799, 4.4, "🎨", "#fce4ec"),
        ],
    },
    "food": {
        "title": "Food & Health",
        "icon": "🍔",
        "subcategories": ["Snacks", "Beverages", "Health Drinks", "Organic", "Supplements"],
        "products": [
            p("Whey Protein 1kg", "Optimum Nutrition", 3499, 4999, 4.6, "💪", "#e3f2fd"),
            p("Green Tea 100 bags", "Tetley", 499, 799, 4.4, "🍵", "#e8f5e9"),
            p("Mixed Dry Fruits 1kg", "Happilo", 1299, 1999, 4.5, "🥜", "#fff3e0"),
            p("Multivitamin 60tabs", "Revital", 599, 999, 4.3, "💊", "#f3e5f5"),
            p("Olive Oil 1L", "Borges", 899, 1299, 4.6, "🫒", "#e0f7fa"),
            p("Honey 500g", "Dabur", 349, 549, 4.4, "🍯", "#e1f0ff"),
            p("Dark Chocolate", "Lindt", 399, 599, 4.7, "🍫", "#fce4ec"),
            p("Coffee Beans 500g", "Blue Tokai", 699, 999, 4.5, "☕", "#e8f5e9"),
        ],
    },
    "auto": {
        "title": "Auto Accessories",
        "icon": "🚗",
        "subcategories": ["Car Care", "Bike Care", "Helmets", "Tyres", "Interior"],
        "products": [
            p("Car Cover", "AutoFurnish", 1299, 2499, 4.3, "🚗", "#e3f2fd"),
            p("Bike Helmet", "Vega", 1499, 2499, 4.5, "🪖", "#e8f5e9"),
            p("Car Vacuum", "Agaro", 899, 1499, 4.2, "🧹", "#fce4ec"),
            p("Tyre Inflator", "Michelin", 2199, 3499, 4.6, "🛞", "#fff3e0"),
            p("Seat Covers", "Elegant", 2999, 4999, 4.4, "🪑", "#f3e5f5"),
            p("Dash Cam", "70mai", 4499, 6999, 4.5, "📷", "#e0f7fa"),
            p("Engine Oil 1L", "Castrol", 599, 899, 4.6, "🛢️", "#e1f0ff"),
            p("Microfiber Cloth", "3M", 299, 499, 4.4, "🧽", "#fce4ec"),
        ],
    },
    "sports": {
        "title": "Sports & Fitness",
        "icon": "🏏",
        "subcategories": ["Cricket", "Football", "Gym", "Yoga", "Cycling"],
        "products": [
            p("Cricket Bat", "SG", 2499, 3999, 4.5, "🏏", "#e3f2fd"),
            p("Football Size 5", "Nivia", 899, 1499, 4.4, "⚽", "#e8f5e9"),
            p("Dumbbell Set 20kg", "Kore", 1999, 3499, 4.6, "🏋️", "#fce4ec"),
            p("Yoga Mat 6mm", "Boldfit", 699, 1299, 4.5, "🧘", "#fff3e0"),
            p("Cycling Helmet", "Steelbird", 1499, 2499, 4.3, "🚴", "#f3e5f5"),
            p("Badminton Racket", "Yonex", 1999, 2999, 4.7, "🏸", "#e0f7fa"),
            p("Treadmill", "Fitkit", 19999, 29999, 4.4, "🏃", "#e1f0ff"),
            p("Skipping Rope", "Nivia", 299, 499, 4.4, "🪢", "#fce4ec"),
        ],
    },
    "furniture": {
        "title": "Furniture",
        "icon": "🪑",
        "subcategories": ["Sofas", "Beds", "Tables", "Chairs", "Wardrobes"],
        "products": [
            p("3-Seater Sofa", "Urban Ladder", 18999, 29999, 4.5, "🛋️", "#e3f2fd"),
            p("Queen Bed", "Wakefit", 15999, 24999, 4.6, "🛏️", "#e8f5e9"),
            p("Study Table", "Nilkamal", 4999, 7999, 4.3, "🪑", "#fce4ec"),
            p("Office Chair", "Green Soul", 7999, 12999, 4.4, "💺", "#fff3e0"),
            p("Wardrobe 3-Door", "Godrej", 21999, 32999, 4.5, "🚪", "#f3e5f5"),
            p("Coffee Table", "Home Centre", 3999, 5999, 4.2, "☕", "#e0f7fa"),
            p("Bookshelf", "Ikea", 5999, 8999, 4.6, "📚", "#e1f0ff"),
            p("Bean Bag XL", "Solimo", 1499, 2499, 4.3, "🪑", "#fce4ec"),
        ],
    },
    "books": {
        "title": "Books",
        "icon": "📚",
        "subcategories": ["Fiction", "Non-Fiction", "Academic", "Comics", "Children"],
        "products": [
            p("Atomic Habits", "James Clear", 399, 799, 4.8, "📘", "#e3f2fd"),
            p("Rich Dad Poor Dad", "Robert Kiyosaki", 299, 599, 4.6, "📗", "#e8f5e9"),
            p("The Alchemist", "Paulo Coelho", 249, 499, 4.7, "📕", "#fce4ec"),
            p("Wings of Fire", "APJ Kalam", 299, 499, 4.8, "📙", "#fff3e0"),
            p("Sapiens", "Yuval Noah", 599, 999, 4.7, "📔", "#f3e5f5"),
            p("Harry Potter Set", "JK Rowling", 2999, 4999, 4.9, "📚", "#e0f7fa"),
            p("Ikigai", "Hector Garcia", 349, 599, 4.5, "📓", "#e1f0ff"),
            p("Do Epic Shit", "Ankur Warikoo", 249, 399, 4.4, "📖", "#fce4ec"),
        ],
    },
    "2wheelers": {
        "title": "2 Wheelers",
        "icon": "🛵",
        "subcategories": ["Scooters", "Bikes", "EV", "Accessories", "Spare Parts"],
        "products": [
            p("Activa 6G", "Honda", 79999, 89999, 4.6, "🛵", "#e3f2fd"),
            p("Pulsar 150", "Bajaj", 109999, 119999, 4.5, "🏍️", "#e8f5e9"),
            p("Ather 450X EV", "Ather", 139999, 149999, 4.7, "⚡", "#fce4ec"),
            p("Jupiter 110", "TVS", 79999, 89999, 4.4, "🛵", "#fff3e0"),
            p("Classic 350", "Royal Enfield", 199999, 209999, 4.8, "🏍️", "#f3e5f5"),
            p("Bike Cover", "AutoFurnish", 599, 999, 4.2, "🛡️", "#e0f7fa"),
            p("Riding Gloves", "Rynox", 1499, 2499, 4.5, "🧤", "#e1f0ff"),
            p("Engine Oil 1L", "Motul", 699, 999, 4.6, "🛢️", "#fce4ec"),
        ],
    },
}

# Build a flat list of all products for search
ALL_PRODUCTS = []
for slug, cat in CATEGORY_DATA.items():
    for prod in cat["products"]:
        prod_copy = dict(prod)
        prod_copy["category"] = cat["title"]
        prod_copy["category_slug"] = slug
        ALL_PRODUCTS.append(prod_copy)


# ------------------------------------------------------------------
# ROUTES
# ------------------------------------------------------------------

@app.route("/")
def home():
    """Homepage — 'For You' view with banners + carousels."""
    top_deals = [
        {"name": "Phone (4b)",     "price": "25,999", "img": "📱", "bg": "#e1f0ff"},
        {"name": "moto watch",     "price": "3,999",  "img": "⌚", "bg": "#fce4ec"},
        {"name": '43" smart TVs',  "price": "19,499", "img": "📺", "bg": "#e8f5e9"},
        {"name": "Galaxy S25",     "price": "54,299", "img": "📱", "bg": "#e3f2fd"},
        {"name": "AGARO devices",  "price": "859",    "img": "💇", "bg": "#f3e5f5"},
        {"name": '32" Smart TVs',  "price": "8,121",  "img": "📺", "bg": "#fff3e0"},
        {"name": "Lifelong m...",  "price": "1,499",  "img": "🪑", "bg": "#e0f7fa"},
    ]
    bestsellers = [
        {"name": "Laptop",     "price": "35,990", "img": "💻", "bg": "#fce4ec"},
        {"name": "LG TV",      "price": "22,499", "img": "📺", "bg": "#e8f5e9"},
        {"name": "Cushion",    "price": "399",    "img": "🛋️", "bg": "#e3f2fd"},
        {"name": "Perfume",    "price": "899",    "img": "🧴", "bg": "#f3e5f5"},
        {"name": "Kitchen",    "price": "1,299",  "img": "🍳", "bg": "#fff3e0"},
        {"name": "Smartphone", "price": "12,999", "img": "📱", "bg": "#e0f7fa"},
        {"name": "iQOO",       "price": "18,999", "img": "📱", "bg": "#e1f0ff"},
    ]
    return render_template(
        "index.html",
        top_deals=top_deals,
        bestsellers=bestsellers,
        categories=CATEGORY_DATA,
        active="foryou",
    )


@app.route("/category/<slug>")
def category(slug):
    """Category listing page (Fashion, Mobiles, Beauty, etc.)."""
    cat = CATEGORY_DATA.get(slug)
    if not cat:
        abort(404)
    return render_template(
        "category.html",
        slug=slug,
        category=cat,
        categories=CATEGORY_DATA,
        active=slug,
    )


@app.route("/search")
def search():
    """Search across all products."""
    q = request.args.get("q", "").strip().lower()
    results = []
    if q:
        results = [
            prod for prod in ALL_PRODUCTS
            if q in prod["name"].lower() or q in prod["brand"].lower()
        ]
    return render_template(
        "search.html",
        query=q,
        results=results,
        categories=CATEGORY_DATA,
        active="search",
    )


@app.errorhandler(404)
def not_found(e):
    return render_template(
        "search.html",
        query="",
        results=[],
        categories=CATEGORY_DATA,
        active="404",
        message="Page not found 😕",
    ), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
