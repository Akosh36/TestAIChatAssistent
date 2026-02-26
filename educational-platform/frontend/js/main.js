// Configuration and translations
const API_BASE = "http://localhost:8000/api";

const translations = {
    en: {
        welcomeTitle: "Welcome to EduAssist",
        welcomeSubtitle: "Learn with AI assistance in your preferred language",
        math: "Mathematics",
        programming: "Programming",
        science: "Science",
        history: "History",
        languages: "Languages",
        general: "General",
        signIn: "Sign In",
        logout: "Logout",
        bookmark: "🔖 Bookmark",
        askQuestion: "Ask a question...",
        send: "Send",
        back: "← Back",
        login: "Login",
        register: "Register",
        email: "Email",
        password: "Password",
        confirmPassword: "Confirm Password",
        bookmarked: "Article bookmarked!"
    },
    uz: {
        welcomeTitle: "EduAssist ga xush kelibsiz",
        welcomeSubtitle: "Sizning afzal tilida AI yordamida o'rganing",
        math: "Matematika",
        programming: "Dasturlash",
        science: "Fanlar",
        history: "Tarix",
        languages: "Tillar",
        general: "Umumiy",
        signIn: "Kirish",
        logout: "Chiqish",
        bookmark: "🔖 Saqlash",
        askQuestion: "Savol so'rang...",
        send: "Yuborish",
        back: "← Orqaga",
        login: "Kirish",
        register: "Ro'yxatdan o'tish",
        email: "Email",
        password: "Parol",
        confirmPassword: "Parolni tasdiqlang",
        bookmarked: "Maqola saqlandi!"
    },
    ru: {
        welcomeTitle: "Добро пожаловать в EduAssist",
        welcomeSubtitle: "Обучайтесь с помощью ИИ на предпочитаемом языке",
        math: "Математика",
        programming: "Программирование",
        science: "Наука",
        history: "История",
        languages: "Языки",
        general: "Общее",
        signIn: "Войти",
        logout: "Выход",
        bookmark: "🔖 Закладка",
        askQuestion: "Задайте вопрос...",
        send: "Отправить",
        back: "← Назад",
        login: "Вход",
        register: "Регистрация",
        email: "Email",
        password: "Пароль",
        confirmPassword: "Подтвердите пароль",
        bookmarked: "Статья сохранена!"
    }
};

// Section icons
const sectionIcons = {
    math: "📐",
    programming: "💻",
    science: "🔬",
    history: "📚",
    languages: "🌍",
    general: "💡"
};

// Global state
let currentLanguage = localStorage.getItem("language") || "en";
let currentUser = JSON.parse(localStorage.getItem("user")) || null;
let currentUserToken = localStorage.getItem("token") || null;

// Initialize app on page load
document.addEventListener("DOMContentLoaded", () => {
    initializeApp();
});

function initializeApp() {
    // Set current language and update UI
    setLanguage(currentLanguage);
    
    // Load sections on initial page load
    loadSections();
    
    // Set up event listeners
    setupEventListeners();
    
    // Update UI based on login state
    updateAuthUI();
}

function setLanguage(lang) {
    // Change language and update all translatable text.
    currentLanguage = lang;
    localStorage.setItem("language", lang);
    
    // Update active language button
    document.querySelectorAll(".lang-btn").forEach(btn => {
        btn.classList.remove("active");
        if (btn.dataset.lang === lang) {
            btn.classList.add("active");
        }
    });
    
    // Update translated text
    updateTranslations();
    
    // Reload content with new language
    const sectionsGrid = document.getElementById("sectionsGrid");
    const sectionContent = document.getElementById("sectionContent");
    const articleDetail = document.getElementById("articleDetail");
    
    if (sectionsGrid.children.length > 0) {
        loadSections();
    } else if (sectionContent.style.display !== "none") {
        loadSections();
    }
}

function updateTranslations() {
    // Update all UI text with translations for current language.
    const t = translations[currentLanguage];
    
    document.getElementById("welcomeTitle").textContent = t.welcomeTitle;
    document.getElementById("welcomeSubtitle").textContent = t.welcomeSubtitle;
    document.getElementById("authBtn").textContent = t.signIn;
    
    // Update chart language selector if visible
    const chatLang = document.getElementById("chatLanguage");
    if (chatLang) {
        chatLang.value = currentLanguage;
    }
}

function setupEventListeners() {
    // Language switcher
    document.querySelectorAll(".lang-btn").forEach(btn => {
        btn.addEventListener("click", (e) => {
            setLanguage(e.target.dataset.lang);
        });
    });
    
    // Auth button
    document.getElementById("authBtn").addEventListener("click", openAuthModal);
    document.getElementById("closeAuthModal").addEventListener("click", closeAuthModal);
    document.getElementById("logoutBtn")?.addEventListener("click", logout);
    
    // Auth tabs
    document.querySelectorAll(".auth-tab").forEach(tab => {
        tab.addEventListener("click", (e) => {
            const mode = e.target.dataset.tab;
            document.querySelectorAll(".auth-tab").forEach(t => t.classList.remove("active"));
            e.target.classList.add("active");
            
            document.getElementById("loginForm").style.display = mode === "login" ? "flex" : "none";
            document.getElementById("registerForm").style.display = mode === "register" ? "flex" : "none";
        });
    });
    
    // Auth forms
    document.getElementById("loginForm").addEventListener("submit", handleLogin);
    document.getElementById("registerForm").addEventListener("submit", handleRegister);
    
    // Back buttons
    document.getElementById("backBtn").addEventListener("click", backToSections);
    document.getElementById("backFromArticleBtn").addEventListener("click", backToPreviousSection);
    
    // Bookmark button
    document.getElementById("bookmarkBtn").addEventListener("click", handleBookmark);
}

