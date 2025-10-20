# Django to Flask Migration Plan: Weekend Project

## Current Project Analysis

Your current Django project consists of three main applications:

### Current Structure
```
config/
├── settings.py          # Django configuration
├── urls.py             # Main URL routing
├── wsgi.py/asgi.py     # WSGI/ASGI applications
└── __init__.py

portfolio/              # Portfolio display app
├── views.py           # Single index view
├── urls.py            # URL routing
├── models.py          # Empty models file
└── templates/
    └── portfolio/
        └── modern_index.html

pfa/                   # Personal Fitness Academy app
├── models.py          # ClassCategory, Class, ClassInstance models
├── views.py           # fitness_class_view with filtering
├── urls.py            # URL routing  
├── forms.py           # DayOfWeekForm, CategoryFilterForm
├── middleware.py      # Request/DB logging middleware
├── templates/
│   ├── pfa/
│   │   ├── index.html
│   │   └── _base.html
│   └── admin/
├── management/
│   └── commands/      # Custom Django commands
└── migrations/        # Database migrations

pokedex/              # Pokemon app (minimal)
├── views.py
├── models.py         # Empty
└── templates/
```

### Key Features to Migrate
1. **PFA Fitness Class Scheduler**: Complex filtering system with categories (Striking, Grappling, Fitness, Lifestyle)
2. **Database Models**: ClassCategory, Class, ClassInstance with relationships
3. **Custom Logging**: Request and database query logging middleware
4. **Admin Interface**: Django admin customizations
5. **Static Files**: Tailwind CSS, custom JavaScript, images
6. **Portfolio**: Simple static page display

---

## High-Level Migration Strategy

### 1. Architecture Approach: Modern Flask (2025)
- **Application Factory Pattern**: Flexible configuration and testing
- **Blueprint-based Modular Design**: Clean separation of concerns
- **SQLAlchemy 2.0+ with Alembic**: Modern ORM with proper migrations
- **Structured Logging**: Python's logging module with custom formatters
- **Configuration Management**: Environment-based config classes

### 2. Technology Stack Comparison

| Component | Django (Current) | Flask (Target) |
|-----------|------------------|----------------|
| Web Framework | Django 4.2.18 | Flask 3.0+ |
| ORM | Django ORM | SQLAlchemy 2.0+ |
| Database Migrations | Django Migrations | Alembic |
| URL Routing | Django URLs | Flask Blueprint routing |
| Templates | Django Templates | Jinja2 (similar syntax) |
| Static Files | Django Static Files | Flask static handling |
| Admin Interface | Django Admin | Flask-Admin or custom |
| Logging | Django Logging | Python logging |
| Forms | Django Forms | WTForms |
| Middleware | Django Middleware | Flask request hooks |

---

## Detailed Migration Breakdown

### Phase 1: Project Setup and Core Structure

#### 1.1 Project Structure Creation
```
flask_project/
├── app/
│   ├── __init__.py              # Application factory
│   ├── config.py                # Configuration classes
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py             # Base model class
│   │   └── pfa.py              # PFA models
│   ├── blueprints/
│   │   ├── __init__.py
│   │   ├── main/               # Portfolio blueprint
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── templates/
│   │   ├── pfa/                # PFA blueprint
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── forms.py
│   │   │   └── templates/
│   │   └── pokedex/            # Pokedex blueprint
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── logging.py          # Custom logging middleware
│   ├── services/
│   │   ├── __init__.py
│   │   └── pfa_service.py      # Business logic
│   └── static/                 # Static files
├── migrations/                 # Alembic migrations
├── tests/
├── requirements.txt
├── run.py                      # Application entry point
├── alembic.ini                # Migration configuration
└── .env                       # Environment variables
```

#### 1.2 Dependencies Installation
```python
# requirements.txt
Flask==3.0.3
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.7
Flask-WTF==1.2.1
WTForms==3.1.2
Flask-Admin==1.6.1            # Optional admin interface
Alembic==1.16.5
python-dotenv==1.0.1
gunicorn==23.0.0
whitenoise==6.9.0              # Static file serving
psycopg2-binary==2.9.10        # PostgreSQL adapter
```

