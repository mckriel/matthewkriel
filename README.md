# Matthew Kriel - Portfolio Website

A modern, responsive portfolio website showcasing my experience as a Senior Software Engineer. Built with Django and featuring a clean monochrome design with dark mode support.

## Features

- **Modern Design**: Clean, contemporary UI with monochrome color scheme
- **Dark Mode**: Toggle between light and dark themes
- **Responsive Layout**: Optimized for desktop and mobile devices
- **Profile Sections**: About, Technical Skills, Work Experience, Featured Projects
- **Contact Integration**: Direct links to social profiles and resume

## Tech Stack

- **Backend**: Django 4.2.17
- **Frontend**: Modern CSS with custom properties, Font Awesome icons
- **Typography**: Plus Jakarta Sans font family
- **Deployment**: Configured for production with Gunicorn and WhiteNoise

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository
```bash
git clone https://github.com/mckriel/matthewkriel.git
cd matthewkriel
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Collect static files
```bash
python manage.py collectstatic
```

5. Run the development server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to view the portfolio.

## Project Structure

- `portfolio/` - Main Django app containing views and templates
- `static/portfolio/assets/` - CSS, JavaScript, and image files
- `pfa/` - Pride Fighting Academy PWA sub-application
- `staticfiles/` - Collected static files for production

## Deployment

The project is configured for production deployment with:
- Gunicorn WSGI server
- WhiteNoise for static file serving
- Environment-based settings

## Contact

- **Email**: mckriel@gmail.com
- **LinkedIn**: [linkedin.com/in/mckriel](https://www.linkedin.com/in/mckriel/)
- **GitHub**: [github.com/mckriel](https://github.com/mckriel)
- **Location**: Cape Town, South Africa