async function loadSections() {
    // Load all sections from API and display as cards.
    try {
        const response = await fetch(`${API_BASE}/content/sections?language=${currentLanguage}`);
        const sections = await response.json();
        
        const grid = document.getElementById("sectionsGrid");
        grid.innerHTML = "";
        
        sections.forEach(section => {
            const card = document.createElement("div");
            card.className = "section-card";
            card.innerHTML = `
                <div class="section-icon">${sectionIcons[section.name] || "📖"}</div>
                <h3>${section.label}</h3>
                <p>Expand your knowledge in ${section.label}</p>
            `;
            card.addEventListener("click", () => loadSectionArticles(section.name));
            grid.appendChild(card);
        });
    } catch (error) {
        console.error("Error loading sections:", error);
    }
}

async function loadSectionArticles(section) {
    // Load articles for a specific section.
    try {
        const response = await fetch(`${API_BASE}/content/${section}?language=${currentLanguage}`);
        const articles = await response.json();
        
        // Hide sections grid, show section content
        document.getElementById("sectionsGrid").style.display = "none";
        document.getElementById("sectionContent").style.display = "block";
        document.getElementById("sectionTitle").textContent = translations[currentLanguage][section] || section;
        
        // Display articles
        const articlesList = document.getElementById("articlesList");
        articlesList.innerHTML = "";
        
        articles.forEach(article => {
            const card = document.createElement("div");
            card.className = "article-card";
            card.innerHTML = `
                <h3>${article.title}</h3>
                <p>${article.body.substring(0, 150)}...</p>
            `;
            card.addEventListener("click", () => loadArticleDetail(article));
            articlesList.appendChild(card);
        });
        
        // Update chat context
        document.getElementById("chatLanguage").value = currentLanguage;
        window.currentSection = section;
    } catch (error) {
        console.error("Error loading articles:", error);
    }
}

async function loadArticleDetail(article) {
    // Load and display full article detail.
    document.getElementById("sectionContent").style.display = "none";
    document.getElementById("articleDetail").style.display = "block";
    
    document.getElementById("articleTitle").textContent = article.title;
    document.getElementById("articleBody").textContent = article.body;
    
    // Store article ID for bookmarking
    window.currentArticle = article;
}

function backToSections() {
    // Go back from section view to sections grid.
    document.getElementById("sectionContent").style.display = "none";
    document.getElementById("sectionsGrid").style.display = "grid";
}

function backToPreviousSection() {
    // Go back from article detail to section articles list.
    document.getElementById("articleDetail").style.display = "none";
    document.getElementById("sectionContent").style.display = "block";
}

async function handleBookmark() {
    // Save current article to bookmarks.
    if (!currentUserToken) {
        alert("Please sign in to bookmark articles");
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/content/bookmarks`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ article_id: window.currentArticle.id, token: currentUserToken })
        });
        
        if (response.ok) {
            alert(translations[currentLanguage].bookmarked);
            document.getElementById("bookmarkBtn").textContent = "✅ Bookmarked";
        } else {
            const error = await response.json();
            alert(`Error: ${error.detail.error}`);
        }
    } catch (error) {
        console.error("Error bookmarking:", error);
    }
}

function openAuthModal() {
    // Show authentication modal.
    document.getElementById("authModal").style.display = "flex";
}

function closeAuthModal() {
    // Hide authentication modal.
    document.getElementById("authModal").style.display = "none";
}

async function handleLogin(e) {
    // Handle user login.
    e.preventDefault();
    const form = e.target;
    const email = form.querySelector("input[type='email']").value;
    const password = form.querySelector("input[type='password']").value;
    
    try {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            currentUserToken = data.token;
            currentUser = { email };
            localStorage.setItem("token", currentUserToken);
            localStorage.setItem("user", JSON.stringify(currentUser));
            updateAuthUI();
            closeAuthModal();
            form.reset();
        } else {
            const error = await response.json();
            document.getElementById("loginError").textContent = error.detail.error;
            document.getElementById("loginError").classList.add("show");
        }
    } catch (error) {
        console.error("Login error:", error);
    }
}

async function handleRegister(e) {
    // Handle user registration.
    e.preventDefault();
    const form = e.target;
    const email = form.querySelector("input[type='email']").value;
    const password = form.querySelectorAll("input[type='password']")[0].value;
    const confirmPassword = form.querySelectorAll("input[type='password']")[1].value;
    
    if (password !== confirmPassword) {
        document.getElementById("registerError").textContent = "Passwords do not match";
        document.getElementById("registerError").classList.add("show");
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });
        
        if (response.ok) {
            alert("Registration successful! Please log in.");
            form.reset();
            document.querySelectorAll(".auth-tab")[0].click(); // Switch to login tab
        } else {
            const error = await response.json();
            document.getElementById("registerError").textContent = error.detail.error;
            document.getElementById("registerError").classList.add("show");
        }
    } catch (error) {
        console.error("Registration error:", error);
    }
}

function logout() {
    // Log out current user.
    currentUserToken = null;
    currentUser = null;
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    updateAuthUI();
}

function updateAuthUI() {
    // Update UI based on login state.
    const authBtn = document.getElementById("authBtn");
    const userInfo = document.getElementById("userInfo");
    
    if (currentUserToken && currentUser) {
        authBtn.style.display = "none";
        userInfo.style.display = "flex";
        document.getElementById("userEmail").textContent = currentUser.email;
    } else {
        authBtn.style.display = "block";
        userInfo.style.display = "none";
        authBtn.textContent = translations[currentLanguage].signIn;
    }
}

// Export for use in chat.js
window.currentSection = null;
window.currentLanguage = currentLanguage;
window.currentUserToken = currentUserToken;
