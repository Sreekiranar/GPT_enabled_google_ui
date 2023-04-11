document.getElementById("submitButton").addEventListener("click", async () => {
  const textInput = document.getElementById("textInput").value;
  displayContent("textPrompt", textInput);

  setLoadingStatus("Loading...");
  const response = await sendPromptToServer(textInput);
  setLoadingStatus("");

  displayStructuredResponse(response);
});

function displayContent(elementId, content) {
  document.getElementById(elementId).textContent = content;
}

function setLoadingStatus(status) {
  document.getElementById("loadingStatus").textContent = status;
}

async function sendPromptToServer(prompt) {
  const response = await fetch("http://127.0.0.1:5000/send_prompt", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt }),
  });
  return await response.json();
}


function displayStructuredResponse(data) {
  const apiResponseElement = document.getElementById("apiResponse");
  apiResponseElement.innerHTML = "";

  const table = document.createElement("table");

  const thead = document.createElement("thead");
  const tr = document.createElement("tr");

  ["Index", "Generated Text", "Source"].forEach(headerText => {
    const th = document.createElement("th");
    th.textContent = headerText;
    tr.appendChild(th);
  });

  thead.appendChild(tr);
  table.appendChild(thead);

  const tbody = document.createElement("tbody");

  data.forEach((result, index) => {
    const tr = document.createElement("tr");

    const indexTd = document.createElement("td");
    indexTd.textContent = index + 1;
    tr.appendChild(indexTd);

    const generatedTextTd = document.createElement("td");
    generatedTextTd.textContent = result.generated_text;
    tr.appendChild(generatedTextTd);

    const sourceTd = document.createElement("td");
    const sourceLink = document.createElement("a");
    sourceLink.href = result.source;
    sourceLink.textContent = result.source;
    sourceTd.appendChild(sourceLink);
    tr.appendChild(sourceTd);

    tbody.appendChild(tr);
  });

  table.appendChild(tbody);
  apiResponseElement.appendChild(table);
}

