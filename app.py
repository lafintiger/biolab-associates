from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'biolab_test_key_2024')
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_PERMANENT'] = False

# User database with security clearance levels
USERS = {
    'admin': {
        'password': 'biolab123',
        'clearance_level': 'BSL4_AUTHORIZED',
        'max_order_value': 1000000,
        'facility_id': 'FAC-001',
        'organization': 'BioLab Research Institute'
    },
    'researcher': {
        'password': 'research456',
        'clearance_level': 'BSL3_CERTIFIED',
        'max_order_value': 250000,
        'facility_id': 'FAC-002',
        'organization': 'University Medical Center'
    },
    'student': {
        'password': 'student789',
        'clearance_level': 'BASIC',
        'max_order_value': 5000,
        'facility_id': None,
        'organization': 'Educational Institution'
    }
}

# Security clearance levels
USER_CLEARANCE_LEVELS = {
    'BASIC': {
        'access_level': 1,
        'max_order_value': 5000,
        'restricted_categories': ['bsl3_equipment', 'research_materials', 'decontamination'],
        'allowed_bsl_levels': [1]
    },
    'INSTITUTIONAL': {
        'access_level': 2,
        'max_order_value': 50000,
        'requires_verification': True,
        'allowed_categories': ['specialized_ppe', 'decontamination'],
        'allowed_bsl_levels': [1, 2]
    },
    'BSL3_CERTIFIED': {
        'access_level': 3,
        'max_order_value': 250000,
        'requires_documentation': ['facility_license', 'irb_approval'],
        'allowed_categories': ['bsl3_equipment', 'specialized_ppe', 'research_materials', 'decontamination'],
        'allowed_bsl_levels': [1, 2, 3]
    },
    'BSL4_AUTHORIZED': {
        'access_level': 4,
        'max_order_value': 1000000,
        'requires_documentation': ['cdc_registration', 'facility_inspection', 'personnel_clearance'],
        'allowed_categories': ['all_categories'],
        'allowed_bsl_levels': [1, 2, 3, 4]
    }
}

