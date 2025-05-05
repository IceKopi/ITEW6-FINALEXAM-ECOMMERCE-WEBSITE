<template>
    <div class="container-fluid px-0">
      <!-- Hero Section with Side-aligned Text -->
      <section class="hero-section">
        <div class="container container-transparent py-5">
          <div class="row align-items-center">
            <div class="col-lg-6 col-md-7 text-start hero-content">
              <span class="badge bg-secondary mb-3 py-2 px-3">Exclusive Collection</span>
              <h1 class="display-4 fw-bold mb-3 hero-title">Elegance Wall Clock</h1>
              <p class="lead mb-4 fs-5">Starting from <span class="text-dark fw-bold">P129.00</span></p>
              <button class="btn btn-outline-dark px-4 py-2 py-md-3 fs-5">Discover Now</button>
            </div>
            <div class="col-lg-6 col-md-5 mt-4 mt-md-0 text-center">
              <!-- Image would be placed here -->
            </div>
          </div>
        </div>
      </section>
    </div>
  </template>
  
  <script>
  export default {
    name: 'HomePage'
  }
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&display=swap');
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600&display=swap');
  
  .hero-section {
    background-image: url('@/assets/bg.svg');
    background-size: cover;
    background-position: center;
    position: relative;
    min-height: 90vh;
    width: 100%;
    display: flex;
    align-items: center;
  }
  
  .hero-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    /* background-color: rgba(249, 246, 240, 0.85); */
    z-index: 0;
  }
  
  .hero-section > .container {
    position: relative;
    z-index: 1;
  }
  
  .container-transparent {
    background: transparent !important;
  }
  
  .hero-content {
    background: transparent !important; /* Ensure no background on hero content */
  }
  
  /* Font styling */
  body {
    font-family: 'Montserrat', sans-serif;
  }
  
  .hero-title {
    font-family: 'Playfair Display', serif;
    font-weight: 600;
    letter-spacing: -0.5px;
    font-size: 3.5rem;
    color: #2c2a29;
  }
  
  @media (max-width: 1199.98px) {
    .hero-title {
      font-size: 3rem;
    }
  }
  
  @media (max-width: 767.98px) {
    .hero-title {
      font-size: 2.5rem;
    }
    
    .hero-section {
      min-height: auto;
      padding: 80px 0;
    }
  }
  
  @media (max-width: 575.98px) {
    .hero-title {
      font-size: 2rem;
    }
    
    .hero-content {
      text-align: center;
      background: transparent !important; /* Reinforce no background for mobile */
    }
  }
  
  .badge {
    font-family: 'Montserrat', sans-serif;
    font-weight: 500;
    letter-spacing: 1px;
    text-transform: uppercase;
    background-color: #d4c9be !important;
    color: #2c2a29;
  }
  
  .btn {
    font-family: 'Montserrat', sans-serif;
    font-weight: 500;
    letter-spacing: 1px;
    text-transform: uppercase;
    border: 1px solid #2c2a29;
    border-radius: 0;
    transition: all 0.3s ease;
  }
  
  .btn:hover {
    background-color: #2c2a29;
    color: #f9f6f0;
  }
  
  .categories-section {
    background-color: #f9f6f0;
  }
  
  .category-card {
    background-color: #ffffff;
    transition: all 0.3s ease;
    cursor: pointer;
    height: 100%;
    border-radius: 0;
    border: none;
  }
  
  .category-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05) !important;
  }
  
  .promo-section {
    background-image: url('@/assets/bg.svg');
    background-color: #f9f6f0;
    background-size: cover;
    background-position: center;
    position: relative;
  }
  
  .promo-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(249, 246, 240, 0.9);
    z-index: 0;
  }
  
  .promo-section > .container {
    position: relative;
    z-index: 1;
  }
  
  .time-block {
    background-color: #ffffff;
    border-radius: 0;
    padding: 15px 25px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.03);
    min-width: 80px;
    border: 1px solid #d4c9be;
  }
  
  /* Add Bootstrap Icons */
  @import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css");
  </style>