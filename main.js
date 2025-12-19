document.getElementById("sendButton").addEventListener("click", function () {
  const message = document.getElementById("message").value;
  if (message.trim() === "") {
    alert("Please enter text");
    return;
  }
  const entriesCount = message.split(/\s+/).filter(Boolean).length;
  fetch("api/submit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text: message }),
  })
    .then((response) => response.json())
    .then((data) => console.log("Server response:", data))
    .catch((error) => console.error("Error:", error));
  alert(`Sent ${entriesCount} entries`);
});
