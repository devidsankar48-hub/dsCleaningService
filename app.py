import os
from flask import Flask, render_template, request, flash, redirect, url_for, session, Response
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)
app.secret_key = 'ds-house-cleaning-service-2024'

# --- Cloudinary Configuration ---
cloudinary.config(
    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME", "uo6e0lqa"),
    api_key = os.environ.get("CLOUDINARY_API_KEY", "816811886594347"),
    api_secret = os.environ.get("CLOUDINARY_API_SECRET") # MUST BE SET IN RENDER!
)

# --- Admin Configuration ---
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin")  # Reads from Render env var, defaults to 'admin' locally
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Business Configuration
BUSINESS = {
    'name': 'D.S. House Cleaning Service',
    'owner': 'Y. Sankar',
    'tagline': 'Professional Cleaning Services in Tirupati',
    'description': (
        'Trusted House Cleaning, Painting, Water Tank Cleaning, '
        'Office Cleaning and House Shifting Services in Tirupati. '
        'Affordable Pricing. Trained Staff. Same Day Service Available.'
    ),
    'phone1': '9505946310',
    'phone2': '9618148435',
    'whatsapp': '919505946310',
    'address': (
        'Korlagunta Main Rd, Korlagunta, Kothapalli, '
        'Subash Nagar, Tirupati, Andhra Pradesh 517501'
    ),
    'map_query': 'Korlagunta+Main+Rd,+Korlagunta,+Tirupati,+Andhra+Pradesh+517501',
    'services': [
        {
            'id': 'painting',
            'name': 'Painting Services',
            'description': 'Professional interior and exterior painting services. '
                           'Transform your home with expert color consultation and flawless finish.',
            'icon': 'fa-solid fa-paint-roller'
        },
        {
            'id': 'bathroom',
            'name': 'Bathroom Cleaning',
            'description': 'Deep cleaning for bathrooms including tiles, fixtures, '
                           'and hard water stain removal. Sparkling results guaranteed.',
            'icon': 'fa-solid fa-shower'
        },
        {
            'id': 'kitchen',
            'name': 'Kitchen Cleaning',
            'description': 'Thorough kitchen cleaning covering countertops, chimney, '
                           'cabinets, and grease removal. A hygienic kitchen for your family.',
            'icon': 'fa-solid fa-utensils'
        },
        {
            'id': 'window-fan',
            'name': 'Window & Fan Cleaning',
            'description': 'Complete cleaning of windows, glass panels, ceiling fans, '
                           'and exhaust fans. Crystal clear views and fresh air.',
            'icon': 'fa-solid fa-wind'
        },
        {
            'id': 'water-tank',
            'name': 'Water Tank Cleaning',
            'description': 'Professional water tank and sump cleaning with anti-bacterial '
                           'treatment. Ensure safe and clean drinking water for your family.',
            'icon': 'fa-solid fa-droplet'
        },
        {
            'id': 'office',
            'name': 'Office Cleaning',
            'description': 'Complete office and commercial space cleaning services. '
                           'Maintain a clean and productive work environment.',
            'icon': 'fa-solid fa-building'
        },
        {
            'id': 'house-shifting',
            'name': 'House Shifting',
            'description': 'Reliable and careful house shifting and relocation services. '
                           'Safe packing, transport, and unpacking of your belongings.',
            'icon': 'fa-solid fa-truck-moving'
        },
        {
            'id': 'deep-cleaning',
            'name': 'Deep Cleaning',
            'description': 'Complete deep cleaning of your entire home from floor to ceiling. '
                           'Perfect for festivals, move-in, or periodic maintenance.',
            'icon': 'fa-solid fa-broom'
        },
    ],
    'trust_signals': [
        {'icon': 'fa-solid fa-star', 'text': 'Trusted by Families'},
        {'icon': 'fa-solid fa-circle-check', 'text': 'Same Day Service'},
        {'icon': 'fa-solid fa-circle-check', 'text': 'Affordable Pricing'},
        {'icon': 'fa-solid fa-circle-check', 'text': 'Trained Professionals'},
        {'icon': 'fa-solid fa-circle-check', 'text': '100% Satisfaction'},
    ],
    'why_choose_us': [
        {'icon': 'fa-solid fa-user-shield', 'title': 'Trained & Verified Staff', 'desc': 'Background-verified, skilled cleaning professionals you can trust.'},
        {'icon': 'fa-solid fa-tags', 'title': 'Affordable Pricing', 'desc': 'Best-in-class service at prices that fit your budget.'},
        {'icon': 'fa-solid fa-leaf', 'title': 'Eco-Friendly Products', 'desc': 'Safe, non-toxic cleaning products for your family and pets.'},
        {'icon': 'fa-solid fa-screwdriver-wrench', 'title': 'Modern Equipment', 'desc': 'Latest cleaning machines and tools for superior results.'},
        {'icon': 'fa-solid fa-bolt', 'title': 'Same Day Service', 'desc': 'Book today, get it done today. Quick and reliable service.'},
        {'icon': 'fa-solid fa-handshake', 'title': '100% Satisfaction', 'desc': 'We don\'t stop until you\'re completely happy with the results.'},
    ],
    'areas': [
        'Tirupati', 'Korlagunta', 'Maruthi Nagar', 'Subash Nagar',
        'Kothapalli', 'Renigunta', 'Tiruchanoor', 'MR Palli', 'LB Nagar',
    ]
}

