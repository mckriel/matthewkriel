// Modern Portfolio JavaScript

document.addEventListener('DOMContentLoaded', function() {
    init_theme_toggle();
    init_smooth_scrolling();
    init_scroll_indicator();
    init_nav_highlighting();
    init_animations();
    init_typing_animation();
});

// ===== THEME TOGGLE =====
function init_theme_toggle() {
    const theme_toggle = document.querySelector('.theme-toggle');
    const current_theme = localStorage.getItem('theme') || 
        (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    
    // Set initial theme
    document.documentElement.setAttribute('data-theme', current_theme);
    
    if (theme_toggle) {
        theme_toggle.addEventListener('click', function() {
            const current_theme = document.documentElement.getAttribute('data-theme');
            const new_theme = current_theme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', new_theme);
            localStorage.setItem('theme', new_theme);
        });
    }
}

// ===== SMOOTH SCROLLING =====
function init_smooth_scrolling() {
    const nav_links = document.querySelectorAll('.nav-link[href^="#"]');
    
    nav_links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target_id = this.getAttribute('href');
            const target_element = document.querySelector(target_id);
            
            if (target_element) {
                const nav_height = document.querySelector('.nav').offsetHeight;
                const target_position = target_element.offsetTop - nav_height - 20;
                
                window.scrollTo({
                    top: target_position,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ===== SCROLL PROGRESS INDICATOR =====
function init_scroll_indicator() {
    const scroll_indicator = document.querySelector('.scroll-indicator');
    
    if (scroll_indicator) {
        window.addEventListener('scroll', function() {
            const scroll_total = document.documentElement.scrollHeight - window.innerHeight;
            const scroll_current = window.pageYOffset;
            const scroll_percentage = (scroll_current / scroll_total) * 100;
            
            scroll_indicator.style.width = scroll_percentage + '%';
        });
    }
}

// ===== NAVIGATION HIGHLIGHTING =====
function init_nav_highlighting() {
    const nav_links = document.querySelectorAll('.nav-link[href^="#"]');
    const sections = document.querySelectorAll('section[id]');
    
    window.addEventListener('scroll', function() {
        const current_scroll = window.pageYOffset + 100;
        
        sections.forEach(section => {
            const section_top = section.offsetTop;
            const section_height = section.offsetHeight;
            const section_id = section.getAttribute('id');
            
            if (current_scroll >= section_top && current_scroll < section_top + section_height) {
                nav_links.forEach(link => link.classList.remove('active'));
                const active_link = document.querySelector(`.nav-link[href="#${section_id}"]`);
                if (active_link) {
                    active_link.classList.add('active');
                }
            }
        });
    });
}

// ===== SCROLL ANIMATIONS =====
function init_animations() {
    const observer = new IntersectionObserver(
        function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in-up');
                }
            });
        },
        { 
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        }
    );
    
    // Observe all cards and sections
    const elements_to_animate = document.querySelectorAll('.card, .section-content, .skill-item, .project-item');
    elements_to_animate.forEach(el => observer.observe(el));
}

// ===== TYPING ANIMATION =====
function init_typing_animation() {
    const typing_element = document.querySelector('.typing-text');
    if (!typing_element) return;
    
    const texts = [
        'Senior Software Engineer',
        'Photography Enthusiast', 
        'Jiu Jitsu Practioner',
        'World of Warcraft Badass'
    ];
    
    let current_text_index = 0;
    let current_char_index = 0;
    let is_deleting = false;
    
    function type_text() {
        const current_text = texts[current_text_index];
        
        if (is_deleting) {
            typing_element.textContent = current_text.substring(0, current_char_index - 1);
            current_char_index--;
        } else {
            typing_element.textContent = current_text.substring(0, current_char_index + 1);
            current_char_index++;
        }
        
        let typing_speed = is_deleting ? 50 : 100;
        
        if (!is_deleting && current_char_index === current_text.length) {
            typing_speed = 2000; // Pause at end
            is_deleting = true;
        } else if (is_deleting && current_char_index === 0) {
            is_deleting = false;
            current_text_index = (current_text_index + 1) % texts.length;
            typing_speed = 500; // Pause before starting new text
        }
        
        setTimeout(type_text, typing_speed);
    }
    
    type_text();
}

// ===== SKILL BARS ANIMATION =====
function animate_skill_bars() {
    const skill_bars = document.querySelectorAll('.skill-progress');
    
    const observer = new IntersectionObserver(
        function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const progress_bar = entry.target;
                    const width = progress_bar.getAttribute('data-width');
                    
                    setTimeout(() => {
                        progress_bar.style.width = width + '%';
                    }, 200);
                    
                    observer.unobserve(progress_bar);
                }
            });
        },
        { threshold: 0.5 }
    );
    
    skill_bars.forEach(bar => observer.observe(bar));
}

// ===== MOBILE MENU TOGGLE =====
function init_mobile_menu() {
    const mobile_toggle = document.querySelector('.mobile-menu-toggle');
    const mobile_menu = document.querySelector('.mobile-menu');
    
    if (mobile_toggle && mobile_menu) {
        mobile_toggle.addEventListener('click', function() {
            mobile_menu.classList.toggle('active');
            mobile_toggle.classList.toggle('active');
        });
        
        // Close menu when clicking on a link
        const mobile_links = mobile_menu.querySelectorAll('a');
        mobile_links.forEach(link => {
            link.addEventListener('click', function() {
                mobile_menu.classList.remove('active');
                mobile_toggle.classList.remove('active');
            });
        });
    }
}

// ===== CONTACT FORM =====
function init_contact_form() {
    const contact_form = document.querySelector('.contact-form');
    
    if (contact_form) {
        contact_form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const form_data = new FormData(this);
            const submit_button = this.querySelector('button[type="submit"]');
            const original_text = submit_button.textContent;
            
            submit_button.textContent = 'Sending...';
            submit_button.disabled = true;
            
            // Simulate form submission (replace with actual endpoint)
            setTimeout(() => {
                submit_button.textContent = 'Message Sent!';
                contact_form.reset();
                
                setTimeout(() => {
                    submit_button.textContent = original_text;
                    submit_button.disabled = false;
                }, 2000);
            }, 1500);
        });
    }
}

// ===== UTILS =====
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize additional features when needed
document.addEventListener('DOMContentLoaded', function() {
    animate_skill_bars();
    init_mobile_menu();
    init_contact_form();
});