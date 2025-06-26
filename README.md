# BioLab Associates - Laboratory Equipment Supplier

A Flask-based web application for biological equipment ordering and procurement management.

## Features

- **User Authentication**: Secure login system with multi-level authorization
- **Product Catalog**: Comprehensive biological equipment from multiple categories:
  - Biosafety Cabinets
  - Incubators & Shakers
  - Autoclaves
  - DNA Extractors
  - PCR Systems
  - Microscopes
  - Centrifuges
  - Spectrophotometers
  - Gel Electrophoresis
  - BSL-3/4 Specialized Equipment
  - Specialized PPE
  - Research Materials
  - Decontamination Equipment
- **Shopping Cart**: Add products to cart and checkout
- **Order Management**: View order history and track purchases
- **Lab Procedures**: Step-by-step laboratory protocols
- **Special Order System**: Request equipment not in standard catalog
- **Activity Logging**: All user actions are logged for audit purposes

## Quick Start

Choose either deployment method below:

### Method 1: Direct Python Execution (Recommended for Development)

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Access the Application**:
   - Open your browser and go to `http://localhost:5000`
   - You'll see the secure access portal

### Method 2: Docker Deployment (Recommended for Production/Distribution)

1. **Prerequisites**:
   - Docker Desktop installed and running
   - No additional Python installation required

2. **Build and Run with Docker Compose** (Easiest):
   ```bash
   docker-compose up --build
   ```

3. **Or Build and Run Manually**:
   ```bash
   # Build the Docker image
   docker build -t biolab-associates .
   
   # Run the container
   docker run -p 5000:5000 -v ./data:/app/data biolab-associates
   ```

4. **Access the Application**:
   - Open your browser and go to `http://localhost:5000`
   - All data is persisted in the `./data` directory

### Test Credentials

Access the secure portal with these test accounts:

| Username | Password | Clearance Level | Max Order | Access |
|----------|----------|----------------|-----------|---------|
| `admin` | `biolab123` | BSL-4 Authorized | $1,000,000 | Full access to all equipment and services |
| `researcher` | `research456` | BSL-3 Certified | $250,000 | Access to BSL-3 equipment and standard services |
| `student` | `student789` | Basic | $5,000 | Educational access to standard equipment only |

## System Architecture

### Multi-Level Authorization
- **Basic**: Standard laboratory equipment access
- **Institutional**: Enhanced equipment for research facilities
- **BSL-3 Certified**: Access to BSL-3 equipment and materials
- **BSL-4 Authorized**: Full access to all controlled equipment

### Security Features
- Authorization-based product access
- Controlled item indicators
- Professional secure access portal
- Comprehensive audit logging
- Session management and tracking

## Usage

1. **Authentication**: Access the secure portal with authorized credentials
2. **Browse Catalog**: View products by category or browse all items
3. **Add to Cart**: Select products and add them to your shopping cart
4. **Checkout**: Complete orders with secure payment processing
5. **View Orders**: Check your order history and tracking
6. **Lab Procedures**: Access step-by-step laboratory protocols
7. **Special Orders**: Request specialized equipment not in catalog

## File Structure

```
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── SYSTEM_SPECIFICATION.md # Technical documentation
├── BSL_ENHANCEMENT_SPEC.md # Security enhancement documentation
├── templates/            # HTML templates
│   ├── base.html
│   ├── login.html        # Secure access portal
│   ├── index.html
│   ├── catalog.html      # Product catalog with access controls
│   ├── product_detail.html
│   ├── cart.html
│   ├── order_confirmation.html
│   ├── orders.html
│   ├── lab_procedures.html
│   ├── procedure_detail.html
│   ├── special_order.html
│   └── special_order_confirmation.html
├── static/
│   └── css/
│       └── style.css     # Custom CSS styles
├── activity_log.json     # User activity log (generated)
├── orders.json          # Order history (generated)
└── special_orders.json  # Special order requests (generated)
```

## Data Management

The application automatically manages:
- User authentication and authorization
- Product access control based on authorization level
- Order processing and tracking
- Special order request handling
- All activity is saved to `activity_log.json`
- Orders are saved to `orders.json`
- Special orders are saved to `special_orders.json`

## Product Categories

### Standard Laboratory Equipment
- **Biosafety Cabinets**: Class II biological safety cabinets with HEPA filtration
- **Incubators**: Precision incubators and shakers for cell culture applications
- **Autoclaves**: Steam sterilizers for laboratory decontamination
- **DNA Extractors**: Automated nucleic acid purification systems
- **PCR Systems**: Thermal cyclers and real-time PCR systems
- **Microscopes**: Advanced imaging systems from leading manufacturers
- **Centrifuges**: High-speed and ultracentrifuge systems
- **Spectrophotometers**: UV-Vis and advanced analytical instruments
- **Gel Electrophoresis**: Electrophoresis systems and accessories