# Product catalog with real biological equipment
PRODUCTS = {
    'biosafety_cabinets': [
        {
            'id': 'bsc001',
            'name': 'Thermo Scientific Class II A2 Biosafety Cabinet',
            'description': 'Herasafe KS 18 Class II biological safety cabinet with HEPA filtration',
            'price': 12500.00,
            'category': 'Biosafety Cabinets',
            'image': '/static/images/biosafety_cabinet.jpg',
            'specifications': 'Work area: 1200mm, HEPA efficiency: 99.995%'
        },
        {
            'id': 'bsc002', 
            'name': 'Baker SterilGARD e3 Class II Biosafety Cabinet',
            'description': 'Advanced biosafety cabinet with SmartFlow technology',
            'price': 15200.00,
            'category': 'Biosafety Cabinets',
            'image': '/static/images/baker_cabinet.jpg',
            'specifications': 'Work area: 1200mm, Energy efficient design'
        },
        {
            'id': 'bsc003',
            'name': 'Labconco Purifier Logic+ Class II A2 Biosafety Cabinet',
            'description': 'Energy-efficient biosafety cabinet with advanced airflow monitoring',
            'price': 13800.00,
            'category': 'Biosafety Cabinets',
            'image': '/static/images/labconco_cabinet.jpg',
            'specifications': 'Work area: 1200mm, SmartFlow airflow control, LED lighting'
        },
        {
            'id': 'bsc004',
            'name': 'NuAire LabGard ES Class II B2 Biosafety Cabinet',
            'description': 'Total exhaust biosafety cabinet for volatile chemicals',
            'price': 18900.00,
            'category': 'Biosafety Cabinets',
            'image': '/static/images/nuaire_cabinet.jpg',
            'specifications': 'Work area: 1200mm, 100% exhaust, Chemical-resistant construction'
        }
    ],
    'incubators': [
        {
            'id': 'inc001',
            'name': 'Thermo Scientific Heratherm Advanced Protocol Incubator',
            'description': 'Precision incubator for cell culture applications',
            'price': 3200.00,
            'category': 'Incubators',
            'image': '/static/images/incubator.jpg',
            'specifications': 'Temperature range: +5°C to +100°C, Volume: 50L'
        },
        {
            'id': 'inc002',
            'name': 'New Brunswick Innova 44 Incubator Shaker',
            'description': 'Benchtop incubator shaker for bacterial cultures',
            'price': 4800.00,
            'category': 'Incubators', 
            'image': '/static/images/shaker_incubator.jpg',
            'specifications': 'Temperature range: 4°C to 80°C, Speed: 25-500 rpm'
        },
        {
            'id': 'inc003',
            'name': 'PHC Corporation MCO-170AICUVH-PA CO2 Incubator',
            'description': 'Advanced CO2 incubator with contamination control',
            'price': 8900.00,
            'category': 'Incubators',
            'image': '/static/images/co2_incubator.jpg',
            'specifications': 'Volume: 165L, CO2 range: 0-20%, HEPA filtration'
        },
        {
            'id': 'inc004',
            'name': 'Binder CB Series CO2 Incubator',
            'description': 'Reliable CO2 incubator with hot air sterilization',
            'price': 7200.00,
            'category': 'Incubators',
            'image': '/static/images/binder_incubator.jpg',
            'specifications': 'Volume: 160L, Hot air sterilization at 180°C, IR CO2 sensor'
        },
        {
            'id': 'inc005',
            'name': 'Eppendorf New Brunswick Excella E24 Incubator Shaker',
            'description': 'Floor model incubator shaker for large volume cultures',
            'price': 12400.00,
            'category': 'Incubators',
            'image': '/static/images/excella_shaker.jpg',
            'specifications': 'Temperature range: 4°C to 80°C, Speed: 25-500 rpm, 2.5" orbit'
        }
    ],
    'autoclaves': [
        {
            'id': 'auto001',
            'name': 'Tuttnauer 3870EA Autoclave',
            'description': 'Benchtop steam sterilizer with automatic controls',
            'price': 8500.00,
            'category': 'Autoclaves',
            'image': '/static/images/autoclave.jpg',
            'specifications': 'Chamber: 15"D x 30"L, Pre-vacuum and gravity cycles'
        },
        {
            'id': 'auto002',
            'name': 'STERIS Amsco Century V116 Steam Sterilizer',
            'description': 'Large capacity steam sterilizer for research applications',
            'price': 35000.00,
            'category': 'Autoclaves',
            'image': '/static/images/steris_autoclave.jpg',
            'specifications': 'Chamber: 16"W x 26"D x 24"H, Prevacuum and gravity, Printer'
        },
        {
            'id': 'auto003',
            'name': 'Midmark M11 UltraClave Automatic Sterilizer',
            'description': 'Compact fully automatic steam sterilizer',
            'price': 4200.00,
            'category': 'Autoclaves',
            'image': '/static/images/midmark_autoclave.jpg',
            'specifications': 'Chamber: 11"D x 18"L, Fully automatic cycle, Self-monitoring'
        }
    ],
    'dna_extractors': [
        {
            'id': 'dna001',
            'name': 'QIAGEN QIAcube Connect Automated DNA Extractor',
            'description': 'Automated nucleic acid purification system',
            'price': 28000.00,
            'category': 'DNA Extractors',
            'image': '/static/images/qiacube.jpg',
            'specifications': 'Throughput: 1-12 samples, Multiple purification protocols'
        },
        {
            'id': 'dna002',
            'name': 'Hamilton Microlab STARlet Liquid Handler',
            'description': 'Automated liquid handling for DNA extraction workflows',
            'price': 45000.00,
            'category': 'DNA Extractors',
            'image': '/static/images/hamilton.jpg',
            'specifications': '8-channel pipetting, Volume range: 0.5-1000µL'
        },
        {
            'id': 'dna003',
            'name': 'Promega Maxwell RSC 48 Instrument',
            'description': 'High-throughput automated nucleic acid purification',
            'price': 52000.00,
            'category': 'DNA Extractors',
            'image': '/static/images/maxwell.jpg',
            'specifications': 'Throughput: 1-48 samples, 45 minutes processing time'
        },
        {
            'id': 'dna004',
            'name': 'KingFisher Flex Magnetic Particle Processor',
            'description': 'Flexible magnetic bead-based purification system',
            'price': 32000.00,
            'category': 'DNA Extractors',
            'image': '/static/images/kingfisher.jpg',
            'specifications': 'Throughput: 1-96 samples, Magnetic separation technology'
        }
    ],
    'pcr_systems': [
        {
            'id': 'pcr001',
            'name': 'Applied Biosystems VeriFlex PCR System',
            'description': 'Flexible thermal cycler for PCR applications',
            'price': 15600.00,
            'category': 'PCR Systems',
            'image': '/static/images/veriflex.jpg',
            'specifications': '48-384 well capacity, Fast ramping technology'
        },
        {
            'id': 'pcr002',
            'name': 'Bio-Rad T100 Thermal Cycler',
            'description': 'Reliable thermal cycler with intuitive interface',
            'price': 6200.00,
            'category': 'PCR Systems',
            'image': '/static/images/t100.jpg',
            'specifications': '96-well capacity, Gradient capability'
        },
        {
            'id': 'pcr003',
            'name': 'Applied Biosystems ProFlex PCR System',
            'description': '3-in-1 thermal cycler with interchangeable blocks',
            'price': 18500.00,
            'category': 'PCR Systems',
            'image': '/static/images/proflex.jpg',
            'specifications': '2x96, 384 or 96+384 well capacity, VeriFlex blocks'
        },
        {
            'id': 'pcr004',
            'name': 'Eppendorf Mastercycler X50 PCR System',
            'description': 'Advanced thermal cycler with silver block technology',
            'price': 12800.00,
            'category': 'PCR Systems',
            'image': '/static/images/mastercycler.jpg',
            'specifications': '96-well capacity, OptiLid technology, Fast ramping'
        }
    ],
    'microscopes': [
        {
            'id': 'mic001',
            'name': 'Leica DM6000 B Upright Microscope',
            'description': 'Advanced research microscope with LED illumination',
            'price': 32000.00,
            'category': 'Microscopes',
            'image': '/static/images/leica_microscope.jpg',
            'specifications': 'LED illumination, 6-position objective nosepiece, Digital interface'
        },
        {
            'id': 'mic002',
            'name': 'Zeiss Axio Observer 7 Inverted Microscope',
            'description': 'Inverted microscope for live cell imaging',
            'price': 48000.00,
            'category': 'Microscopes',
            'image': '/static/images/zeiss_microscope.jpg',
            'specifications': 'Inverted design, Definite Focus.2, LED modules'
        },
        {
            'id': 'mic003',
            'name': 'Olympus CX23 Binocular Microscope',
            'description': 'Educational and clinical microscope',
            'price': 1850.00,
            'category': 'Microscopes',
            'image': '/static/images/olympus_microscope.jpg',
            'specifications': 'LED illumination, 4x, 10x, 40x, 100x objectives'
        },
        {
            'id': 'mic004',
            'name': 'Nikon Eclipse Ti2 Inverted Microscope',
            'description': 'Advanced inverted microscope system',
            'price': 65000.00,
            'category': 'Microscopes',
            'image': '/static/images/nikon_microscope.jpg',
            'specifications': 'Motorized components, Perfect Focus System, Ti2 hub'
        }
    ],
    'centrifuges': [
        {
            'id': 'cen001',
            'name': 'Eppendorf Centrifuge 5424 R',
            'description': 'Refrigerated microcentrifuge with versatile rotor selection',
            'price': 12500.00,
            'category': 'Centrifuges',
            'image': '/static/images/eppendorf_centrifuge.jpg',
            'specifications': 'Max speed: 21,130 xg, Temperature range: -10°C to 40°C'
        },
        {
            'id': 'cen002',
            'name': 'Beckman Coulter Allegra X-30R Centrifuge',
            'description': 'Benchtop centrifuge with refrigeration',
            'price': 18900.00,
            'category': 'Centrifuges',
            'image': '/static/images/beckman_centrifuge.jpg',
            'specifications': 'Max speed: 30,000 rpm, Temperature range: -20°C to 40°C'
        },
        {
            'id': 'cen003',
            'name': 'Thermo Scientific Sorvall LYNX 6000 Superspeed Centrifuge',
            'description': 'High-speed floor model centrifuge',
            'price': 85000.00,
            'category': 'Centrifuges',
            'image': '/static/images/sorvall_centrifuge.jpg',
            'specifications': 'Max speed: 75,000 rpm, Temperature range: -20°C to 40°C'
        }
    ],
    'spectrophotometers': [
        {
            'id': 'spec001',
            'name': 'Thermo Scientific NanoDrop One Microvolume UV-Vis Spectrophotometer',
            'description': 'Microvolume spectrophotometer for nucleic acid quantification',
            'price': 14500.00,
            'category': 'Spectrophotometers',
            'image': '/static/images/nanodrop.jpg',
            'specifications': 'Sample volume: 0.5-2.0µL, Wavelength range: 190-850 nm'
        },
        {
            'id': 'spec002',
            'name': 'Bio-Rad SmartSpec Plus Spectrophotometer',
            'description': 'Simple, reliable UV-Vis spectrophotometer',
            'price': 3200.00,
            'category': 'Spectrophotometers',
            'image': '/static/images/smartspec.jpg',
            'specifications': 'Wavelength range: 340-700 nm, 1.5 nm bandwidth'
        },
        {
            'id': 'spec003',
            'name': 'Agilent Cary 60 UV-Vis Spectrophotometer',
            'description': 'High-performance UV-Vis spectrophotometer',
            'price': 28000.00,
            'category': 'Spectrophotometers',
            'image': '/static/images/cary60.jpg',
            'specifications': 'Wavelength range: 190-1100 nm, 1.5 nm bandwidth'
        }
    ],
    'gel_electrophoresis': [
        {
            'id': 'gel001',
            'name': 'Bio-Rad Mini-PROTEAN Tetra Vertical Electrophoresis Cell',
            'description': 'Compact system for protein electrophoresis',
            'price': 1200.00,
            'category': 'Gel Electrophoresis',
            'image': '/static/images/miniprotean.jpg',
            'specifications': '4-gel capacity, Multiple gel formats, Temperature control'
        },
        {
            'id': 'gel002',
            'name': 'Invitrogen E-Gel Power Snap Electrophoresis System',
            'description': 'Rapid agarose gel electrophoresis system',
            'price': 2400.00,
            'category': 'Gel Electrophoresis',
            'image': '/static/images/egel.jpg',
            'specifications': '8-15 minute run times, No gel preparation required'
        },
        {
            'id': 'gel003',
            'name': 'Bio-Rad PowerPac Basic Power Supply',
            'description': 'Reliable power supply for electrophoresis',
            'price': 850.00,
            'category': 'Gel Electrophoresis',
            'image': '/static/images/powerpac.jpg',
            'specifications': 'Constant voltage, current, or power, 300V/400mA/75W max'
        }
    ],
    'bsl3_equipment': [
        {
            'id': 'bsl3001',
            'name': 'Baker SterilGARD e3 Class III Biological Safety Cabinet',
            'description': 'Fully enclosed glove-box style cabinet for BSL-3/4 containment',
            'price': 85000.00,
            'category': 'BSL-3 Equipment',
            'image': '/static/images/class3_cabinet.jpg',
            'specifications': 'Negative pressure containment, HEPA filtration, Gas-tight construction',
            'bsl_level': 3,
            'requires_clearance': True,
            'restricted': True
        },
        {
            'id': 'bsl3002',
            'name': 'IsoGard Positive Pressure Personnel Suit System',
            'description': 'Complete positive pressure suit system for BSL-4 operations',
            'price': 12500.00,
            'category': 'BSL-3 Equipment',
            'image': '/static/images/pressure_suit.jpg',
            'specifications': 'Positive pressure air supply, Chemical resistant material, Emergency escape breathing apparatus',
            'bsl_level': 4,
            'requires_clearance': True,
            'restricted': True
        },
        {
            'id': 'bsl3003',
            'name': 'STERIS VHP ARD Pass-Through Chamber',
            'description': 'Automated sterilization pass-through for BSL-3/4 facilities',
            'price': 125000.00,
            'category': 'BSL-3 Equipment',
            'image': '/static/images/passthrough.jpg',
            'specifications': 'Vaporized hydrogen peroxide sterilization, Automated cycle control, Bio-decontamination validation',
            'bsl_level': 3,
            'requires_clearance': True,
            'restricted': True
        },
        {
            'id': 'bsl3004',
            'name': 'ULPA Filtration Air Handling Unit',
            'description': 'Ultra-low penetration air filtration system for containment facilities',
            'price': 95000.00,
            'category': 'BSL-3 Equipment',
            'image': '/static/images/ulpa_system.jpg',
            'specifications': '99.999% efficiency at 0.12 microns, Redundant filtration, Continuous monitoring',
            'bsl_level': 3,
            'requires_clearance': True,
            'restricted': True
        }
    ],
    'specialized_ppe': [
        {
            'id': 'ppe001',
            'name': '3M Versaflo TR-300+ Powered Air Respirator',
            'description': 'Powered air-purifying respirator for biological containment',
            'price': 2800.00,
            'category': 'Specialized PPE',
            'image': '/static/images/papr.jpg',
            'specifications': 'HEPA filtration, 8-hour battery life, Voice amplification',
            'bsl_level': 2,
            'requires_clearance': False,
            'restricted': False
        },
        {
            'id': 'ppe002',
            'name': 'DuPont Tychem TK Chemical Protection Suit',
            'description': 'Gas-tight chemical protective suit for maximum protection',
            'price': 1200.00,
            'category': 'Specialized PPE',
            'image': '/static/images/chemical_suit.jpg',
            'specifications': 'Multi-gas protection, Butyl rubber construction, Emergency escape capabilities',
            'bsl_level': 3,
            'requires_clearance': True,
            'restricted': True
        },
        {
            'id': 'ppe003',
            'name': 'Ansell AlphaTec Butyl Rubber Gloves',
            'description': 'Chemical resistant gloves for hazardous material handling',
            'price': 85.00,
            'category': 'Specialized PPE',
            'image': '/static/images/butyl_gloves.jpg',
            'specifications': 'Butyl rubber construction, 32-mil thickness, Chemical breakthrough resistance',
            'bsl_level': 2,
            'requires_clearance': False,
            'restricted': False
        }
    ],
    'research_materials': [
        {
            'id': 'mat001',
            'name': 'Inactivated Pathogen Reference Panel',
            'description': 'Heat-inactivated specimens for diagnostic training and validation',
            'price': 850.00,
            'category': 'Research Materials',
            'image': '/static/images/reference_panel.jpg',
            'specifications': 'Multiple pathogen types, Certified inactivation, Research use only',
            'bsl_level': 1,
            'requires_clearance': True,
            'restricted': True,
            'documentation_required': ['facility_license', 'training_certificate']
        },
        {
            'id': 'mat002',
            'name': 'Biosafety Training Culture Kit',
            'description': 'Non-pathogenic bacterial cultures for training purposes',
            'price': 320.00,
            'category': 'Research Materials',
            'image': '/static/images/training_cultures.jpg',
            'specifications': 'Non-pathogenic strains, Educational use only, Safety data sheets included',
            'bsl_level': 1,
            'requires_clearance': False,
            'restricted': False
        },
        {
            'id': 'mat003',
            'name': 'Vaccine Development Substrate Kit',
            'description': 'Specialized cell culture media for vaccine research',
            'price': 1250.00,
            'category': 'Research Materials',
            'image': '/static/images/vaccine_substrate.jpg',
            'specifications': 'Sterile formulation, Multiple substrate types, Research grade purity',
            'bsl_level': 2,
            'requires_clearance': True,
            'restricted': True,
            'documentation_required': ['irb_approval', 'facility_license']
        }
    ],
    'decontamination': [
        {
            'id': 'decon001',
            'name': 'STERIS Sporicidin Disinfectant Concentrate',
            'description': 'Sporicidal disinfectant for BSL-3/4 decontamination',
            'price': 450.00,
            'category': 'Decontamination',
            'image': '/static/images/sporicidin.jpg',
            'specifications': 'EPA registered sporicidal, Broad spectrum efficacy, Concentrate formula',
            'bsl_level': 3,
            'requires_clearance': False,
            'restricted': True
        },
        {
            'id': 'decon002',
            'name': 'American Ultraviolet Germicidal UV Lamp System',
            'description': 'UV-C germicidal lamps for surface decontamination',
            'price': 2200.00,
            'category': 'Decontamination',
            'image': '/static/images/uv_system.jpg',
            'specifications': '254nm UV-C output, Timer controls, Safety interlocks',
            'bsl_level': 2,
            'requires_clearance': False,
            'restricted': False
        },
        {
            'id': 'decon003',
            'name': 'BIOQUELL Clarus C Fumigation System',
            'description': 'Hydrogen peroxide vapor room decontamination system',
            'price': 185000.00,
            'category': 'Decontamination',
            'image': '/static/images/fumigation.jpg',
            'specifications': 'Room-scale decontamination, Automated process control, Validation documentation',
            'bsl_level': 4,
            'requires_clearance': True,
            'restricted': True,
            'documentation_required': ['facility_registration', 'operator_certification']
        }
    ],
    'biological_specimens': [
        {
            'id': 'bio001',
            'name': 'Bacillus anthracis (Sterne strain) - Research Grade',
            'description': 'Non-weaponized vaccine strain for BSL-3 research and training',
            'price': 2850.00,
            'category': 'Biological Specimens',
            'image': '/static/images/bacillus_anthracis.jpg',
            'specifications': 'Avirulent Sterne strain (34F2), Lyophilized culture, Certificate of analysis included',
            'bsl_level': 3,
            'requires_clearance': True,
            'restricted': True,
            'documentation_required': ['bsl3_facility_license', 'cdc_registration', 'irb_approval', 'personnel_training_cert']
        },
        {
            'id': 'bio002',
            'name': 'Clostridium botulinum Type A - Research Isolate',
            'description': 'Neurotoxin-producing strain for vaccine and therapeutic research',
            'price': 3200.00,
            'category': 'Biological Specimens',
            'image': '/static/images/clostridium_botulinum.jpg',
            'specifications': 'Type A Hall strain, Spore suspension, BSL-3 containment required',
            'bsl_level': 3,
            'requires_clearance': True,
            'restricted': True,
            'documentation_required': ['bsl3_facility_license', 'select_agent_permit', 'irb_approval', 'security_clearance']
        },
        {
            'id': 'bio003',
            'name': 'Abrus precatorius Seeds (Rosary Pea) - Research Sample',
            'description': 'Abrin-containing seeds for toxicology and antidote development research',
            'price': 1750.00,
            'category': 'Biological Specimens',
            'image': '/static/images/rosary_pea.jpg',
            'specifications': '10g authenticated seeds, High abrin content, Chain of custody documentation',
            'bsl_level': 3,
            'requires_clearance': True,
            'restricted': True,
            'documentation_required': ['dea_registration', 'facility_license', 'toxin_research_permit', 'security_plan']
        },
        {
            'id': 'bio004',
            'name': 'Ricinus communis Extract (Ricin) - Research Grade',
            'description': 'Purified ricin toxin for vaccine development and medical countermeasures',
            'price': 4500.00,
            'category': 'Biological Specimens',
            'image': '/static/images/ricin.jpg',
            'specifications': 'Purified ricin toxin, 1mg vial, BSL-3 handling required',
            'bsl_level': 3,
            'requires_clearance': True,
            'restricted': True,
            'documentation_required': ['select_agent_permit', 'toxin_research_license', 'security_clearance', 'facility_inspection_cert']
        },
        {
            'id': 'bio005',
            'name': 'Francisella tularensis - Research Strain',
            'description': 'Attenuated strain for tularemia research and vaccine development',
            'price': 2650.00,
            'category': 'Biological Specimens',
            'image': '/static/images/francisella.jpg',
            'specifications': 'Live vaccine strain (LVS), Lyophilized culture, Research use only',
            'bsl_level': 3,
            'requires_clearance': True,
            'restricted': True,
            'documentation_required': ['bsl3_facility_license', 'select_agent_registration', 'personnel_security_check']
        },
        {
            'id': 'bio006',
            'name': 'Yersinia pestis - Avirulent Research Strain',
            'description': 'Pigmentation-negative strain for plague research (pPCP1-, pMT1-)',
            'price': 3850.00,
            'category': 'Biological Specimens',
            'image': '/static/images/yersinia_pestis.jpg',
            'specifications': 'Avirulent laboratory strain, Missing virulence plasmids, BSL-2 containment adequate',
            'bsl_level': 2,
            'requires_clearance': True,
            'restricted': True,
            'documentation_required': ['facility_license', 'researcher_training_cert', 'irb_approval']
        },
        {
            'id': 'bio007',
            'name': 'Variola Major DNA Fragments - Sequencing Kit',
            'description': 'Non-infectious DNA segments for diagnostic development (WHO approved)',
            'price': 5200.00,
            'category': 'Biological Specimens',
            'image': '/static/images/variola_dna.jpg',
            'specifications': 'Cloned DNA fragments, Non-infectious, WHO/CDC approved segments only',
            'bsl_level': 4,
            'requires_clearance': True,
            'restricted': True,
            'documentation_required': ['bsl4_facility_certification', 'who_approval', 'international_permit', 'maximum_security_clearance']
        },
        {
            'id': 'bio008',
            'name': 'Castor Bean Extract Kit - Toxicology Research',
            'description': 'Standardized castor bean components for ricin precursor studies',
            'price': 850.00,
            'category': 'Biological Specimens',
            'image': '/static/images/castor_beans.jpg',
            'specifications': 'Standardized extract, Ricinus communis components, Educational/research grade',
            'bsl_level': 2,
            'requires_clearance': True,
            'restricted': True,
            'documentation_required': ['facility_license', 'safety_protocol_approval']
        },
        {
            'id': 'bio009',
            'name': 'Brucella abortus - Vaccine Strain RB51',
            'description': 'Rough, attenuated vaccine strain for brucellosis research',
            'price': 1950.00,
            'category': 'Biological Specimens',
            'image': '/static/images/brucella.jpg',
            'specifications': 'RB51 vaccine strain, Lyophilized culture, Veterinary research grade',
            'bsl_level': 3,
            'requires_clearance': True,
            'restricted': True,
            'documentation_required': ['bsl3_facility_license', 'veterinary_research_permit', 'biosafety_approval']
        },
        {
            'id': 'bio010',
            'name': 'Burkholderia mallei - Research Isolate',
            'description': 'Attenuated strain for glanders research and countermeasure development',
            'price': 4200.00,
            'category': 'Biological Specimens',
            'image': '/static/images/burkholderia.jpg',
            'specifications': 'Laboratory-attenuated strain, Research use only, BSL-3 containment required',
            'bsl_level': 3,
            'requires_clearance': True,
            'restricted': True,
            'documentation_required': ['select_agent_permit', 'bsl3_certification', 'defense_research_clearance']
        }
    ],
    'detoxicants': [
        {
            'id': 'detox001',
            'name': 'Neutralizing Monoclonal Antibody mAb 10D8 (Anti-Abrin)',
            'description': 'Experimental neutralizing antibody with promise for abrin toxin treatment',
            'price': 8500.00,
            'category': 'Detoxicants & Antidotes',
            'image': '/static/images/mab_10d8.jpg',
            'specifications': 'Monoclonal antibody, Anti-abrin specificity, Research grade, 1mg vial',
            'bsl_level': 3,
            'requires_clearance': True,
            'restricted': True,
            'documentation_required': ['toxin_research_license', 'irb_approval', 'facility_license', 'antidote_research_permit']
        },
        {
            'id': 'detox002',
            'name': 'Anti-Ricin Neutralizing Antibody (RAC18)',
            'description': 'Neutralizing antibody for ricin toxin exposure treatment research',
            'price': 9200.00,
            'category': 'Detoxicants & Antidotes',
            'image': '/static/images/anti_ricin.jpg',
            'specifications': 'Humanized monoclonal antibody, High neutralizing capacity, Clinical grade',
            'bsl_level': 3,
            'requires_clearance': True,
            'restricted': True,
            'documentation_required': ['select_agent_permit', 'clinical_research_license', 'irb_approval', 'gmp_facility_cert']
        },
        {
            'id': 'detox003',
            'name': 'Botulinum Antitoxin (Equine-derived, Heptavalent)',
            'description': 'Polyvalent botulinum antitoxin for Types A, B, C, D, E, F, G',
            'price': 12500.00,
            'category': 'Detoxicants & Antidotes',
            'image': '/static/images/botulinum_antitoxin.jpg',
            'specifications': 'Equine-derived, Heptavalent formula, Emergency treatment grade, Cold storage required',
            'bsl_level': 3,
            'requires_clearance': True,
            'restricted': True,
            'documentation_required': ['emergency_response_license', 'veterinary_antitoxin_permit', 'cold_storage_cert', 'medical_facility_license']
        },
        {
            'id': 'detox004',
            'name': 'Anthrax Immune Globulin (Human)',
            'description': 'Human-derived antibodies for post-exposure anthrax prophylaxis research',
            'price': 15000.00,
            'category': 'Detoxicants & Antidotes',
            'image': '/static/images/anthrax_ig.jpg',
            'specifications': 'Human plasma-derived, High titer anti-PA antibodies, Clinical research grade',
            'bsl_level': 3,
            'requires_clearance': True,
            'restricted': True,
            'documentation_required': ['blood_product_license', 'clinical_research_permit', 'fda_investigational_approval', 'pathogen_immunity_cert']
        },
        {
            'id': 'detox005',
            'name': 'Chelation Therapy Kit (Heavy Metal Detoxification)',
            'description': 'Comprehensive chelation agents for heavy metal poisoning treatment',
            'price': 3200.00,
            'category': 'Detoxicants & Antidotes',
            'image': '/static/images/chelation_kit.jpg',
            'specifications': 'EDTA, DMSA, DMPS, BAL included, Emergency treatment protocols, Medical grade',
            'bsl_level': 2,
            'requires_clearance': True,
            'restricted': True,
            'documentation_required': ['medical_facility_license', 'emergency_response_cert', 'toxicology_training_cert']
        },
        {
            'id': 'detox006',
            'name': 'Sodium Thiosulfate Injection (Cyanide Antidote)',
            'description': 'High-concentration sodium thiosulfate for cyanide poisoning treatment',
            'price': 850.00,
            'category': 'Detoxicants & Antidotes',
            'image': '/static/images/sodium_thiosulfate.jpg',
            'specifications': '25% solution, Injectable grade, Emergency antidote, Shelf life 24 months',
            'bsl_level': 2,
            'requires_clearance': True,
            'restricted': True,
            'documentation_required': ['emergency_medical_license', 'poison_control_cert', 'antidote_storage_permit']
        },
        {
            'id': 'detox007',
            'name': 'Methylene Blue Injection (Methemoglobinemia Treatment)',
            'description': 'Pharmaceutical-grade methylene blue for nitrite/nitrate poisoning',
            'price': 750.00,
            'category': 'Detoxicants & Antidotes',
            'image': '/static/images/methylene_blue.jpg',
            'specifications': '1% injectable solution, USP grade, Methemoglobinemia antidote, Light-protected vials',
            'bsl_level': 1,
            'requires_clearance': True,
            'restricted': True,
            'documentation_required': ['medical_facility_license', 'pharmaceutical_handling_cert']
        },
        {
            'id': 'detox008',
            'name': 'Obidoxime Chloride (Nerve Agent Antidote)',
            'description': 'Oxime compound for organophosphate and nerve agent poisoning',
            'price': 4500.00,
            'category': 'Detoxicants & Antidotes',
            'image': '/static/images/obidoxime.jpg',
            'specifications': 'Pharmaceutical grade, Acetylcholinesterase reactivator, Military-spec packaging',
            'bsl_level': 3,
            'requires_clearance': True,
            'restricted': True,
            'documentation_required': ['chemical_warfare_research_permit', 'defense_contractor_license', 'nerve_agent_training_cert', 'secure_storage_permit']
        },
        {
            'id': 'detox009',
            'name': 'Activated Charcoal Suspension (USP Grade)',
            'description': 'High-surface-area activated charcoal for toxin adsorption',
            'price': 450.00,
            'category': 'Detoxicants & Antidotes',
            'image': '/static/images/activated_charcoal.jpg',
            'specifications': 'USP pharmaceutical grade, High adsorption capacity, Emergency decontamination',
            'bsl_level': 1,
            'requires_clearance': False,
            'restricted': False
        },
        {
            'id': 'detox010',
            'name': 'Prussian Blue Capsules (Cesium-137 Decorporation)',
            'description': 'Pharmaceutical Prussian blue for radioactive cesium elimination',
            'price': 2800.00,
            'category': 'Detoxicants & Antidotes',
            'image': '/static/images/prussian_blue.jpg',
            'specifications': 'Insoluble Prussian blue, 500mg capsules, Radiological emergency antidote',
            'bsl_level': 2,
            'requires_clearance': True,
            'restricted': True,
            'documentation_required': ['radiological_emergency_license', 'nuclear_medicine_permit', 'radiation_safety_cert']
        },
        {
            'id': 'detox011',
            'name': 'Monoclonal Antibody D6F10 (Broad-Spectrum Toxin Neutralizer)',
            'description': 'Broad-spectrum neutralizing antibody for multiple plant and bacterial toxins',
            'price': 11200.00,
            'category': 'Detoxicants & Antidotes',
            'image': '/static/images/mab_d6f10.jpg',
            'specifications': 'Monoclonal antibody, Broad-spectrum neutralization, Research grade, 2mg vial',
            'bsl_level': 3,
            'requires_clearance': True,
            'restricted': True,
            'documentation_required': ['toxin_research_license', 'broad_spectrum_permit', 'irb_approval', 'multi_toxin_clearance']
        },
        {
            'id': 'detox012',
            'name': 'Humanized Antibody S008 (Advanced Therapeutic)',
            'description': 'Next-generation humanized antibody for enhanced biocompatibility and efficacy',
            'price': 15800.00,
            'category': 'Detoxicants & Antidotes',
            'image': '/static/images/humanized_s008.jpg',
            'specifications': 'Humanized therapeutic antibody, Enhanced biocompatibility, Clinical trial grade, 5mg vial',
            'bsl_level': 3,
            'requires_clearance': True,
            'restricted': True,
            'documentation_required': ['clinical_trial_license', 'humanized_therapy_permit', 'fda_investigational_approval', 'advanced_therapeutic_cert']
        },
        {
            'id': 'detox013',
            'name': 'Activated Charcoal (Medical Emergency Grade)',
            'description': 'Ultra-high surface area activated charcoal for emergency toxin adsorption',
            'price': 680.00,
            'category': 'Detoxicants & Antidotes',
            'image': '/static/images/activated_charcoal_medical.jpg',
            'specifications': 'Medical emergency grade, 2000+ m²/g surface area, USP pharmaceutical grade, Emergency response kit',
            'bsl_level': 1,
            'requires_clearance': True,
            'restricted': True,
            'documentation_required': ['emergency_medical_license', 'poison_control_cert']
        }
    ]
}

