const chatBox = document.getElementById("chat-box");
const messageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");
const clearButton = document.getElementById("clear-button");
const memoryStatus = document.getElementById("memory-status");


// ============================================================
// ADD MESSAGE TO CHAT
// ============================================================

function addMessage(sender, message) {

    const messageDiv = document.createElement("div");

    messageDiv.classList.add("message");

    if (sender === "user") {
        messageDiv.classList.add("user-message");
    } else {
        messageDiv.classList.add("bot-message");
    }

    const label = document.createElement("div");
    label.classList.add("message-label");

    label.textContent =
        sender === "user" ? "You" : "AI";

    const text = document.createElement("div");
    text.classList.add("message-text");

    text.textContent = message;

    messageDiv.appendChild(label);
    messageDiv.appendChild(text);

    chatBox.appendChild(messageDiv);

    chatBox.scrollTop = chatBox.scrollHeight;
}


// ============================================================
// UPDATE MEMORY STATUS
// ============================================================

function updateMemoryStatus(count) {

    memoryStatus.textContent =
        `Memory: ${count} messages`;
}


// ============================================================
// SEND MESSAGE TO FLASK
// ============================================================

async function sendMessage() {

    const message =
        messageInput.value.trim();

    if (!message) {
        return;
    }

    addMessage("user", message);

    messageInput.value = "";

    sendButton.disabled = true;

    sendButton.textContent = "Thinking...";

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.error || "Something went wrong."
            );

        }

        addMessage(
            "bot",
            data.response
        );

        updateMemoryStatus(
            data.history_count
        );

    } catch (error) {

        addMessage(
            "bot",
            "❌ Error: " + error.message
        );

    } finally {

        sendButton.disabled = false;

        sendButton.textContent = "Send";

        messageInput.focus();
    }
}


// ============================================================
// SEND BUTTON
// ============================================================

sendButton.addEventListener(
    "click",
    sendMessage
);


// ============================================================
// ENTER KEY
// ============================================================

messageInput.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();
        }

    }
);


// ============================================================
// CLEAR CONVERSATION
// ============================================================

clearButton.addEventListener(
    "click",
    async function() {

        try {

            const response =
                await fetch("/clear", {
                    method: "POST"
                });

            const data =
                await response.json();

            if (!response.ok) {
                throw new Error(
                    data.error || "Unable to clear conversation."
                );
            }

            chatBox.innerHTML = "";

            addMessage(
                "bot",
                "Conversation cleared. 🧹\n\nLet's start a new conversation!"
            );

            updateMemoryStatus(0);

        } catch (error) {

            addMessage(
                "bot",
                "❌ Error: " + error.message
            );
        }

    }
);


// ============================================================
// CHECK MEMORY WHEN PAGE LOADS
// ============================================================

async function loadMemoryStatus() {

    try {

        const response =
            await fetch("/memory");

        const data =
            await response.json();

        updateMemoryStatus(
            data.messages_in_memory
        );

    } catch (error) {

        console.error(
            "Could not load memory status:",
            error
        );

    }
}


loadMemoryStatus();