class ThemeManager {
  constructor() {
    this.themeToggle = document.getElementById('themeToggle');
    this.currentTheme = this.getStoredTheme() || this.getPreferredTheme();
    
    this.init();
  }

  init() {
    // Set initial theme
    this.setTheme(this.currentTheme);
    
    // Add event listener
    if (this.themeToggle) {
      this.themeToggle.addEventListener('click', () => {
        this.toggleTheme();
      });
    }

    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
      if (!this.getStoredTheme()) {
        this.setTheme(e.matches ? 'dark' : 'light');
      }
    });
  }

  getStoredTheme() {
    return localStorage.getItem('theme');
  }

  getPreferredTheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    this.currentTheme = theme;

    // Update body background image based on theme
    const body = document.body;
    if (theme === 'dark') {
      body.style.backgroundImage = "url('/static/assets/bg.jpg')";
    } else {
      body.style.backgroundImage = "url('/static/assets/bg2.jpg')";
    }
    body.style.backgroundRepeat = "no-repeat";
    body.style.backgroundPosition = "center center";
    body.style.backgroundAttachment = "fixed";
    body.style.backgroundSize = "cover";

    // Update toggle button state
    this.updateToggleButton();
  }

  toggleTheme() {
    const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
    this.setTheme(newTheme);
    
    // Add a subtle animation effect
    this.animateThemeTransition();
  }

  updateToggleButton() {
    if (!this.themeToggle) return;
    
    const lightIcon = this.themeToggle.querySelector('.light-icon');
    const darkIcon = this.themeToggle.querySelector('.dark-icon');
    
    if (this.currentTheme === 'dark') {
      lightIcon && (lightIcon.style.display = 'none');
      darkIcon && (darkIcon.style.display = 'block');
    } else {
      lightIcon && (lightIcon.style.display = 'block');
      darkIcon && (darkIcon.style.display = 'none');
    }
  }

  animateThemeTransition() {
    // Add a subtle pulse effect to the toggle button
    if (this.themeToggle) {
      this.themeToggle.style.transform = 'scale(0.95)';
      setTimeout(() => {
        this.themeToggle.style.transform = 'scale(1)';
      }, 150);
    }

    // Optional: Add a brief overlay effect for smooth transition
    const overlay = document.createElement('div');
    overlay.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: ${this.currentTheme === 'dark' ? '#0f172a' : '#edf5ff'};
      pointer-events: none;
      z-index: 9999;
      opacity: 0;
      transition: opacity 0.3s ease;
    `;
    
    document.body.appendChild(overlay);
    
    // Trigger the fade effect
    requestAnimationFrame(() => {
      overlay.style.opacity = '0.1';
      setTimeout(() => {
        overlay.style.opacity = '0';
        setTimeout(() => {
          document.body.removeChild(overlay);
        }, 300);
      }, 50);
    });
  }
}

// Initialize theme manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new ThemeManager();
});

// Additional utility functions for theme-aware components
window.ThemeUtils = {
  // Get current theme
  getCurrentTheme() {
    return document.documentElement.getAttribute('data-theme') || 'light';
  },

  // Check if dark mode is active
  isDarkMode() {
    return this.getCurrentTheme() === 'dark';
  },

  // Listen for theme changes
  onThemeChange(callback) {
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.type === 'attributes' && mutation.attributeName === 'data-theme') {
          callback(this.getCurrentTheme());
        }
      });
    });

    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['data-theme']
    });

    return observer;
  },

  // Get theme-aware color values
  getThemeColor(colorName) {
    const computedStyle = getComputedStyle(document.documentElement);
    return computedStyle.getPropertyValue(`--${colorName}`).trim();
  }
};