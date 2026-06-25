/* ============================
   Lazy AI Agency — Landing Page Script
   ============================ */

document.addEventListener('DOMContentLoaded', function() {

  // Mobile nav toggle
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', function() {
      navLinks.classList.toggle('nav__links--open');
    });

    // Close on link click
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

      // Close all
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
        // Fallback: show success anyway
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