### Phase 2: Database Migration

#### 2.1 SQLAlchemy Model Translation

**Django Model (Current):**
```python
# pfa/models.py
class ClassCategory(models.Model):
    CLASS_CATEGORIES = [
        ("Striking", "Striking"),
        ("Grappling", "Grappling"),
        ("Fitness", "Fitness"),
        ("Lifestyle", "Lifestyle"),
    ]
    category = models.CharField(max_length=10, choices=CLASS_CATEGORIES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
```

**Flask SQLAlchemy Model (Target):**
```python
# app/models/pfa.py
from datetime import datetime
from sqlalchemy import String, DateTime, Integer, Time, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel
import enum

class CategoryEnum(str, enum.Enum):
    STRIKING = "Striking"
    GRAPPLING = "Grappling"
    FITNESS = "Fitness"
    LIFESTYLE = "Lifestyle"

class ClassCategory(BaseModel):
    __tablename__ = 'pfa_classcategory'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[CategoryEnum] = mapped_column(SQLEnum(CategoryEnum))
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    classes = relationship("Class", secondary="class_categories", back_populates="class_categories")

class Class(BaseModel):
    __tablename__ = 'pfa_class'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted: Mapped[int] = mapped_column(Integer, default=0)
    
    # Relationships
    class_categories = relationship("ClassCategory", secondary="class_categories", back_populates="classes")
    instances = relationship("ClassInstance", back_populates="training_class")

class ClassInstance(BaseModel):
    __tablename__ = 'pfa_classinstance'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    training_class_id: Mapped[int] = mapped_column(ForeignKey('pfa_class.id'))
    weekday: Mapped[str] = mapped_column(String(10))  # '1'-'7' for Mon-Sun
    start_time: Mapped[datetime.time] = mapped_column(Time)
    end_time: Mapped[datetime.time] = mapped_column(Time)
    time_span: Mapped[int] = mapped_column(Integer)
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted: Mapped[int] = mapped_column(Integer, default=0)
    
    # Relationships
    training_class = relationship("Class", back_populates="instances")
    
    @property
    def weekday_display(self):
        weekdays = {
            '1': 'Monday', '2': 'Tuesday', '3': 'Wednesday',
            '4': 'Thursday', '5': 'Friday', '6': 'Saturday', '7': 'Sunday'
        }
        return weekdays.get(self.weekday, "Unknown")
```

#### 2.2 Database Migration Strategy
1. **Export Django Data**: Use Django's `dumpdata` command
2. **Create Alembic Migrations**: Auto-generate from SQLAlchemy models
3. **Data Migration Script**: Custom script to transform and load data
4. **Validation**: Compare record counts and key relationships

### Phase 3: Application Factory and Configuration

#### 3.1 Application Factory Pattern
```python
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.blueprints.main import bp as main_bp
    from app.blueprints.pfa import bp as pfa_bp
    from app.blueprints.pokedex import bp as pokedex_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(pfa_bp, url_prefix='/pfa')
    app.register_blueprint(pokedex_bp, url_prefix='/pokedex')
    
    # Register middleware
    from app.middleware.logging import register_logging_middleware
    register_logging_middleware(app)
    
    return app
```

#### 3.2 Configuration Management
```python
# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Logging configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/app.log')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    DEBUG = False
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
```

### Phase 4: Blueprint Migration