# Flatten products for easy lookup
ALL_PRODUCTS = {}
for category_products in PRODUCTS.values():
    for product in category_products:
        ALL_PRODUCTS[product['id']] = product

# Orders and activity log
ORDERS = []
ACTIVITY_LOG = []

def log_activity(action, details):
    """Log user activity"""
    entry = {
        'timestamp': datetime.datetime.now().isoformat(),
        'user': session.get('username', 'anonymous'),
        'action': action,
        'details': details
    }
    ACTIVITY_LOG.append(entry)
    
    # Also save to file
    with open('activity_log.json', 'w') as f:
        json.dump(ACTIVITY_LOG, f, indent=2)

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    log_activity('page_visit', {'page': 'home'})
    return render_template('index.html', username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in USERS and USERS[username]['password'] == password:
            user_data = USERS[username]
            session['username'] = username
            session['clearance_level'] = user_data['clearance_level']
            session['max_order_value'] = user_data['max_order_value']
            session['facility_id'] = user_data['facility_id']
            session['organization'] = user_data['organization']
            # Only initialize cart if it doesn't exist (preserve existing cart)
            if 'cart' not in session:
                session['cart'] = {}
            log_activity('login', {
                'success': True, 
                'clearance_level': user_data['clearance_level'],
                'facility_id': user_data['facility_id']
            })
            return redirect(url_for('index'))
        else:
            log_activity('login', {'success': False, 'username': username})
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    log_activity('logout', {})
    session.clear()
    return redirect(url_for('login'))

def check_product_access(product, user_clearance):
    """Check if user has access to view/purchase a product"""
    # Check if product requires special clearance or has BSL restrictions
    if product.get('requires_clearance', False) or product.get('bsl_level', 1) > 1:
        clearance_data = USER_CLEARANCE_LEVELS.get(user_clearance, {})
        allowed_bsl_levels = clearance_data.get('allowed_bsl_levels', [1])
        product_bsl = product.get('bsl_level', 1)
        
        if product_bsl not in allowed_bsl_levels:
            return False, f"BSL-{product_bsl} clearance required"
        
        if product.get('requires_clearance', False) and user_clearance == 'BASIC':
            return False, "Institutional clearance required"
    
    # Standard products (no special requirements) are accessible to all users
    return True, None

@app.route('/catalog')
def catalog():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    category = request.args.get('category', 'all')
    user_clearance = session.get('clearance_level', 'BASIC')
    
    log_activity('catalog_view', {'category': category, 'user_clearance': user_clearance})
    
    if category == 'all':
        all_products = ALL_PRODUCTS
    else:
        all_products = {p['id']: p for p in PRODUCTS.get(category, [])}
    
    # Filter products based on user clearance
    accessible_products = {}
    restricted_count = 0
    
    for product_id, product in all_products.items():
        has_access, restriction_reason = check_product_access(product, user_clearance)
        if has_access:
            accessible_products[product_id] = product
        else:
            restricted_count += 1
            # Show restricted products but mark them as inaccessible
            restricted_product = product.copy()
            restricted_product['access_restricted'] = True
            restricted_product['restriction_reason'] = restriction_reason
            accessible_products[product_id] = restricted_product
    
    return render_template('catalog.html', 
                         products=accessible_products, 
                         categories=PRODUCTS.keys(), 
                         current_category=category,
                         user_clearance=user_clearance,
                         restricted_count=restricted_count)

@app.route('/product/<product_id>')
def product_detail(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    product = ALL_PRODUCTS.get(product_id)
    if not product:
        return "Product not found", 404
    
    log_activity('product_view', {'product_id': product_id, 'product_name': product['name']})
    return render_template('product_detail.html', product=product)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    product_id = request.form['product_id']
    quantity = int(request.form.get('quantity', 1))
    
    if 'cart' not in session:
        session['cart'] = {}
    
    if product_id in session['cart']:
        session['cart'][product_id] += quantity
    else:
        session['cart'][product_id] = quantity
    
    session.modified = True
    
    product = ALL_PRODUCTS.get(product_id)
    log_activity('add_to_cart', {
        'product_id': product_id, 
        'product_name': product['name'] if product else 'Unknown',
        'quantity': quantity,
        'cart_after_add': session.get('cart', {}),
        'session_modified': True
    })
    
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    cart_items = []
    total = 0
    
    cart_data = session.get('cart', {})
    user_clearance = session.get('clearance_level', 'BASIC')
    
    # Track products to remove from cart
    products_to_remove = []
    
    for product_id, quantity in cart_data.items():
        product = ALL_PRODUCTS.get(product_id)
        if product:
            # Check if user has access to this product
            has_access, restriction_reason = check_product_access(product, user_clearance)
            if has_access and not product.get('access_restricted', False):
                item_total = product['price'] * quantity
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'item_total': item_total
                })
                total += item_total
            else:
                # Mark restricted products for removal
                products_to_remove.append(product_id)
    
    # Remove restricted products from cart
    for product_id in products_to_remove:
        del session['cart'][product_id]
        session.modified = True
    
    log_activity('cart_view', {'item_count': len(cart_items), 'total': total, 'cart_data': cart_data})
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/checkout', methods=['POST'])
def checkout():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    cart_data = session.get('cart', {})
    if not cart_data:
        return redirect(url_for('cart'))
    
    # Create order
    order = {
        'id': f"ORD{len(ORDERS) + 1:05d}",
        'username': session['username'],
        'timestamp': datetime.datetime.now().isoformat(),
        'order_items': [],
        'total': 0,
        'status': 'completed'
    }
    
    for product_id, quantity in cart_data.items():
        product = ALL_PRODUCTS.get(product_id)
        if product:
            item_total = product['price'] * quantity
            order['order_items'].append({
                'product_id': product_id,
                'product_name': product['name'],
                'quantity': quantity,
                'price': product['price'],
                'item_total': item_total
            })
            order['total'] += item_total
    
    ORDERS.append(order)
    
    # Save orders to file
    with open('orders.json', 'w') as f:
        json.dump(ORDERS, f, indent=2)
    
    log_activity('order_placed', {
        'order_id': order['id'],
        'total': order['total'],
        'item_count': len(order['order_items'])
    })
    
    # Clear cart
    session['cart'] = {}
    session.modified = True
    
    return render_template('order_confirmation.html', order=order)

