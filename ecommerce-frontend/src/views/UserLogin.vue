<template>
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <h2 class="login-title">Welcome Back</h2>
          <p class="login-subtitle">Sign in to your Maisonova account</p>
        </div>
        
        <form @submit.prevent="login" class="login-form">
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
                placeholder="Enter your username" 
                class="form-input" 
                autocomplete="username"
              />
            </div>
          </div>
          
          <div class="form-group">
            <div class="password-header">
              <label for="password">Password</label>
            </div>
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
                placeholder="Enter your password" 
                class="form-input"
                autocomplete="current-password"
              />
            </div>
          </div>
          
          <button type="submit" class="login-button">
            <span class="button-text">Sign In</span>
            <span class="button-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-right" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8"/>
              </svg>
            </span>
          </button>
        </form>
        
        <div class="login-footer">
          <p>Don't have an account? <router-link to="/register" class="register-link">Register</router-link></p>
        </div>
      </div>
    </div>
  </template>
    
  <script>
  import axios from '../axios'
  import { auth } from '../auth'
  import { ref } from 'vue'
    
  export default {
    name: 'UserLogin',
    setup() {
      const username = ref('')
      const password = ref('')
      
      const login = async () => {
        if (!username.value || !password.value) {
          alert('Please enter both username and password')
          return
        }
        
        try {
          // Step 1: Get access and refresh tokens
          const res = await axios.post('token/', {
            username: username.value,
            password: password.value
          })
          localStorage.setItem('access', res.data.access)
          localStorage.setItem('refresh', res.data.refresh)
          auth.isLoggedIn = true
    
          // Step 2: Get user info
          const user = await axios.get('user/')
          localStorage.setItem('is_staff', user.data.is_staff)
          auth.isStaff = user.data.is_staff
    
          // Step 3: Redirect based on role
          window.location.href = user.data.is_staff ? '/monitor' : '/products'
        } catch (err) {
          alert('Login failed: Check your username or password.')
        }
      }
      
      return {
        username,
        password,
        login
      }
    }
  }
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&display=swap');
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600&display=swap');
  
  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: calc(100vh - 70px);
    padding: 2rem 1rem;
    background-color: rgba(249, 246, 240, 0.6);
    background-image: linear-gradient(135deg, rgba(255,255,255,0.3) 0%, rgba(212, 201, 190, 0.1) 100%);
  }
  
  .login-card {
    width: 100%;
    max-width: 420px;
    padding: 2.8rem;
    border-radius: 0;
    background-color: rgba(255, 255, 255, 0.9);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    border: 1px solid rgba(212, 201, 190, 0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .login-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.07);
  }
  
  .login-header {
    text-align: center;
    margin-bottom: 2.5rem;
  }
  
  .login-title {
    font-family: 'Playfair Display', serif;
    font-weight: 500;
    color: #2c2a29;
    margin-bottom: 0.7rem;
    font-size: 2rem;
    letter-spacing: 1px;
  }
  
  .login-subtitle {
    color: #8a7c6d;
    font-size: 0.9rem;
    font-family: 'Montserrat', sans-serif;
    letter-spacing: 0.5px;
  }
  
  .login-form {
    margin-bottom: 2rem;
    font-family: 'Montserrat', sans-serif;
  }
  
  .form-group {
    margin-bottom: 1.8rem;
  }
  
  .password-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
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
  
  .login-button {
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
  
  .login-button:hover {
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
  
  .login-button:hover .button-icon {
    transform: translateX(3px);
  }
  
  .login-footer {
    text-align: center;
    color: #8a7c6d;
    font-size: 0.85rem;
    font-family: 'Montserrat', sans-serif;
    letter-spacing: 0.5px;
  }
  
  .register-link {
    color: #2c2a29;
    font-weight: 500;
    text-decoration: none;
    transition: color 0.2s ease;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    font-size: 0.85rem;
  }
  
  .register-link:hover {
    color: #8a7c6d;
    text-decoration: underline;
  }
  
  @media (max-width: 480px) {
    .login-card {
      padding: 2rem 1.5rem;
    }
  }
  </style>