#### 4.1 PFA Blueprint (Most Complex)
```python
# app/blueprints/pfa/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from app.models.pfa import ClassInstance, ClassCategory
from app.blueprints.pfa.forms import DayOfWeekForm, CategoryFilterForm
from app.services.pfa_service import PFAService
from datetime import datetime
import logging

bp = Blueprint('pfa', __name__)
logger = logging.getLogger('pfa')

@bp.route('/', methods=['GET', 'POST'])
def fitness_class_view():
    service = PFAService()
    
    # Get current day (1-7 for Mon-Sun)
    current_day = datetime.now().weekday() + 1
    
    # Get parameters
    selected_day = int(request.args.get('day', current_day))
    selected_category = request.args.get('category', 'all')
    
    logger.info(f"Schedule view accessed from {request.remote_addr}")
    
    if request.method == 'POST':
        day_form = DayOfWeekForm(request.form)
        selected_category = request.form.get('category', 'all')
        
        if day_form.validate():
            selected_day = day_form.day_of_week.data
            return redirect(url_for('pfa.fitness_class_view', 
                                  day=selected_day, 
                                  category=selected_category))
    else:
        day_form = DayOfWeekForm(data={'day_of_week': selected_day})
    
    # Get filtered classes
    class_list = service.get_filtered_classes(selected_day, selected_category)
    
    logger.debug(f"Query returned {len(class_list)} classes")
    
    return render_template('pfa/index.html',
                         day_form=day_form,
                         class_list=class_list,
                         selected_day=selected_day,
                         selected_category=selected_category)
```

#### 4.2 Service Layer Pattern
```python
# app/services/pfa_service.py
from app.models.pfa import ClassInstance, ClassCategory, Class
from app import db
from sqlalchemy.orm import joinedload
import logging

logger = logging.getLogger('pfa')

class PFAService:
    def get_filtered_classes(self, selected_day, selected_category='all'):
        """Get classes filtered by day and category."""
        
        query = db.session.query(ClassInstance).options(
            joinedload(ClassInstance.training_class).joinedload(Class.class_categories)
        )
        
        # Filter by day
        query = query.filter(ClassInstance.weekday == str(selected_day))
        
        # Filter by category if specified
        if selected_category in ['striking', 'grappling']:
            category_name = selected_category.capitalize()
            query = query.join(ClassInstance.training_class)\
                         .join(Class.class_categories)\
                         .filter(ClassCategory.category == category_name)
        
        # Order by start time
        class_list = query.order_by(ClassInstance.start_time).all()
        
        logger.debug(f"Filtering by day={selected_day}, category={selected_category}")
        
        return class_list
```

### Phase 5: Forms Migration

#### 5.1 WTForms Implementation
```python
# app/blueprints/pfa/forms.py
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class DayOfWeekForm(FlaskForm):
    DAY_CHOICES = [
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('7', 'Sunday'),
    ]
    
    day_of_week = SelectField('Day of Week', 
                             choices=DAY_CHOICES, 
                             validators=[DataRequired()],
                             coerce=int)
    submit = SubmitField('Filter')

class CategoryFilterForm(FlaskForm):
    CATEGORY_CHOICES = [
        ('all', 'All'),
        ('striking', 'Striking'),
        ('grappling', 'Grappling'),
    ]
    
    category = SelectField('Category', 
                          choices=CATEGORY_CHOICES, 
                          validators=[DataRequired()])
    submit = SubmitField('Filter')
```

### Phase 6: Template Migration

#### 6.1 Jinja2 Template Conversion
The template syntax is very similar between Django and Jinja2, requiring minimal changes:

