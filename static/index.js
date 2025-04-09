document.addEventListener('DOMContentLoaded', () => {
    // Initialize Lucide icons
    lucide.createIcons();

    // Theme toggle functionality with enhanced animation
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;

    themeToggle.addEventListener('click', () => {
        body.style.transition = 'background-color 0.5s ease, color 0.5s ease';
        body.classList.toggle('dark');

        // Add ripple effect to theme toggle
        const ripple = document.createElement('div');
        ripple.style.position = 'fixed';
        ripple.style.top = '0';
        ripple.style.left = '0';
        ripple.style.width = '100%';
        ripple.style.height = '100%';
        ripple.style.backgroundColor = body.classList.contains('dark') ? 'rgba(0,0,0,0.2)' : 'rgba(255,255,255,0.2)';
        ripple.style.transition = 'opacity 0.5s ease';
        ripple.style.zIndex = '999';
        document.body.appendChild(ripple);

        setTimeout(() => {
            ripple.style.opacity = '0';
            setTimeout(() => ripple.remove(), 500);
        }, 50);

        // Enhance card transitions
        const cards = document.querySelectorAll('.feature-card');
        cards.forEach((card, index) => {
            card.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
            card.style.transitionDelay = `${index * 0.05}s`;
        });
    });

    // Enhanced scroll animations with Intersection Observer
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0) scale(1)';
            }
        });
    }, observerOptions);

    // Apply enhanced animations to feature cards
    document.querySelectorAll('.feature-card').forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(50px) scale(0.95)';
        card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
        card.style.transitionDelay = `${index * 0.1}s`;
        observer.observe(card);
    });

    // Enhanced button hover effects
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', () => {
            button.style.transform = 'translateY(-4px) scale(1.05)';
            button.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        });

        button.addEventListener('mouseleave', () => {
            button.style.transform = 'translateY(0) scale(1)';
        });

        // Add click ripple effect
        button.addEventListener('click', (e) => {
            const ripple = document.createElement('div');
            const rect = button.getBoundingClientRect();

            ripple.style.position = 'absolute';
            ripple.style.width = ripple.style.height = '100px';
            ripple.style.left = `${e.clientX - rect.left - 50}px`;
            ripple.style.top = `${e.clientY - rect.top - 50}px`;
            ripple.style.backgroundColor = 'rgba(255,255,255,0.3)';
            ripple.style.borderRadius = '50%';
            ripple.style.transform = 'scale(0)';
            ripple.style.animation = 'ripple 0.6s linear';
            ripple.style.pointerEvents = 'none';

            button.style.position = 'relative';
            button.style.overflow = 'hidden';
            button.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    });

    // Add parallax effect to hero section
    const hero = document.querySelector('.hero');
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        hero.style.transform = `translateY(${scrolled * 0.5}px)`;
    });

    // Add floating animation to feature icons
    document.querySelectorAll('.feature-icon').forEach(icon => {
        icon.style.animation = 'float 3s ease-in-out infinite';
    });

    // Add CSS keyframes for ripple animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
});