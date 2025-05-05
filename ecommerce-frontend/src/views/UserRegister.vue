<template>
    <div class="register-container">
      <div class="register-card">
        <div class="register-header">
          <h2 class="register-title">Create Account</h2>
          <p class="register-subtitle">Join the Maisonova experience</p>
        </div>
        
        <form @submit.prevent="register" class="register-form">
          <div class="form-group">
            <label for="username">Username</label>
            <div class="input-wrapper">
              <span class="input-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person" viewBox="0 0 16 16">
                  <path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6m2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0m4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4m-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664z"/>
                </svg>
              </span>
              <input 
                id="username"
                v-model="username" 
                placeholder="Choose a username" 
                class="form-input" 
                autocomplete="username"
              />
            </div>
          </div>
          
          <div class="form-group">
            <label for="password">Password</label>
            <div class="input-wrapper">
              <span class="input-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-lock" viewBox="0 0 16 16">
                  <path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2m3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2M5 8h6a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1"/>
                </svg>
              </span>
              <input 
                id="password"
                v-model="password" 
                type="password" 
                placeholder="Create a password" 
                class="form-input"
                autocomplete="new-password"
              />
            </div>
          </div>
          
          <button type="submit" class="register-button">
            <span class="button-text">Create Account</span>
            <span class="button-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-right" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8"/>
              </svg>
            </span>
          </button>
        </form>
        
        <div class="register-footer">
          <p>Already have an account? <router-link to="/login" class="login-link">Sign In</router-link></p>
        </div>
      </div>
    </div>
  </template>
    
  <script>
  import axios from '../axios'
    
  export default {
    name: 'UserRegister',
    data() {
      return {
        username: '',
        password: ''
      }
    },
    methods: {
      async register() {
        if (!this.username || !this.password) {
          alert('Please enter both username and password')
          return
        }
        
        try {
          await axios.post('register/', {
            username: this.username,
            password: this.password
          })
          alert('Registration successful! Please log in.')
          this.$router.push('/login')
        } catch (err) {
          alert('Registration failed.')
        }
      }
    }
  }
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&display=swap');
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600&display=swap');
  
  .register-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: calc(100vh - 70px);
    padding: 2rem 1rem;
    background-color: rgba(249, 246, 240, 0.6);
    background-image: linear-gradient(135deg, rgba(255,255,255,0.3) 0%, rgba(212, 201, 190, 0.1) 100%);
  }
  
  .register-card {
    width: 100%;
    max-width: 420px;
    padding: 2.8rem;
    border-radius: 0;
    background-color: rgba(255, 255, 255, 0.9);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    border: 1px solid rgba(212, 201, 190, 0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .register-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.07);
  }
  
  .register-header {
    text-align: center;
    margin-bottom: 2.5rem;
  }
  
  .register-title {
    font-family: 'Playfair Display', serif;
    font-weight: 500;
    color: #2c2a29;
    margin-bottom: 0.7rem;
    font-size: 2rem;
    letter-spacing: 1px;
  }
  
  .register-subtitle {
    color: #8a7c6d;
    font-size: 0.9rem;
    font-family: 'Montserrat', sans-serif;
    letter-spacing: 0.5px;
  }
  
  .register-form {
    margin-bottom: 2rem;
    font-family: 'Montserrat', sans-serif;
  }
  
  .form-group {
    margin-bottom: 1.8rem;
  }
  
  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #2c2a29;
    font-size: 0.85rem;
    letter-spacing: 0.8px;
    text-transform: uppercase;
  }
  
  .input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
  }
  
  .input-icon {
    position: absolute;
    left: 15px;
    color: #8a7c6d;
    font-size: 0.9rem;
  }
  
  .form-input {
    width: 100%;
    padding: 12px 15px 12px 40px;
    border: 1px solid #d4c9be;
    border-radius: 0;
    background-color: rgba(255, 255, 255, 0.8);
    font-size: 0.9rem;
    letter-spacing: 0.5px;
    transition: all 0.3s ease;
    font-family: 'Montserrat', sans-serif;
  }
  
  .form-input:focus {
    outline: none;
    border-color: #8a7c6d;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.03);
    background-color: rgba(255, 255, 255, 0.95);
  }
  
  .form-input::placeholder {
    color: #8a7c6d;
    opacity: 0.7;
  }
  
  .register-button {
    width: 100%;
    padding: 12px;
    border: none;
    border-radius: 0;
    background-color: #8a7c6d;
    color: white;
    font-weight: 500;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    justify-content: center;
    align-items: center;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    font-family: 'Montserrat', sans-serif;
  }
  
  .register-button:hover {
    background-color: #2c2a29;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  }
  
  .button-text {
    margin-right: 10px;
  }
  
  .button-icon {
    transition: transform 0.3s ease;
  }
  
  .register-button:hover .button-icon {
    transform: translateX(3px);
  }
  
  .register-footer {
    text-align: center;
    color: #8a7c6d;
    font-size: 0.85rem;
    font-family: 'Montserrat', sans-serif;
    letter-spacing: 0.5px;
  }
  
  .login-link {
    color: #2c2a29;
    font-weight: 500;
    text-decoration: none;
    transition: color 0.2s ease;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    font-size: 0.85rem;
  }
  
  .login-link:hover {
    color: #8a7c6d;
    text-decoration: underline;
  }
  
  @media (max-width: 480px) {
    .register-card {
      padding: 2rem 1.5rem;
    }
  }
  </style>