```html
<!-- app/blueprints/pfa/templates/pfa/index.html -->
{% extends 'pfa/_base.html' %}

{% block content %}
<script>
    var selectedCategoryGlobal = "{{ selected_category }}";
</script>
<script src="{{ url_for('static', filename='pfa/script.js') }}"></script>

<!-- app header section start -->
<div class="fixed-top" style="background-color: #1a1a1a;">
    <!-- app logo section -->
    <div class="px-10 pt-8 pb-2 flex justify-center">
        <img src="{{ url_for('static', filename='pfa/pfa-logo.png') }}" alt="pfa-logo">
    </div>
    <!-- day picker section -->
    <div class="flex justify-center text-gray-100 text-sm">
        <form method="POST" id="filterForm" class="day-picker font-semibold">
            {{ day_form.hidden_tag() }}
            {{ day_form.day_of_week }}
            <input type="hidden" id="id_category" name="category" value="{{ selected_category }}">
            <div class="button-group pt-2 pb-2">
                <button type="button" class="category-button" data-category="all">ALL</button>
                <button type="button" class="category-button" data-category="striking">STRIKING</button>
                <button type="button" class="category-button" data-category="grappling">GRAPPLING</button>
            </div>
        </form>
    </div>
</div>

<!-- app body section start -->
<div class="scrollable-content">
    <!-- class section -->
    <div class="text-gray-50 flex justify-center">
        <div>
            {% for class in class_list %}
            <!-- individual class card -->
            <div class="max-w-xs rounded-md overflow-hidden shadow-sm shadow-gray-200/10 my-2 min-w-72 max-w-72 border border-gray-200 py-2" style="background-color: #333333;">
                <div class="">
                    <p class="text-base text-gray-50 font-medium">{{ class.training_class.name }}</p>
                </div>
                <div class="flex justify-center">
                    <div>
                        <p class="text-xs text-gray-300 font-light">{{ class.start_time.strftime('%H:%M') }} - {{ class.end_time.strftime('%H:%M') }} ({{ class.time_span }} Minutes)</p>
                    </div>
                </div>
            </div>
            {% endfor %}
            <div class="pb-20"></div>
        </div>
    </div>
</div>

<!-- app footer section start -->
<footer class="fixed bottom-0 left-0 w-full text-white text-center py-2 text-xs" style="background-color: #1a1a1a;">
    <p>for the PFA family ❤️</p>
    <p>by <a href="https://www.matthewkriel.com" class="text-blue-400 hover:underline">Matthew Kriel</a></p>
</footer>
{% endblock content %}
```

### Phase 7: Middleware and Logging Migration

#### 7.1 Flask Logging Middleware
```python
# app/middleware/logging.py
import time
import logging
from flask import request, g
import json

logger = logging.getLogger('pfa')

def register_logging_middleware(app):
    @app.before_request
    def log_request_info():
        if not request.path.startswith('/pfa'):
            return
            
        g.start_time = time.time()
        
        user = 'anonymous'  # TODO: Implement user authentication
        method = request.method
        path = request.path
        query = dict(request.args.items())
        
        logger.info(
            f"REQUEST: {method} {path} from user={user} "
            f"ip={request.remote_addr} query={json.dumps(query)}"
        )
    
    @app.after_request
    def log_response_info(response):
        if not request.path.startswith('/pfa'):
            return response
            
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            duration_ms = int(duration * 1000)
            
            logger.info(
                f"RESPONSE: {request.method} {request.path} "
                f"status={response.status_code} time={duration_ms}ms"
            )
        
        return response

def setup_logging(app):
    if not app.debug and not app.testing:
        import logging
        from logging.handlers import RotatingFileHandler
        import os
        
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler('logs/pfa.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Flask PFA startup')
```

### Phase 8: Testing Strategy

#### 8.1 Unit Tests
```python
# tests/test_pfa_service.py
import unittest
from app import create_app, db
from app.models.pfa import ClassCategory, Class, ClassInstance
from app.services.pfa_service import PFAService
from app.config import TestingConfig
from datetime import time

class PFAServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test data
        self.setup_test_data()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def setup_test_data(self):
        # Create categories
        striking = ClassCategory(category='Striking')
        grappling = ClassCategory(category='Grappling')
        
        # Create classes
        boxing = Class(name='Boxing', class_categories=[striking])
        bjj = Class(name='BJJ', class_categories=[grappling])
        
        # Create instances
        boxing_monday = ClassInstance(
            training_class=boxing,
            weekday='1',
            start_time=time(18, 0),
            end_time=time(19, 0),
            time_span=60
        )
        
        db.session.add_all([striking, grappling, boxing, bjj, boxing_monday])
        db.session.commit()
    
    def test_get_filtered_classes_by_day(self):
        service = PFAService()
        classes = service.get_filtered_classes(1)  # Monday
        self.assertEqual(len(classes), 1)
        self.assertEqual(classes[0].training_class.name, 'Boxing')
    
    def test_get_filtered_classes_by_category(self):
        service = PFAService()
        classes = service.get_filtered_classes(1, 'striking')
        self.assertEqual(len(classes), 1)
        self.assertEqual(classes[0].training_class.name, 'Boxing')
```

