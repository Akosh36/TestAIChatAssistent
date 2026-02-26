// Chat widget functionality

const API_BASE = "http://localhost:8000/api";

const chatToggle = document.getElementById("chatToggle");
const chatDrawer = document.getElementById("chatDrawer");
const messageInput = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const chatMessages = document.getElementById("chatMessages");
const chatLanguage = document.getElementById("chatLanguage");

// Toggle chat drawer
chatToggle.addEventListener("click", () => {
    if (chatDrawer.style.display === "none") {
        chatDrawer.style.display = "flex";
        messageInput.focus();
    } else {
        chatDrawer.style.display = "none";
    }
});

// Send message on button click
sendBtn.addEventListener("click", sendMessage);

// Send message on Enter key
messageInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Load chat history from localStorage on page load
window.addEventListener("load", () => {
    loadChatHistory();
});

function sendMessage() {
    // Send user message and get AI response.
    const message = messageInput.value.trim();
    
    if (!message) {
        return;
    }
    
    // Display user message
    addMessageToChat("user", message);
    messageInput.value = "";
    
    // Show typing indicator
    showTypingIndicator();
    
    // Get response from AI
    getAIResponse(message);
}

function addMessageToChat(role, content) {
    // Add a message to the chat display.
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${role}`;
    
    const contentDiv = document.createElement("div");
    contentDiv.className = "message-content";
    contentDiv.textContent = content;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Auto-scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Save to localStorage
    saveChatHistory();
}

function showTypingIndicator() {
    // Show animated typing indicator.
    const messageDiv = document.createElement("div");
    messageDiv.className = "message assistant";
    messageDiv.id = "typing-indicator";
    
    const contentDiv = document.createElement("div");
    contentDiv.className = "message-content";
    contentDiv.innerHTML = '<div class="typing-indicator"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div></div>';
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
    // Remove typing indicator when response arrives.
    const indicator = document.getElementById("typing-indicator");
    if (indicator) {
        indicator.remove();
    }
}

async function getAIResponse(message) {
    // Get AI response from backend.
    try {
        const section = window.currentSection || "general";
        const language = document.getElementById("chatLanguage").value;
        
        const response = await fetch(`${API_BASE}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: message,
                section: section,
                language: language,
                token: window.currentUserToken || null
            })
        });
        
        removeTypingIndicator();
        
        if (response.ok) {
            const data = await response.json();
            addMessageToChat("assistant", data.reply);
        } else {
            const error = await response.json();
            addMessageToChat("assistant", `Error: ${error.detail?.error || "Unable to get response"}`);
        }
    } catch (error) {
        removeTypingIndicator();
        console.error("Chat error:", error);
        addMessageToChat("assistant", "Sorry, I encountered an error. Please try again.");
    }
}

function saveChatHistory() {
    // Save chat history to localStorage.
    const messages = [];
    document.querySelectorAll(".message").forEach(msg => {
        if (!msg.id) {
            const role = msg.classList.contains("user") ? "user" : "assistant";
            const content = msg.querySelector(".message-content").textContent;
            messages.push({ role, content });
        }
    });
    localStorage.setItem("chatHistory", JSON.stringify(messages));
}

function loadChatHistory() {
    // Load chat history from localStorage.
    const history = JSON.parse(localStorage.getItem("chatHistory")) || [];
    history.forEach(msg => {
        addMessageToChat(msg.role, msg.content);
    });
}

function clearChatHistory() {
    // Clear chat history.
    chatMessages.innerHTML = "";
    localStorage.removeItem("chatHistory");
}

// Expose functions for main.js
window.currentSection = null;
