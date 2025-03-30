document.addEventListener('DOMContentLoaded', function() {
    // Initialize GSAP animations
    initializeAnimations();
    
    // Animate elements when they come into view
    initializeScrollAnimations();
    
    // Initialize interactive elements
    initializeInteractiveElements();
});

// Function to initialize page animations
function initializeAnimations() {
    // Hero section animation
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        gsap.from(heroSection.querySelector('h1'), {
            duration: 1,
            y: 50,
            opacity: 0,
            ease: 'power3.out'
        });
        
        gsap.from(heroSection.querySelector('p'), {
            duration: 1,
            y: 30,
            opacity: 0,
            delay: 0.3,
            ease: 'power3.out'
        });
        
        const ctaButton = heroSection.querySelector('.btn-primary');
        if (ctaButton) {
            gsap.from(ctaButton, {
                duration: 0.8,
                y: 20,
                opacity: 0,
                delay: 0.6,
                ease: 'back.out(1.7)'
            });
        }
    }
    
    // Features section animation
    const features = document.querySelectorAll('.feature-card');
    if (features.length > 0) {
        gsap.from(features, {
            duration: 0.8,
            y: 50,
            opacity: 0,
            stagger: 0.15,
            ease: 'power3.out',
            scrollTrigger: {
                trigger: features[0].parentElement,
                start: 'top 80%'
            }
        });
    }
    
    // Dashboard cards animation
    const dashboardCards = document.querySelectorAll('.dashboard-card');
    if (dashboardCards.length > 0) {
        gsap.from(dashboardCards, {
            duration: 0.6,
            scale: 0.9,
            opacity: 0,
            stagger: 0.1,
            ease: 'power2.out',
            scrollTrigger: {
                trigger: dashboardCards[0].parentElement,
                start: 'top 80%'
            }
        });
    }
    
    // Form elements animation
    const formElements = document.querySelectorAll('.form-group, .form-check, .form-floating');
    if (formElements.length > 0) {
        gsap.from(formElements, {
            duration: 0.5,
            y: 20,
            opacity: 0,
            stagger: 0.05,
            ease: 'power2.out',
            scrollTrigger: {
                trigger: formElements[0].parentElement,
                start: 'top 80%'
            }
        });
    }
}

// Function to initialize scroll-triggered animations
function initializeScrollAnimations() {
    // Animate elements when they come into view
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    animatedElements.forEach(element => {
        let animation = element.getAttribute('data-animation') || 'fadeIn';
        let delay = element.getAttribute('data-delay') || 0;
        
        gsap.from(element, {
            duration: 0.8,
            opacity: 0,
            y: animation.includes('Up') ? 50 : 0,
            x: animation.includes('Left') ? -50 : (animation.includes('Right') ? 50 : 0),
            scale: animation.includes('Zoom') ? 0.8 : 1,
            delay: parseFloat(delay),
            ease: 'power2.out',
            scrollTrigger: {
                trigger: element,
                start: 'top 80%'
            }
        });
    });
    
    // Parallax effect for background images
    const parallaxElements = document.querySelectorAll('.parallax-bg');
    
    parallaxElements.forEach(element => {
        gsap.to(element, {
            backgroundPositionY: '30%',
            ease: 'none',
            scrollTrigger: {
                trigger: element,
                start: 'top bottom',
                end: 'bottom top',
                scrub: true
            }
        });
    });
}

// Function to initialize interactive elements
function initializeInteractiveElements() {
    // Interactive card hover effects
    const interactiveCards = document.querySelectorAll('.interactive-card');
    
    interactiveCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            gsap.to(card, {
                duration: 0.3,
                y: -10,
                boxShadow: '0 15px 30px rgba(0,0,0,0.1)',
                ease: 'power2.out'
            });
        });
        
        card.addEventListener('mouseleave', () => {
            gsap.to(card, {
                duration: 0.3,
                y: 0,
                boxShadow: '0 5px 15px rgba(0,0,0,0.1)',
                ease: 'power2.out'
            });
        });
    });
    
    // Button hover animations
    const animatedButtons = document.querySelectorAll('.btn-animated');
    
    animatedButtons.forEach(button => {
        button.addEventListener('mouseenter', () => {
            gsap.to(button, {
                duration: 0.3,
                scale: 1.05,
                ease: 'power2.out'
            });
        });
        
        button.addEventListener('mouseleave', () => {
            gsap.to(button, {
                duration: 0.3,
                scale: 1,
                ease: 'power2.out'
            });
        });
    });
    
    // Pulse animation for important elements
    const pulseElements = document.querySelectorAll('.pulse-animation');
    
    pulseElements.forEach(element => {
        gsap.to(element, {
            duration: 1.5,
            scale: 1.05,
            repeat: -1,
            yoyo: true,
            ease: 'sine.inOut'
        });
    });
    
    // Number counter animation
    const counterElements = document.querySelectorAll('.counter-number');
    
    counterElements.forEach(element => {
        const target = parseFloat(element.getAttribute('data-target'));
        
        gsap.to(element, {
            duration: 2,
            innerText: target,
            roundProps: 'innerText',
            ease: 'power2.out',
            scrollTrigger: {
                trigger: element,
                start: 'top 80%'
            },
            onUpdate: function() {
                element.innerText = Math.round(element.innerText);
            }
        });
    });
}

// Function to animate page transitions
function animatePageTransition(url) {
    // Create overlay for transition
    const overlay = document.createElement('div');
    overlay.className = 'page-transition-overlay';
    document.body.appendChild(overlay);
    
    // Animate overlay
    gsap.to(overlay, {
        duration: 0.5,
        opacity: 1,
        onComplete: function() {
            window.location.href = url;
        }
    });
}

// Function to create typewriter effect
function createTypewriterEffect(element, text, speed = 50, delay = 0) {
    const originalText = text || element.textContent;
    element.textContent = '';
    
    setTimeout(() => {
        let i = 0;
        const typeInterval = setInterval(() => {
            if (i < originalText.length) {
                element.textContent += originalText.charAt(i);
                i++;
            } else {
                clearInterval(typeInterval);
            }
        }, speed);
    }, delay);
}

// Function to create animated progress bar
function animateProgressBar(element, targetValue, duration = 1.5) {
    const bar = element.querySelector('.progress-bar');
    if (!bar) return;
    
    gsap.to(bar, {
        duration: duration,
        width: `${targetValue}%`,
        ease: 'power2.out',
        scrollTrigger: {
            trigger: element,
            start: 'top 80%'
        }
    });
}

// Expose functions to window for HTML onclick use
window.animatePageTransition = animatePageTransition;
window.createTypewriterEffect = createTypewriterEffect;
window.animateProgressBar = animateProgressBar;
