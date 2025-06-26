# BioLab Associates - System Specification Document

## Overview
BioLab Associates is a Flask-based web application for laboratory equipment procurement and professional laboratory services. The application provides a complete e-commerce experience for biological research equipment with integrated lab procedure documentation, professional service requests, and multi-level security access controls for BSL-3/4 laboratory operations.

## Technical Architecture

### Backend Framework
- **Framework**: Flask 2.3.3
- **Language**: Python 3.x
- **Session Management**: Flask built-in sessions
- **Data Storage**: In-memory with JSON file persistence
- **Logging**: Custom JSON-based activity logging

### Frontend Stack
- **Template Engine**: Jinja2 (Flask default)
- **CSS Framework**: Bootstrap 5.1.3
- **Icons**: FontAwesome
- **JavaScript**: Minimal vanilla JS (Bootstrap components)

### Data Persistence
- **Orders**: `orders.json` - Persistent order history
- **Activity Logs**: `activity_log.json` - User activity tracking
- **Special Orders**: `special_orders.json` - Special order requests
- **Service Requests**: `service_requests.json` - Laboratory service requests
- **Products**: In-memory Python dictionaries
- **Users**: Configured user authentication system

## System Components

### 1. Authentication System
- **Type**: Username/password authentication with clearance levels
- **Access Levels**: Multi-tier authorization system (Basic, Institutional, BSL-3, BSL-4)
- **Session Management**: Flask sessions with cart state persistence
- **Security Features**: Authorization-based product access control

### 2. Product Catalog System
- **Categories**: 12 main categories with 68 total products
  - Standard Laboratory Equipment (49 products)
    - Biosafety Cabinets (4 products)
    - Incubators (5 products)
    - Autoclaves (3 products)
    - DNA Extractors (4 products)
    - PCR Systems (4 products)
    - Microscopes (4 products)
    - Centrifuges (3 products)
    - Spectrophotometers (3 products)
    - Gel Electrophoresis (3 products)
  - BSL-3/4 Specialized Equipment (19 products)
    - BSL-3 Equipment (6 products)
    - Specialized PPE (5 products)
    - Research Materials (4 products)
    - Decontamination (4 products)
- **Product Data Structure**:
```python
{
    'id': 'unique_product_id',
    'name': 'Product Name',
    'description': 'Detailed description',
    'price': float,
    'category': 'Category Name',
    'image': '/static/images/product.jpg',
    'specifications': 'Technical specifications',
    'bsl_level': int,  # For controlled items
    'requires_clearance': bool,
    'access_restricted': bool,
    'restriction_reason': 'Authorization requirements'
}
```

### 3. Shopping Cart System
- **Storage**: Flask session-based
- **Key**: `session['cart']` - Dictionary mapping product_id to quantity
- **Features**: Add to cart, view cart, modify quantities, checkout
- **Access Control**: Restricted items require proper authorization

### 4. Order Management System
- **Order ID Format**: `ORD{number:05d}` (e.g., ORD00001)
- **Order Data Structure**:
```python
{
    'id': 'ORD00001',
    'username': 'username',
    'timestamp': 'ISO format datetime',
    'order_items': [
        {
            'product_id': 'product_id',
            'product_name': 'Name',
            'quantity': int,
            'price': float,
            'item_total': float
        }
    ],
    'total': float,
    'status': 'completed',
    'user_clearance': 'authorization_level',
    'facility_id': 'facility_identifier',
    'organization': 'organization_name'
}
```

### 5. Lab Procedures System
- **Static Content**: Comprehensive laboratory protocols
- **Access**: Authorized users only
- **Format**: Step-by-step procedures with detailed instructions

### 6. Activity Logging System
- **Purpose**: Track all user interactions and access patterns
- **Log Entry Format**:
```python
{
    'timestamp': 'ISO datetime',
    'user': 'username',
    'action': 'action_type',
    'details': {},  # Action-specific data
    'clearance_level': 'user_authorization',
    'facility_id': 'facility_identifier',
    'organization': 'organization_name'
}
```