### BSL-3/4 Specialized Equipment
- **BSL-3 Equipment**: Class III biosafety cabinets, pressure suit systems, HEPA filtration
- **Specialized PPE**: PAPR respirators, chemical suits, protective equipment
- **Research Materials**: Controlled biological materials and research substrates
- **Decontamination**: VHP generators, sporicidal agents, UV systems

## Lab Procedures Available

- Cell Culture Protocols
- DNA Extraction Procedures
- PCR Setup and Operation
- Autoclave Operation Guidelines
- Biosafety Cabinet Use
- Sample Processing Protocols
- Equipment Maintenance Procedures
- And many more...

## Security and Compliance

- **Authorization Control**: Multi-level access control system
- **Audit Logging**: Comprehensive activity tracking
- **Secure Processing**: Industry-standard transaction security
- **Compliance Tracking**: Documentation and certification requirements
- **Professional Interface**: Business-standard user experience

## Technical Details

- **Framework**: Flask 2.3.3
- **Frontend**: Bootstrap 5.1.3 with FontAwesome icons
- **Database**: In-memory storage with JSON file persistence
- **Session Management**: Flask built-in sessions with security context
- **Logging**: JSON-based activity and audit logging

## Special Order System

Don't see the equipment you need? Our special order system allows you to:
- Request specific equipment from any manufacturer
- Provide detailed specifications and requirements
- Set budget ranges and timeline requirements
- Receive expert consultation and recommendations
- Track request status and communication

## Stopping the Application

### Direct Python Method:
- Press `Ctrl+C` in the terminal to stop the Flask development server

### Docker Method:
- **Docker Compose**: Press `Ctrl+C` or run `docker-compose down`
- **Manual Docker**: Press `Ctrl+C` or run `docker stop <container_name>`

## Data Persistence

The application automatically saves data to JSON files:

- **Direct Python**: Files saved in the application directory
  - `orders.json` - Order history
  - `special_orders.json` - Special order requests  
  - `service_requests.json` - Laboratory service requests
  - `activity_log.json` - User activity logs

- **Docker**: Files saved in the `./data` directory (mounted volume)
  - Persistent across container restarts
  - Easy backup and data management

## Educational Use and Distribution

This application is designed for educational purposes and can be easily distributed:

1. **Zip the entire project directory**
2. **Share with students/colleagues**
3. **Recipients can run using either method above**
4. **No external database required** - everything is self-contained

### What's Included in the Package:
- Complete Flask web application
- All HTML templates and styling
- Comprehensive product catalog (49 products)
- 6 laboratory service categories
- Multi-user authentication system
- Docker deployment configuration
- Complete documentation

## Troubleshooting

### Common Issues and Solutions:

**"ModuleNotFoundError: No module named 'flask'"**
- Solution: Install requirements with `pip install -r requirements.txt`

**"Permission denied" errors**
- Solution: Run terminal as administrator or use `sudo` on Linux/Mac

**"Port 5000 already in use"**
- Solution: Kill existing processes using port 5000 or change port in `app.py`

**Docker issues**
- Ensure Docker Desktop is running
- Try `docker-compose down` then `docker-compose up --build`

**Browser shows "This site can't be reached"**
- Ensure the application is running (check terminal output)
- Try `http://127.0.0.1:5000` instead of `localhost:5000`
- Check firewall settings

**Service requests not saving**
- Check write permissions in the application directory
- Ensure you're logged in when submitting requests

### For Educational Instructors:
- Students should use the `student` account for basic access
- Use `admin` account to demonstrate full BSL-4 features
- `researcher` account shows intermediate BSL-3 access
- Data files can be reset by deleting JSON files

**Viewing Activity Logs:**
- Login as `admin` (admin/biolab123) to access activity logs
- Click "Activity Logs" in the navigation menu (admin-only feature)
- View comprehensive activity monitoring including:
  - User login/logout events
  - Product catalog access
  - Service requests submitted
  - Order transactions
  - Security events and unauthorized access attempts
  - Real-time activity summaries and statistics

**Alternative Log Access:**
- Direct file access: View `activity_log.json` in the application directory
- Contains detailed JSON records of all user interactions
- Perfect for security analysis and compliance auditing

---

**BioLab Associates** - Your trusted partner for laboratory equipment and biological research supplies.  
© 2024 BioLab Associates. All rights reserved. 