document.addEventListener("DOMContentLoaded", () => {

    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    const greetingMessage = "Hi! I'm jerryBOT. How can I assist you today?";
    chatBox.innerHTML += `<div class='bot-message'>${greetingMessage}</div>`;

    function sendMessage() {
        const userMessage = userInput.value.trim();
        if (userMessage === "") return;

        chatBox.innerHTML += `<div class='text-end'><div class='user-message'>${userMessage}</div></div>`;
        userInput.value = "";

        fetch("/get_response", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_input: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            chatBox.innerHTML += `<div class='bot-message'>${data.response}</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        })
        .catch(error => console.error("Error:", error));
    }

    sendBtn.addEventListener("click", sendMessage);

    userInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
});
