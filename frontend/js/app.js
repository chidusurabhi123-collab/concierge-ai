
const API = "/api";

const messages = document.getElementById("messages");
const welcome = document.getElementById("welcome");
const chatForm = document.getElementById("chat-form");
const questionInput = document.getElementById("question-input");

function addMessage(content, type, sources = [], ticket = null) {
    welcome.style.display = "none";

    const message = document.createElement("div");
    message.className = `message ${type}`;

    const text = document.createElement("div");
    text.textContent = content;
    message.appendChild(text);

    if (sources.length) {
        const sourceInfo = document.createElement("small");
        sourceInfo.textContent = "Sources: " + sources.map(
            source => `${source.source}${source.page ? ` (Page ${source.page})` : ""}`
        ).join(", ");
        message.appendChild(sourceInfo);
    }

    if (ticket) {
        const ticketInfo = document.createElement("small");
        ticketInfo.textContent = `Escalated to human support · Ticket: ${ticket.ticket_id}`;
        message.appendChild(ticketInfo);
    }

    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;
}

chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const question = questionInput.value.trim();
    if (!question) return;

    addMessage(question, "user");
    questionInput.value = "";

    const sendButton = document.getElementById("send-button");
    sendButton.disabled = true;
    sendButton.textContent = "Thinking...";

    try {
        const response = await fetch(`${API}/ask`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({question})
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Request failed");
        }

        addMessage(
            data.answer,
            "bot",
            data.sources || [],
            data.escalation_ticket || null
        );

    } catch (error) {
        addMessage(`Error: ${error.message}`, "bot");
    } finally {
        sendButton.disabled = false;
        sendButton.textContent = "Send ↑";
    }
});

document.querySelectorAll(".suggestion").forEach(button => {
    button.addEventListener("click", () => {
        questionInput.value = button.dataset.question;
        chatForm.requestSubmit();
    });
});


// NAVIGATION

const pageDetails = {
    chat: ["AI Assistant", "Ask questions about company policies and services."],
    orders: ["Order Tracking", "Search customer orders."],
    tickets: ["Support Tickets", "Manage escalated customer questions."]
};

document.querySelectorAll(".nav-item").forEach(button => {
    button.addEventListener("click", () => {
        const view = button.dataset.view;

        document.querySelectorAll(".nav-item").forEach(item =>
            item.classList.remove("active")
        );

        document.querySelectorAll(".view").forEach(item =>
            item.classList.remove("active")
        );

        button.classList.add("active");
        document.getElementById(`${view}-view`).classList.add("active");

        document.getElementById("page-title").textContent = pageDetails[view][0];
        document.getElementById("page-description").textContent = pageDetails[view][1];

        if (view === "tickets") loadTickets();
    });
});


// ORDER LOOKUP

document.getElementById("order-form").addEventListener("submit", async event => {
    event.preventDefault();

    const orderId = document.getElementById("order-id").value.trim();
    const result = document.getElementById("order-result");

    result.textContent = "Searching...";

    try {
        const response = await fetch(
            `${API}/orders/${encodeURIComponent(orderId)}`
        );

        const data = await response.json();

        if (!response.ok) throw new Error(data.detail || "Order lookup failed");

        result.replaceChildren();

        const card = document.createElement("div");
        card.className = "result-card";

        const heading = document.createElement("h3");
        heading.textContent = data.order_id;

        const status = document.createElement("p");
        status.textContent = `Status: ${data.status}`;

        const days = document.createElement("p");
        days.textContent = `Delivery days: ${data.delivery_days}`;

        card.append(heading, status, days);
        result.appendChild(card);

    } catch (error) {
        result.textContent = error.message;
    }
});


// ESCALATION TICKETS

async function loadTickets() {
    const container = document.getElementById("ticket-list");
    container.textContent = "Loading tickets...";

    try {
        const response = await fetch(`${API}/escalations`);
        const data = await response.json();

        if (!response.ok) throw new Error("Could not load tickets");

        container.replaceChildren();

        if (!data.tickets.length) {
            container.textContent = "No support tickets yet.";
            return;
        }

        data.tickets.forEach(ticket => {
            const card = document.createElement("div");
            card.className = "ticket-card";

            const heading = document.createElement("h3");
            heading.textContent = `Ticket ${ticket.ticket_id}`;

            const question = document.createElement("p");
            question.textContent = ticket.question;

            const reason = document.createElement("p");
            reason.textContent = `Reason: ${ticket.reason}`;

            const status = document.createElement("small");
            status.textContent = `Status: ${ticket.status} · ${ticket.created_at}`;

            card.append(heading, question, reason, status);
            container.appendChild(card);
        });

    } catch (error) {
        container.textContent = error.message;
    }
}

document.getElementById("refresh-tickets")
    .addEventListener("click", loadTickets);