@app.route('/orders')
def orders():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user_orders = [order for order in ORDERS if order['username'] == session['username']]
    log_activity('orders_view', {'order_count': len(user_orders)})
    
    return render_template('orders.html', orders=user_orders)

@app.route('/activity_logs')
def activity_logs():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Only allow admin users to view activity logs
    if session.get('clearance_level') != 'BSL4_AUTHORIZED':
        log_activity('unauthorized_access_attempt', {'attempted_page': 'activity_logs'})
        return render_template('index.html', error='Access denied: Administrator privileges required')
    
    # Load activity logs
    try:
        with open('activity_log.json', 'r') as f:
            logs = json.load(f)
    except FileNotFoundError:
        logs = []
    
    # Reverse to show most recent first
    logs.reverse()
    
    log_activity('activity_logs_view', {'logs_count': len(logs)})
    
    return render_template('activity_logs.html', logs=logs)

@app.route('/lab_procedures')
def lab_procedures():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    log_activity('lab_procedures_view', {})
    return render_template('lab_procedures.html')

@app.route('/procedure/<procedure_name>')
def procedure_detail(procedure_name):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    log_activity('procedure_view', {'procedure': procedure_name})
    return render_template('procedure_detail.html', procedure_name=procedure_name)

@app.route('/special_order')
def special_order():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    log_activity('special_order_view', {})
    return render_template('special_order.html')