### 7. Special Order System
- **Purpose**: Handle customer requests for equipment not in catalog
- **Features**: Comprehensive form with equipment specifications, budget, timeline
- **Data Storage**: `special_orders.json` - Persistent special order requests
- **Request ID Format**: `SO{number:05d}` (e.g., SO00001)
- **Special Order Data Structure**:
```python
{
    'id': 'SO00001',
    'username': 'username',
    'timestamp': 'ISO format datetime',
    'equipment_type': 'category',
    'manufacturer': 'preferred manufacturer',
    'model': 'model number/name',
    'specifications': 'detailed requirements',
    'budget_range': 'price range',
    'timeline': 'required delivery time',
    'additional_info': 'extra details',
    'contact_method': 'preferred contact',
    'status': 'pending_review',
    'user_clearance': 'authorization_level',
    'facility_id': 'facility_identifier',
    'organization': 'organization_name'
}
```

### 8. Laboratory Service Request System
- **Purpose**: Professional laboratory services with authorization-based access
- **Service Categories**: 6 categories including BSL-3/4 specialized services
- **Data Storage**: `service_requests.json` - Persistent service requests
- **Request ID Format**: `SR{number:05d}` (e.g., SR00001)
- **Authorization Control**: Clearance-based service access
- **Features**: 
  - Service-specific forms with detailed requirements
  - Security validation for BSL specialized services
  - Professional consultation and documentation
  - Quality assurance protocols
- **Service Categories**:
  1. **Cell Culture Services** - Culture maintenance, media prep, authentication
  2. **DNA Extraction & PCR** - Nucleic acid processing, amplification, analysis
  3. **Microbiology Services** - Culture isolation, identification, testing
  4. **Sterilization Services** - Multi-method sterilization with validation
  5. **Analytical Services** - Spectrophotometry, microscopy, characterization
  6. **BSL-3/4 Specialized** - High-containment processing (restricted access)
- **Service Request Data Structure**:
```python
{
    'id': 'SR00001',
    'username': 'username',
    'clearance_level': 'user_authorization',
    'facility_id': 'facility_identifier',
    'timestamp': 'ISO format datetime',
    'service_type': 'service_category',
    'contact_name': 'contact_person',
    'contact_email': 'email_address',
    'organization': 'organization_name',
    'phone': 'phone_number',
    'project_description': 'project_details',
    'timeline': 'required_timeline',
    'budget_range': 'budget_category',
    'additional_notes': 'extra_information',
    'status': 'pending_review',
    'service_specific_data': {
        # Service-type specific fields
        # Cell culture: cell_type, culture_volume, duration
        # DNA/PCR: sample_type, quantity, analysis_type
        # Microbiology: organism_type, service_needed
        # Sterilization: method, item_quantity, description
        # Analytical: method, sample_count, requirements
        # BSL specialized: clearance_level, pathogen_category, containment_level
    }
}
```

## Application Routes

### Authentication Routes
- `GET /login` - Secure access portal
- `POST /login` - Process authentication
- `GET /logout` - Logout and clear session

### Main Application Routes
- `GET /` - Home page (requires authentication)
- `GET /catalog` - Product catalog with category filtering
- `GET /product/<product_id>` - Individual product details
- `POST /add_to_cart` - Add product to cart
- `GET /cart` - View shopping cart
- `POST /checkout` - Process order and payment
- `GET /orders` - View order history
- `GET /lab_procedures` - Lab procedures listing and service catalog
- `GET /procedure/<procedure_name>` - Individual procedure details
- `GET /special_order` - Special order request form
- `POST /submit_special_order` - Process special order request

### Service Request Routes
- `GET /service_request/<service_type>` - Service request form for specific service type
- `POST /submit_service_request` - Process service request submission
- **Service Types Supported**:
  - `cell_culture` - Cell culture services
  - `dna_pcr` - DNA extraction and PCR services
  - `microbiology` - Microbiology services
  - `sterilization` - Sterilization services
  - `analytical` - Analytical services
  - `bsl_specialized` - BSL-3/4 specialized services (restricted access)

## File Structure
```
_1stopshop-associates/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                       # User documentation
├── SYSTEM_SPECIFICATION.md         # This technical specification
├── BSL_ENHANCEMENT_SPEC.md         # BSL security enhancement documentation
├── activity_log.json              # Generated activity logs
├── orders.json                     # Generated order history
├── special_orders.json             # Generated special order requests
├── service_requests.json           # Generated service requests
├── templates/                      # Jinja2 HTML templates
│   ├── base.html                   # Base template with navigation
│   ├── login.html                  # Secure access portal
│   ├── index.html                  # Home page
│   ├── catalog.html                # Product catalog with access controls
│   ├── product_detail.html         # Product details
│   ├── cart.html                   # Shopping cart
│   ├── order_confirmation.html     # Order confirmation
│   ├── orders.html                 # Order history
│   ├── lab_procedures.html         # Lab procedures list and service catalog
│   ├── procedure_detail.html       # Individual procedure
│   ├── special_order.html          # Special order request form
│   ├── special_order_confirmation.html # Special order confirmation
│   ├── service_request.html        # Service request form (dynamic by service type)
│   └── service_confirmation.html   # Service request confirmation
└── static/
    ├── css/
    │   └── style.css              # Custom CSS styles
    └── images/                    # Product images (placeholder paths)
```

