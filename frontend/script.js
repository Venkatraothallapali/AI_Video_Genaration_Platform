const queryInput = document.getElementById("query");
const searchBtn = document.getElementById("searchBtn");
const resultsDiv = document.getElementById("results");
const loadingDiv = document.getElementById("loading");

async function searchVideos() {
  const query = queryInput.value.trim();
  if (!query) return alert("Please enter a search query.");

  resultsDiv.innerHTML = "";
  loadingDiv.classList.remove("hidden");

  try {
    const response = await fetch("http://127.0.0.1:8000/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query })
    });

    if (!response.ok) throw new Error("Search failed.");
    const data = await response.json();
    loadingDiv.classList.add("hidden");

    if (data.results.length === 0) {
      resultsDiv.innerHTML = "<p>No results found.</p>";
      return;
    }

    data.results.forEach((item) => {
      const card = document.createElement("div");
      card.className = "video-card";
      const videoUrl = `http://127.0.0.1:8000/videos/${item.filename}`;

      card.innerHTML = `
        <h3>${item.Description}</h3>
        <video controls src="${videoUrl}" width="300"></video>
        <button class="download-btn" data-url="${videoUrl}" data-filename="${item.filename}">
          ⬇ Download
        </button>
      `;

      resultsDiv.appendChild(card);
    });

    // Download logic
    document.querySelectorAll(".download-btn").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const url = btn.getAttribute("data-url");
        const filename = btn.getAttribute("data-filename");

        const response = await fetch(url);
        const blob = await response.blob();
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        link.remove();
      });
    });

  } catch (err) {
    console.error(err);
    resultsDiv.innerHTML = "<p>Error fetching results.</p>";
    loadingDiv.classList.add("hidden");
  }
}

// Events
searchBtn.addEventListener("click", searchVideos);
queryInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") searchVideos();
});