# --- Reviews Database (In-Memory) ---
# Note: In a production environment on Render, this will reset on restart. 
# A real database (like MongoDB or Supabase) should be added later for permanence.
from datetime import datetime

REVIEWS = [
    {'name': 'King', 'date': '01 Aug 2026', 'rating': 5, 'text': 'I recently used D S House Cleaning Services for my new house deep cleaning, and old house restroom maintenance. I am very happy with their work! The team was so humble, fast and efficient, getting everything done in no time.'},
    {'name': 'Prasanna', 'date': '18 Aug 2026', 'rating': 5, 'text': 'I had a great experience with D S House Cleaning Services! They did an excellent job cleaning my home. The team was friendly and worked very hard. My house looks amazing now! I will definitely call them again.'},
    {'name': 'Divya', 'date': '16 Apr', 'rating': 5, 'text': 'D S House Cleaning Services is amazing! They do an excellent job cleaning my home. The staff is friendly and always on time. My house looks great after they finish. They pay attention to every detail.'},
    {'name': 'Sbfc Gym', 'date': '14 Aug', 'rating': 4, 'text': 'I recently hired D S House Cleaning Services for a thorough cleaning of my home, and I couldn`t be more satisfied! Their team displayed exceptional professionalism and attention to detail. Highly recommend!'},
    {'name': 'GNANA Prakash Reddy', 'date': '14 Aug', 'rating': 5, 'text': 'They provided excellent service and did a very good job. The prices were reasonable, so I felt it was fair. There were no hidden costs.'},
    {'name': 'Monisha', 'date': '17 Jun', 'rating': 4, 'text': 'The team is friendly and works fast. My home looks so clean and fresh after they visit. I highly recommend their services to anyone.'},
    {'name': 'Deeksha', 'date': '29 Dec', 'rating': 5, 'text': 'My home looks amazing and feels so fresh. They arrived on time and finished quickly without rushing. Excellent service all around!'}
]

def get_rating_stats():
    if not REVIEWS:
        return "0.0", 0
    avg = sum(r['rating'] for r in REVIEWS) / len(REVIEWS)
    return f"{avg:.1f}", len(REVIEWS)

# --- Cloudinary In-Memory Cache ---
cloudinary_cache = None

def get_services_with_images():
    """Helper to dynamically inject the list of images from Cloudinary."""
    global cloudinary_cache
    
    # Refresh cache if empty (runs on boot or after an upload/delete)
    if cloudinary_cache is None:
        cloudinary_cache = {s['id']: [] for s in BUSINESS['services']}
        try:
            # Fetch all resources in the 'services/' folder
            if os.environ.get("CLOUDINARY_API_SECRET"):
                response = cloudinary.api.resources(type="upload", prefix="services/", max_results=500)
                for res in response.get('resources', []):
                    public_id = res['public_id']  # e.g., 'services/painting/xyz123'
                    parts = public_id.split('/')
                    if len(parts) >= 3:
                        service_id = parts[1]
                        if service_id in cloudinary_cache:
                            cloudinary_cache[service_id].append({
                                'url': res['secure_url'],
                                'public_id': public_id
                            })
        except Exception as e:
            print("Cloudinary fetch error:", e)

    # Attach cached images to services
    services = []
    for s in BUSINESS['services']:
        service_copy = dict(s)
        service_copy['images'] = cloudinary_cache.get(s['id'], [])
        services.append(service_copy)
    return services

