// 燧光知识沙龙 - 通用脚本

document.addEventListener('DOMContentLoaded', function() {
  createParticles();
});

function createParticles() {
  const container = document.getElementById('particles');
  if (!container) return;
  
  const particleCount = 30;
  
  for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    
    // 随机位置和动画参数
    particle.style.left = Math.random() * 100 + '%';
    particle.style.animationDelay = Math.random() * 8 + 's';
    particle.style.animationDuration = (6 + Math.random() * 4) + 's';
    
    // 随机大小
    const size = 2 + Math.random() * 4;
    particle.style.width = size + 'px';
    particle.style.height = size + 'px';
    
    // 随机颜色 (橙、金、红)
    const colors = ['#FF6B35', '#FFD700', '#FF4500', '#FFA500'];
    particle.style.background = colors[Math.floor(Math.random() * colors.length)];
    
    // 随机透明度
    particle.style.opacity = 0.3 + Math.random() * 0.5;
    
    container.appendChild(particle);
  }
}

// 平滑滚动
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// 卡片悬停效果增强
document.querySelectorAll('.card').forEach(card => {
  card.addEventListener('mouseenter', function() {
    this.style.transform = 'translateY(-4px)';
  });
  
  card.addEventListener('mouseleave', function() {
    this.style.transform = 'translateY(0)';
  });
});

// 打字机效果
function typeWriter(element, text, speed = 50) {
  let i = 0;
  element.textContent = '';
  
  function type() {
    if (i < text.length) {
      element.textContent += text.charAt(i);
      i++;
      setTimeout(type, speed);
    }
  }
  
  type();
}

// 懒加载图片
if ('IntersectionObserver' in window) {
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        if (img.dataset.src) {
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
        }
        observer.unobserve(img);
      }
    });
  });
  
  document.querySelectorAll('img[data-src]').forEach(img => {
    imageObserver.observe(img);
  });
}