@app.route('/submit_special_order', methods=['POST'])
def submit_special_order():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Get form data
    equipment_type = request.form.get('equipment_type')
    manufacturer = request.form.get('manufacturer')
    model = request.form.get('model')
    specifications = request.form.get('specifications')
    budget_range = request.form.get('budget_range')
    timeline = request.form.get('timeline')
    additional_info = request.form.get('additional_info')
    contact_method = request.form.get('contact_method')
    
    # Create special order request
    special_order_request = {
        'id': f"SO{len(ORDERS) + 1:05d}",
        'username': session['username'],
        'timestamp': datetime.datetime.now().isoformat(),
        'equipment_type': equipment_type,
        'manufacturer': manufacturer,
        'model': model,
        'specifications': specifications,
        'budget_range': budget_range,
        'timeline': timeline,
        'additional_info': additional_info,
        'contact_method': contact_method,
        'status': 'pending_review'
    }
    
    # Save to special orders file
    special_orders_file = 'special_orders.json'
    try:
        with open(special_orders_file, 'r') as f:
            special_orders = json.load(f)
    except FileNotFoundError:
        special_orders = []
    
    special_orders.append(special_order_request)
    
    with open(special_orders_file, 'w') as f:
        json.dump(special_orders, f, indent=2)
    
    log_activity('special_order_submitted', {
        'request_id': special_order_request['id'],
        'equipment_type': equipment_type,
        'manufacturer': manufacturer,
        'model': model
    })
    
    return render_template('special_order_confirmation.html', request=special_order_request)

