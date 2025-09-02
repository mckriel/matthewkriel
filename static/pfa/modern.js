// 2025 Modern PWA JavaScript - Enhanced Interactions

document.addEventListener('DOMContentLoaded', function() {
    initializeModernInteractions();
    initializeCategoryFiltering();
    initializeFormHandling();
    initializeAccessibility();
});

// ===== MODERN INTERACTIONS ===== //

function initializeModernInteractions() {
    // Enhanced ripple effect for better feedback
    document.querySelectorAll('.ripple').forEach(element => {
        element.addEventListener('click', createRippleEffect);
    });
    
    // Smooth scroll with momentum
    const scrollableContent = document.querySelector('.scrollable-content');
    if (scrollableContent) {
        scrollableContent.style.scrollBehavior = 'smooth';
    }
    
    // Add touch feedback for mobile
    document.querySelectorAll('.class-card, .category-btn').forEach(element => {
        element.addEventListener('touchstart', function() {
            this.style.transform = 'scale(0.98)';
        });
        
        element.addEventListener('touchend', function() {
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });
}

function createRippleEffect(e) {
    const button = e.currentTarget;
    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;
    
    const ripple = document.createElement('span');
    ripple.style.cssText = `
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        left: ${x}px;
        top: ${y}px;
        width: ${size}px;
        height: ${size}px;
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    `;
    
    button.style.position = 'relative';
    button.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// Add CSS animation for ripple
if (!document.querySelector('#ripple-styles')) {
    const style = document.createElement('style');
    style.id = 'ripple-styles';
    style.textContent = `
        @keyframes ripple-animation {
            to { transform: scale(4); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
}

// ===== CATEGORY FILTERING ===== //

function initializeCategoryFiltering() {
    const categoryButtons = document.querySelectorAll('.category-btn');
    const categoryInput = document.getElementById('id_category');
    
    // Set initial active state
    const currentCategory = selectedCategoryGlobal || 'all';
    updateActiveCategory(currentCategory);
    
    categoryButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const category = this.dataset.category;
            
            // Update visual state
            updateActiveCategory(category);
            
            // Update form and submit
            if (categoryInput) {
                categoryInput.value = category;
            }
            
            // Add loading state
            showLoadingState();
            
            // Submit form with smooth transition
            setTimeout(() => {
                document.getElementById('filterForm').submit();
            }, 200);
        });
    });
}

function updateActiveCategory(activeCategory) {
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.category === activeCategory) {
            btn.classList.add('active');
        }
    });
}

function showLoadingState() {
    const classList = document.querySelector('.class-list');
    if (classList) {
        classList.style.opacity = '0.5';
        classList.style.pointerEvents = 'none';
        
        // Add loading animation
        const loader = document.createElement('div');
        loader.className = 'loading-skeleton animate-fade-in';
        loader.id = 'temp-loader';
        classList.appendChild(loader);
    }
}

// ===== FORM HANDLING ===== //

function initializeFormHandling() {
    const daySelector = document.getElementById('id_day_of_week');
    
    if (daySelector) {
        daySelector.addEventListener('change', function() {
            // Add smooth transition effect
            showLoadingState();
            
            // Submit with delay for smooth UX
            setTimeout(() => {
                document.getElementById('filterForm').submit();
            }, 300);
        });
    }
}

// ===== ACCESSIBILITY ENHANCEMENTS ===== //

function initializeAccessibility() {
    // Keyboard navigation for category buttons
    document.querySelectorAll('.category-btn').forEach(button => {
        button.setAttribute('role', 'tab');
        button.setAttribute('tabindex', '0');
        
        button.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    });
    
    // Screen reader announcements for dynamic content
    const classList = document.querySelector('.class-list');
    if (classList) {
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    announceContentChange();
                }
            });
        });
        
        observer.observe(classList, { childList: true });
    }
}

function announceContentChange() {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.className = 'sr-only';
    announcement.textContent = 'Class schedule updated';
    
    document.body.appendChild(announcement);
    
    setTimeout(() => {
        announcement.remove();
    }, 1000);
}

// ===== MODERN PWA ENHANCEMENTS ===== //

// Enhanced service worker with modern caching strategies
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/pfa/serviceworker.js')
        .then(registration => {
            console.log('PWA: Service worker registered successfully');
            
            // Check for updates
            registration.addEventListener('updatefound', () => {
                const newWorker = registration.installing;
                newWorker.addEventListener('statechange', () => {
                    if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                        showUpdateNotification();
                    }
                });
            });
        })
        .catch(error => {
            console.log('PWA: Service worker registration failed');
        });
}

function showUpdateNotification() {
    // Modern update notification
    const notification = document.createElement('div');
    notification.className = 'update-notification';
    notification.innerHTML = `
        <div style="
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--glass-white-strong);
            backdrop-filter: var(--blur-md);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-lg);
            padding: var(--space-md);
            color: var(--text-primary);
            box-shadow: var(--shadow-strong);
            z-index: 1000;
            text-align: center;
            min-width: 280px;
            animation: slideDown 0.5s ease-out;
        ">
            <div style="font-weight: 600; margin-bottom: 0.5rem;">App Updated!</div>
            <div style="font-size: 0.9rem; opacity: 0.8;">Refresh to get the latest features</div>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

// Add slide down animation
const updateStyles = document.createElement('style');
updateStyles.textContent = `
    @keyframes slideDown {
        from { transform: translateX(-50%) translateY(-100%); opacity: 0; }
        to { transform: translateX(-50%) translateY(0); opacity: 1; }
    }
    
    .sr-only {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border: 0;
    }
`;
document.head.appendChild(updateStyles);