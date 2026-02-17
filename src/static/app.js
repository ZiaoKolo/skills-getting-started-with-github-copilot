document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

            // Générer la liste des participants avec icône de suppression
            let participantsHTML = "";
            if (details.participants.length > 0) {
              participantsHTML = `
                <div class="participants-section">
                  <strong>Participants&nbsp;:</strong>
                  <ul class="participants-list">
                    ${details.participants.map(email => `
                      <li class="participant-item">
                        <span class="participant-email">${email}</span>
                        <span class="delete-participant" title="Désinscrire" data-activity="${name}" data-email="${email}">🗑️</span>
                      </li>
                    `).join("")}
                  </ul>
                </div>
              `;
            } else {
              participantsHTML = `<div class="participants-section"><em>Aucun participant pour l’instant.</em></div>`;
            }

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
          ${participantsHTML}
        `;

        activitiesList.appendChild(activityCard);

        // Ajouter les gestionnaires d'événements pour la suppression après insertion dans le DOM
        const deleteIcons = activityCard.querySelectorAll('.delete-participant');
        deleteIcons.forEach(icon => {
          icon.addEventListener('click', async (e) => {
            const activityName = icon.getAttribute('data-activity');
            const participantEmail = icon.getAttribute('data-email');
            try {
              const response = await fetch(`/activities/${encodeURIComponent(activityName)}/signup?email=${encodeURIComponent(participantEmail)}`, {
                method: 'DELETE',
              });
              if (response.ok) {
                fetchActivities(); // Rafraîchir la liste
              } else {
                const result = await response.json();
                alert(result.detail || "Erreur lors de la désinscription.");
              }
            } catch (error) {
              alert("Erreur réseau lors de la désinscription.");
            }
          });
        });

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
        fetchActivities(); // Rafraîchir la liste des activités et participants
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