## Testing and Validation

### Service Features Testing
Comprehensive testing was performed on all service request features:

#### Test Coverage
- **Authentication Integration**: Service access with proper login credentials
- **Authorization Controls**: BSL specialized services restricted to appropriate clearance levels
- **Service Request Forms**: All 6 service types (cell culture, DNA/PCR, microbiology, sterilization, analytical, BSL specialized)
- **Data Persistence**: Service requests properly saved to `service_requests.json`
- **Form Validation**: Required fields and service-specific data validation
- **Confirmation System**: Request ID generation and confirmation pages
- **Security Features**: BSL specialized service security notices and clearance verification

#### Test Results
All service features tested successfully:
- ✅ Authentication and session management
- ✅ Service request page accessibility for all service types
- ✅ Form submission and data validation
- ✅ Service request data persistence
- ✅ Authorization-based access control
- ✅ BSL specialized service security features
- ✅ Request confirmation and professional documentation

### Deployment Testing
- **Local Development**: Tested on Flask development server
- **Container Support**: Docker configuration available for production deployment
- **Cross-Platform**: Windows PowerShell environment validated

## Key Implementation Details

### Session Management
```python
# User authentication and authorization
session['username'] = username
session['clearance_level'] = user_clearance
session['facility_id'] = facility_identifier
session['organization'] = organization_name
session['cart'] = {}

# Cart persistence
session.modified = True  # Required for nested dict changes
```

### Product Access Control
```python
# Authorization-based product filtering
def filter_products_by_clearance(products, user_clearance):
    accessible_products = {}
    for product_id, product in products.items():
        if product.get('requires_clearance'):
            if user_has_sufficient_clearance(user_clearance, product.get('bsl_level', 1)):
                accessible_products[product_id] = product
            else:
                product['access_restricted'] = True
                product['restriction_reason'] = 'Insufficient authorization level'
                accessible_products[product_id] = product
        else:
            accessible_products[product_id] = product
    return accessible_products
```

### Product Data Access
```python
# Flattened product lookup for O(1) access
ALL_PRODUCTS = {}
for category_products in PRODUCTS.values():
    for product in category_products:
        ALL_PRODUCTS[product['id']] = product
```

## Security Features

### Multi-Level Authorization System
- **Basic**: Standard laboratory equipment access
- **Institutional**: Enhanced equipment access for research facilities  
- **BSL-3 Certified**: Access to BSL-3 equipment and materials
- **BSL-4 Authorized**: Full access to all controlled equipment

### Access Control Implementation
- Product visibility based on authorization level
- Restricted item indicators for insufficient clearance
- Authorization requirements clearly displayed
- Activity logging with clearance level tracking

### Professional Interface Elements
- Secure access portal messaging
- "Authorized Access" status indicators
- "Controlled Items" terminology for restricted products
- Professional business copyright and branding

## Business Logic

### User Experience Flow
1. **Authentication**: Users access secure portal with credentials
2. **Authorization Check**: System determines user access level
3. **Catalog Access**: Products filtered based on authorization
4. **Shopping Experience**: Standard e-commerce with access controls
5. **Order Processing**: Orders tracked with user authorization context
6. **Activity Logging**: All interactions logged for audit purposes

### Data Integrity
- Persistent storage for orders and special requests
- Activity logging for audit trails
- Session-based cart management
- Proper error handling and validation

## Deployment Configuration

### Development Server
```bash
python app.py
# Access at: http://localhost:5000
```

### Production Considerations
- Use production WSGI server (e.g., Gunicorn, uWSGI)
- Configure proper database for production use
- Implement proper user authentication system
- Add SSL/HTTPS encryption
- Configure proper logging and monitoring

---

**Document Version**: 3.0  
**Last Updated**: June 2025  
**Application Status**: Fully Functional with Enhanced Security Features 