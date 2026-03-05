fetch("/output")
  .then((res) => res.json())
  .then((data) => {
    const agents = {
      architect: "Architect",
      coder: "Coder",
      tester: "Tester",
    };

    const container = document.getElementById("output");
    container.innerHTML = "";

    for (const [key, label] of Object.entries(agents)) {
      const section = document.createElement("div");
      section.className = "agent-section";
      section.innerHTML = `
        <h2>${label}</h2>
        <div class="agent-output">${data[key] || "<em>Intet output endnu...</em>"}</div>
      `;
      container.appendChild(section);
    }
  });