@app.route('/service_request/<service_type>')
def service_request(service_type):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Check authorization for BSL specialized services
    if service_type == 'bsl_specialized':
        user_clearance = session.get('clearance_level', 'BASIC')
        if user_clearance not in ['BSL3_CERTIFIED', 'BSL4_AUTHORIZED']:
            return redirect(url_for('lab_procedures'))
    
    valid_service_types = ['cell_culture', 'dna_pcr', 'microbiology', 'sterilization', 'analytical', 'bsl_specialized']
    if service_type not in valid_service_types:
        return redirect(url_for('lab_procedures'))
    
    log_activity('service_request_view', {'service_type': service_type})
    return render_template('service_request.html', service_type=service_type)

@app.route('/submit_service_request', methods=['POST'])
def submit_service_request():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Get common form data
    service_type = request.form.get('service_type')
    contact_name = request.form.get('contact_name')
    contact_email = request.form.get('contact_email')
    organization = request.form.get('organization')
    phone = request.form.get('phone', '')
    project_description = request.form.get('project_description')
    timeline = request.form.get('timeline')
    budget_range = request.form.get('budget_range')
    additional_notes = request.form.get('additional_notes', '')
    
    # Create base service request
    service_request_data = {
        'id': f"SR{len(ORDERS) + len(load_special_orders()) + 1:05d}",
        'username': session['username'],
        'clearance_level': session.get('clearance_level', 'BASIC'),
        'facility_id': session.get('facility_id', 'N/A'),
        'timestamp': datetime.datetime.now().isoformat(),
        'service_type': service_type,
        'contact_name': contact_name,
        'contact_email': contact_email,
        'organization': organization,
        'phone': phone,
        'project_description': project_description,
        'timeline': timeline,
        'budget_range': budget_range,
        'additional_notes': additional_notes,
        'status': 'pending_review'
    }
    
    # Add service-specific data
    if service_type == 'cell_culture':
        service_request_data.update({
            'cell_type': request.form.get('cell_type'),
            'culture_volume': request.form.get('culture_volume'),
            'culture_duration': request.form.get('culture_duration'),
            'special_conditions': request.form.get('special_conditions', '')
        })
    elif service_type == 'dna_pcr':
        service_request_data.update({
            'sample_type': request.form.get('sample_type'),
            'sample_quantity': request.form.get('sample_quantity'),
            'target_sequence': request.form.get('target_sequence', ''),
            'analysis_type': request.form.get('analysis_type')
        })
    elif service_type == 'microbiology':
        service_request_data.update({
            'organism_type': request.form.get('organism_type'),
            'service_needed': request.form.get('service_needed'),
            'growth_conditions': request.form.get('growth_conditions', '')
        })
    elif service_type == 'sterilization':
        service_request_data.update({
            'sterilization_method': request.form.get('sterilization_method'),
            'item_quantity': request.form.get('item_quantity'),
            'items_description': request.form.get('items_description')
        })
    elif service_type == 'analytical':
        service_request_data.update({
            'analytical_method': request.form.get('analytical_method'),
            'sample_count': request.form.get('sample_count'),
            'analytical_requirements': request.form.get('analytical_requirements')
        })
    elif service_type == 'bsl_specialized':
        # Additional security validation for BSL services
        user_clearance = session.get('clearance_level', 'BASIC')
        if user_clearance not in ['BSL3_CERTIFIED', 'BSL4_AUTHORIZED']:
            return redirect(url_for('lab_procedures'))
        
        service_request_data.update({
            'clearance_level_requested': request.form.get('clearance_level'),
            'facility_id_provided': request.form.get('facility_id'),
            'pathogen_category': request.form.get('pathogen_category'),
            'containment_level': request.form.get('containment_level'),
            'specialized_requirements': request.form.get('specialized_requirements')
        })
    
    # Save to service requests file
    service_requests_file = 'service_requests.json'
    try:
        with open(service_requests_file, 'r') as f:
            service_requests = json.load(f)
    except FileNotFoundError:
        service_requests = []
    
    service_requests.append(service_request_data)
    
    with open(service_requests_file, 'w') as f:
        json.dump(service_requests, f, indent=2)
    
    log_activity('service_request_submitted', {
        'request_id': service_request_data['id'],
        'service_type': service_type,
        'contact_name': contact_name,
        'organization': organization,
        'timeline': timeline,
        'budget_range': budget_range
    })
    
    return render_template('service_confirmation.html', 
                         request_id=service_request_data['id'],
                         service_type=service_type,
                         contact_name=contact_name,
                         contact_email=contact_email,
                         organization=organization,
                         timeline=timeline,
                         budget_range=budget_range,
                         submission_date=datetime.datetime.now().strftime('%B %d, %Y at %I:%M %p'))

def load_special_orders():
    """Load special orders from file"""
    try:
        with open('special_orders.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

if __name__ == '__main__':
    if os.environ.get('FLASK_ENV') == 'production':
        # Production mode
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port)
    else:
        # Development mode
        import socket
        hostname = socket.gethostname()
        try:
            local_ip = socket.gethostbyname(hostname)
        except:
            local_ip = "127.0.0.1"
        
        print("🧪 BioLab Associates - Laboratory Equipment Supplier")
        print("=" * 50)
        print(f"🌐 Local access: http://localhost:5000")
        print(f"🌐 Network access: http://{local_ip}:5000")
        print("📋 For public access, use ngrok: 'ngrok http 5000'")
        print("👤 Admin login: admin / biolab123")
        print("=" * 50)
        
        # Bind to all interfaces for Docker compatibility
        app.run(debug=True, host='0.0.0.0', port=5000) 