---

## Migration Timeline and Effort Estimation

### Weekend Project Breakdown (16-20 hours)

#### Saturday (8-10 hours)
1. **Setup and Structure** (2 hours)
   - Create project structure
   - Set up virtual environment
   - Install dependencies
   - Initialize Git repository

2. **Database Migration** (3-4 hours)
   - Create SQLAlchemy models
   - Set up Alembic migrations
   - Export Django data
   - Create data transformation script
   - Import and validate data

3. **Core Application** (3-4 hours)
   - Implement application factory
   - Create configuration classes
   - Set up basic blueprints
   - Implement PFA service layer

#### Sunday (8-10 hours)
1. **PFA Blueprint Implementation** (4-5 hours)
   - Convert views to Flask routes
   - Implement forms with WTForms
   - Create service layer logic
   - Add filtering functionality

2. **Templates and Static Files** (2-3 hours)
   - Convert Django templates to Jinja2
   - Update static file references
   - Test responsive design
   - Implement JavaScript functionality

3. **Middleware and Logging** (1-2 hours)
   - Implement request logging
   - Set up structured logging
   - Add error handling

4. **Testing and Deployment** (1-2 hours)
   - Write basic unit tests
   - Test all functionality
   - Deploy to development environment
   - Document changes

---

## Key Benefits of Migration

### Technical Benefits
1. **Modern Architecture**: Application factory pattern and blueprint structure
2. **Better Testing**: Easier to mock and test individual components
3. **Flexible Configuration**: Environment-based configuration management
4. **Lighter Weight**: Flask's minimalist approach reduces overhead
5. **SQLAlchemy 2.0**: Modern ORM with better type hints and performance

### Development Benefits
1. **Learning Opportunity**: Hands-on experience with Flask ecosystem
2. **Code Organization**: Cleaner separation of concerns with services
3. **Maintainability**: Smaller, focused modules easier to maintain
4. **Documentation**: Better understanding of existing business logic

---

## Potential Challenges and Solutions

### Challenge 1: Django ORM to SQLAlchemy Translation
**Solution**: Use SQLAlchemy's modern mapped_column syntax with proper type hints

### Challenge 2: Django Admin Interface
**Solution**: Implement Flask-Admin or create simple admin views for key models

### Challenge 3: Django Middleware to Flask Hooks
**Solution**: Use Flask's before_request and after_request decorators

### Challenge 4: Complex Database Queries
**Solution**: Leverage SQLAlchemy's relationship loading strategies (joinedload, selectinload)

### Challenge 5: Template Filter Differences
**Solution**: Create custom Jinja2 filters for Django-specific functionality

---

## Post-Migration Enhancements

Once the basic migration is complete, consider these modern Flask enhancements:

1. **API Endpoints**: Add REST API using Flask-RESTful
2. **Authentication**: Implement Flask-Login for user management
3. **Caching**: Add Flask-Caching for improved performance
4. **Rate Limiting**: Use Flask-Limiter for API protection
5. **OpenAPI Documentation**: Add Flask-RESTX for API documentation
6. **Background Tasks**: Integrate Celery for asynchronous processing
7. **Real-time Features**: Add Flask-SocketIO for live updates

---

## Conclusion

This migration plan provides a comprehensive roadmap for converting your Django project to a modern Flask application following 2025 best practices. The modular blueprint structure, proper separation of concerns with service layers, and modern SQLAlchemy patterns will result in a more maintainable and scalable application.

The weekend timeline is ambitious but achievable given the relatively small scope of your current project. Focus on getting the PFA functionality working first, as it contains the most complex business logic, then tackle the simpler portfolio and pokedex components.

Remember to commit frequently during the migration process and maintain the existing functionality throughout. This will ensure you have working checkpoints to fall back to if needed.