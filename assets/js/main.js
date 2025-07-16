// 粒子背景（如需可扩展）
if (window.particlesJS) {
  particlesJS('tech-bg', {
    "particles": {
      "number": {"value": 60, "density": {"enable": true, "value_area": 900}},
      "color": {"value": ["#1dd1a1", "#3498db", "#fff"]},
      "shape": {"type": "circle"},
      "opacity": {"value": 0.18, "random": true},
      "size": {"value": 3, "random": true},
      "line_linked": {"enable": true, "distance": 120, "color": "#3498db", "opacity": 0.12, "width": 1},
      "move": {"enable": true, "speed": 1.2, "direction": "none", "random": false, "straight": false, "out_mode": "out"}
    },
    "interactivity": {
      "detect_on": "canvas",
      "events": {"onhover": {"enable": true, "mode": "repulse"}, "onclick": {"enable": true, "mode": "push"}},
      "modes": {"repulse": {"distance": 80, "duration": 0.4}, "push": {"particles_nb": 4}}
    },
    "retina_detect": true
  });
}
// 导航高亮
(function() {
  var links = document.querySelectorAll('.nav-archives a');
  var path = window.location.pathname;
  links.forEach(function(link) {
    if (link.getAttribute('href') && path.endsWith(link.getAttribute('href'))) {
      link.classList.add('active');
    }
  });
})(); 