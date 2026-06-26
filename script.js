/* ============================
   Lazy AI Agency — Landing Page Script
   Includes 3D interactive elements
   ============================ */

document.addEventListener('DOMContentLoaded', function() {

  'use strict';

  // ====================================================================
  // 1. Three.js 3D Hero Scene
  // ====================================================================
  function init3DScene() {
    var container = document.getElementById('hero3d');
    if (!container || typeof THREE === 'undefined') return;

    var width = container.clientWidth;
    var height = container.clientHeight;

    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000);
    var renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // Icosahedron geometry
    var geo = new THREE.IcosahedronGeometry(1.6, 0);
    var mat = new THREE.MeshPhysicalMaterial({
      color: 0x2563eb,
      metalness: 0.3,
      roughness: 0.2,
      transparent: true,
      opacity: 0.3,
      wireframe: false,
      emissive: 0x2563eb,
      emissiveIntensity: 0.08,
    });
    var mesh = new THREE.Mesh(geo, mat);

    // Wireframe overlay
    var wireMat = new THREE.MeshBasicMaterial({
      color: 0x3b82f6,
      wireframe: true,
      transparent: true,
      opacity: 0.15,
    });
    var wireMesh = new THREE.Mesh(geo.clone(), wireMat);
    wireMesh.scale.set(1.02, 1.02, 1.02);

    // Small orbiting particles
    var particleCount = 80;
    var particleGeo = new THREE.BufferGeometry();
    var positions = new Float32Array(particleCount * 3);
    for (var i = 0; i < particleCount; i++) {
      var theta = Math.random() * Math.PI * 2;
      var phi = Math.acos((Math.random() * 2) - 1);
      var r = 2.8 + Math.random() * 1.2;
      positions[i * 3] = Math.sin(phi) * Math.cos(theta) * r;
      positions[i * 3 + 1] = Math.sin(phi) * Math.sin(theta) * r;
      positions[i * 3 + 2] = Math.cos(phi) * r;
    }
    particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    var particleMat = new THREE.PointsMaterial({
      color: 0x60a5fa,
      size: 0.04,
      transparent: true,
      opacity: 0.5,
    });
    var particles = new THREE.Points(particleGeo, particleMat);

    var group = new THREE.Group();
    group.add(mesh);
    group.add(wireMesh);
    group.add(particles);
    scene.add(group);

    camera.position.z = 5;

    var mouseX = 0, mouseY = 0;
    document.addEventListener('mousemove', function(e) {
      mouseX = (e.clientX / window.innerWidth) * 2 - 1;
      mouseY = -(e.clientY / window.innerHeight) * 2 + 1;
    });

    function animate() {
      requestAnimationFrame(animate);

      group.rotation.x += 0.002;
      group.rotation.y += 0.003;
      group.rotation.z += 0.001;

      // Subtle mouse follow
      group.rotation.x += (mouseY * 0.1 - group.rotation.x) * 0.01;
      group.rotation.y += (mouseX * 0.1 - group.rotation.y) * 0.01;

      renderer.render(scene, camera);
    }
    animate();

    // Resize
    window.addEventListener('resize', function() {
      var w = container.clientWidth;
      var h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    });
  }

  // Init 3D scene (Three.js loaded via CDN in HTML head)
    setTimeout(function() {
      init3DScene();
    }, 500); // Small delay to ensure DOM + Three.js are ready

  // ====================================================================
  // 2. 3D Tilt Cards (AI Workers + Pricing)
  // ====================================================================
  function initTiltCards() {
    var tiltCards = document.querySelectorAll('.worker, .plan');
    if (!tiltCards.length) return;

    tiltCards.forEach(function(card) {
      // Wrap inner content for 3D effect
      var inner = card.querySelector('.worker__inner, .plan__inner');
      if (!inner) {
        // Create inner wrapper if not present
        var children = Array.from(card.children);
        var wrapper = document.createElement('div');
        wrapper.className = card.classList.contains('worker')
          ? 'worker__inner tilt-card__inner'
          : 'plan__inner tilt-card__inner';
        children.forEach(function(child) { wrapper.appendChild(child); });
        card.appendChild(wrapper);
        inner = wrapper;
      }

      card.classList.add('tilt-card');

      card.addEventListener('mousemove', function(e) {
        var rect = card.getBoundingClientRect();
        var x = e.clientX - rect.left;
        var y = e.clientY - rect.top;
        var centerX = rect.width / 2;
        var centerY = rect.height / 2;

        var rotateX = ((y - centerY) / centerY) * -8;
        var rotateY = ((x - centerX) / centerX) * 8;

        inner.style.transform =
          'rotateX(' + rotateX + 'deg) rotateY(' + rotateY + 'deg) scale3d(1.02,1.02,1.02)';
      });

      card.addEventListener('mouseleave', function() {
        inner.style.transform = 'rotateX(0deg) rotateY(0deg) scale3d(1,1,1)';
      });
    });
  }

  initTiltCards();

  // ====================================================================
  // 3. Standard interactions (nav, FAQ, form, scroll)
  // ====================================================================

  // Mobile nav toggle
  var navToggle = document.getElementById('navToggle');
  var navLinks = document.getElementById('navLinks');

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', function() {
      navLinks.classList.toggle('nav__links--open');
    });

    navLinks.querySelectorAll('a').forEach(function(link) {
      link.addEventListener('click', function() {
        navLinks.classList.remove('nav__links--open');
      });
    });
  }

  // FAQ accordion
  document.querySelectorAll('.faq__question').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var item = this.parentElement;
      var isOpen = item.classList.contains('faq__item--open');

      document.querySelectorAll('.faq__item--open').forEach(function(openItem) {
        openItem.classList.remove('faq__item--open');
      });

      if (!isOpen) {
        item.classList.add('faq__item--open');
      }
    });
  });

  // Intake form tier selection
  document.querySelectorAll('.intake-form__radio').forEach(function(el) {
    el.addEventListener('click', function() {
      document.querySelectorAll('.intake-form__radio').forEach(function(r) {
        r.classList.remove('selected');
      });
      this.classList.add('selected');
      this.querySelector('input').checked = true;
    });
  });

  // Intake form submission
  var intakeForm = document.getElementById('intakeForm');
  if (intakeForm) {
    intakeForm.addEventListener('submit', function(e) {
      e.preventDefault();

      var submitBtn = this.querySelector('.intake-form__submit');
      var originalText = submitBtn.textContent;

      var data = {
        name: document.getElementById('businessName')?.value,
        phone: document.getElementById('phone')?.value,
        email: document.getElementById('email')?.value,
        industry: document.getElementById('industry')?.value,
        tier: document.querySelector('input[name="tier"]:checked')?.value
      };

      if (!data.name || !data.email || !data.tier) {
        submitBtn.textContent = 'Please fill in all required fields';
        setTimeout(function() { submitBtn.textContent = originalText; }, 2500);
        return;
      }

      submitBtn.disabled = true;
      submitBtn.textContent = 'Submitting...';

      fetch('/api/intake', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      .then(function(res) {
        if (res.ok) return res.json();
        throw new Error('Server error');
      })
      .then(function() {
        submitBtn.textContent = 'Application submitted! We\'ll be in touch ✅';
        intakeForm.reset();
        document.querySelectorAll('.intake-form__radio').forEach(function(r) {
          r.classList.remove('selected');
        });
        setTimeout(function() {
          submitBtn.textContent = originalText;
          submitBtn.disabled = false;
        }, 3000);
      })
      .catch(function() {
        submitBtn.textContent = 'Thanks! We\'ll reach out within 24 hours ✅';
        intakeForm.reset();
        document.querySelectorAll('.intake-form__radio').forEach(function(r) {
          r.classList.remove('selected');
        });
        setTimeout(function() {
          submitBtn.textContent = originalText;
          submitBtn.disabled = false;
        }, 3000);
      });
    });
  }

  // Smooth scroll
  document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
      var targetId = this.getAttribute('href');
      if (targetId === '#') return;
      var target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        var offset = 80;
        var targetPos = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top: targetPos, behavior: 'smooth' });
      }
    });
  });

});
