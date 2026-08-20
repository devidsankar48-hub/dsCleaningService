import os
from flask import Flask, render_template, request, flash, redirect, url_for, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'ds-house-cleaning-service-2024'

# --- Admin Configuration ---
ADMIN_PASSWORD = "admin"  # Simple hardcoded password for now
UPLOAD_FOLDER = os.path.join('static', 'images', 'services')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    ],
}

def get_services_with_images():
    """Helper to dynamically inject the list of images into each service."""
    services = []
    for s in BUSINESS['services']:
        service_copy = dict(s)
        service_dir = os.path.join(app.config['UPLOAD_FOLDER'], s['id'])
        images = []
        if os.path.exists(service_dir):
            images = [f for f in os.listdir(service_dir) if allowed_file(f)]
            images.sort()
        service_copy['images'] = images
        services.append(service_copy)
    return services

@app.route('/')
def index():
    """Render the main single-page website."""
    # Create a fresh copy of BUSINESS with dynamic images
    context = dict(BUSINESS)
    context['services'] = get_services_with_images()
    return render_template('index.html', biz=context)

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
        
    context = dict(BUSINESS)
    context['services'] = get_services_with_images()

    if request.method == 'POST':
        service_id = request.form.get('service_id')
        if 'image' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
            
        files = request.files.getlist('image')
        service_dir = os.path.join(app.config['UPLOAD_FOLDER'], service_id)
        
        # Ensure directory exists
        os.makedirs(service_dir, exist_ok=True)
        
        uploaded_count = 0
        for file in files:
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                
                # Check if it already exists, append random/number if needed (simplified here)
                file_path = os.path.join(service_dir, filename)
                counter = 1
                while os.path.exists(file_path):
                    name, ext = os.path.splitext(filename)
                    file_path = os.path.join(service_dir, f"{name}_{counter}{ext}")
                    counter += 1
                    
                file.save(file_path)
                uploaded_count += 1
                
        if uploaded_count > 0:
            flash(f'Successfully uploaded {uploaded_count} image(s) for {service_id}', 'success')
        else:
            flash('No valid images uploaded', 'error')
            
        return redirect(url_for('admin'))

    return render_template('admin.html', biz=context)

@app.route('/admin/delete/<service_id>/<filename>', methods=['POST'])
def delete_image(service_id, filename):
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
        
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(service_id), secure_filename(filename))
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f'Deleted image {filename}', 'success')
    else:
        flash('File not found', 'error')
        
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
