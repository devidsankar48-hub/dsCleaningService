from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'ds-house-cleaning-service-2024'

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
            'name': 'Painting Services',
            'description': 'Professional interior and exterior painting services. '
                           'Transform your home with expert color consultation and flawless finish.',
            'icon': 'fa-solid fa-paint-roller',
            'image': 'painting-service.jpg',
        },
        {
            'name': 'Bathroom Cleaning',
            'description': 'Deep cleaning for bathrooms including tiles, fixtures, '
                           'and hard water stain removal. Sparkling results guaranteed.',
            'icon': 'fa-solid fa-shower',
            'image': 'bathroom-cleaning.jpg',
        },
        {
            'name': 'Kitchen Cleaning',
            'description': 'Thorough kitchen cleaning covering countertops, chimney, '
                           'cabinets, and grease removal. A hygienic kitchen for your family.',
            'icon': 'fa-solid fa-utensils',
            'image': 'kitchen-cleaning.jpg',
        },
        {
            'name': 'Window & Fan Cleaning',
            'description': 'Complete cleaning of windows, glass panels, ceiling fans, '
                           'and exhaust fans. Crystal clear views and fresh air.',
            'icon': 'fa-solid fa-wind',
            'image': 'window-fan-cleaning.jpg',
        },
        {
            'name': 'Water Tank Cleaning',
            'description': 'Professional water tank and sump cleaning with anti-bacterial '
                           'treatment. Ensure safe and clean drinking water for your family.',
            'icon': 'fa-solid fa-droplet',
            'image': 'water-tank-cleaning.jpg',
        },
        {
            'name': 'Office Cleaning',
            'description': 'Complete office and commercial space cleaning services. '
                           'Maintain a clean and productive work environment.',
            'icon': 'fa-solid fa-building',
            'image': 'office-cleaning.jpg',
        },
        {
            'name': 'House Shifting',
            'description': 'Reliable and careful house shifting and relocation services. '
                           'Safe packing, transport, and unpacking of your belongings.',
            'icon': 'fa-solid fa-truck-moving',
            'image': 'house-shifting.jpg',
        },
        {
            'name': 'Deep Cleaning',
            'description': 'Complete deep cleaning of your entire home from floor to ceiling. '
                           'Perfect for festivals, move-in, or periodic maintenance.',
            'icon': 'fa-solid fa-broom',
            'image': 'deep-cleaning.jpg',
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


@app.route('/')
def index():
    """Render the main single-page website."""
    return render_template('index.html', biz=BUSINESS)


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