@app.route('/')
def index():
    """Render the main single-page website."""
    context = dict(BUSINESS)
    context['services'] = get_services_with_images()
    
    avg_rating, total_reviews = get_rating_stats()
    context['rating'] = avg_rating
    context['review_count'] = total_reviews
    
    # Show only the first 5 reviews on the homepage for the horizontal scroll
    context['reviews'] = REVIEWS[:5]
    
    return render_template('index.html', biz=context)

@app.route('/submit_review', methods=['POST'])
def submit_review():
    name = request.form.get('name', 'Anonymous').strip()
    text = request.form.get('text', '').strip()
    try:
        rating = int(request.form.get('rating', 5))
    except ValueError:
        rating = 5

    if name and text:
        date_str = datetime.now().strftime("%d %b %Y")
        REVIEWS.insert(0, {
            'name': name,
            'date': date_str,
            'rating': rating,
            'text': text
        })
        flash('Thank you for your review! It has been posted successfully.', 'success')
    else:
        flash('Please provide both your name and review text.', 'error')
        
    return redirect(url_for('index') + '#reviews')

@app.route('/reviews')
def all_reviews():
    """Render a dedicated page for all reviews."""
    context = dict(BUSINESS)
    avg_rating, total_reviews = get_rating_stats()
    context['rating'] = avg_rating
    context['review_count'] = total_reviews
    context['reviews'] = REVIEWS
    
    return render_template('reviews.html', biz=context)

# --- SEO Routes ---
@app.route('/robots.txt')
def robots():
    lines = [
        "User-agent: *",
        "Allow: /",
        "Sitemap: https://dshousecleaningservice.onrender.com/sitemap.xml"
    ]
    return Response("\n".join(lines), mimetype="text/plain")

@app.route('/sitemap.xml')
def sitemap():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>https://dshousecleaningservice.onrender.com/</loc>
            <changefreq>weekly</changefreq>
            <priority>1.0</priority>
        </url>
    </urlset>"""
    return Response(xml, mimetype="application/xml")

# --- Admin Routes ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Invalid password', 'error')
    return render_template('admin_login.html', biz=BUSINESS)

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
        
    global cloudinary_cache

    if request.method == 'POST':
        if not os.environ.get("CLOUDINARY_API_SECRET"):
            flash("Cloudinary API Secret is missing! Set it in Render Environment Variables.", "error")
            return redirect(url_for('admin'))

        service_id = request.form.get('service_id')
        if 'image' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
            
        files = request.files.getlist('image')
        uploaded_count = 0
        
        for file in files:
            if file and file.filename and allowed_file(file.filename):
                try:
                    # Upload directly to Cloudinary folder e.g., 'services/painting/'
                    cloudinary.uploader.upload(file, folder=f"services/{service_id}/")
                    uploaded_count += 1
                except Exception as e:
                    print("Upload error:", e)
                
        if uploaded_count > 0:
            flash(f'Successfully uploaded {uploaded_count} image(s) for {service_id}', 'success')
            cloudinary_cache = None  # Invalidate cache to force a refresh!
        else:
            flash('No valid images uploaded', 'error')
            
        return redirect(url_for('admin'))

    context = dict(BUSINESS)
    context['services'] = get_services_with_images()
    return render_template('admin.html', biz=context)

@app.route('/admin/delete', methods=['POST'])
def delete_image():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
        
    global cloudinary_cache
    public_id = request.form.get('public_id')

    if public_id:
        try:
            cloudinary.uploader.destroy(public_id)
            flash('Image deleted successfully', 'success')
            cloudinary_cache = None  # Invalidate cache
        except Exception as e:
            flash(f'Failed to delete image: {e}', 'error')
            
    return redirect(url_for('admin'))


@app.route('/contact', methods=['POST'])
def contact():
    """Handle contact form submission."""
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    service = request.form.get('service', '').strip()
    message = request.form.get('message', '').strip()

    if name and phone:
        # In production, this would send an email or save to a database
        flash(
            f'Thank you, {name}! We received your enquiry for "{service}". '
            f'We will call you back at {phone} shortly.',
            'success',
        )
    else:
        flash('Please provide your name and phone number.', 'error')

    return redirect(url_for('index') + '#contact')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
