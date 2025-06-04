// --------------------------------------
// index hamburger script
// --------------------------------------

document.addEventListener("DOMContentLoaded", function () {
  const hamburger = document.getElementById("hamburger");
  const navbarList = document.querySelector(".navbar-list");

  hamburger.addEventListener("click", function () {
    navbarList.classList.toggle("active");
  });
  const userIcon = document.getElementById("user-icon");
  const profilePopup = document.getElementById("profile-popup");
  userIcon.addEventListener("click", function () {
    profilePopup.style.display =
      profilePopup.style.display === "none" ? "block" : "none";
  });
  document.addEventListener("click", function (event) {
    if (
      !userIcon.contains(event.target) &&
      !profilePopup.contains(event.target)
    ) {
      profilePopup.style.display = "none";
    }
  });
});

const hamburger = document.querySelector(".hamburger");
const navbarList = document.querySelector(".navbar-list");
hamburger.addEventListener("click", () => {
  navbarList.classList.toggle("active");
});

document.addEventListener("click", (e) => {
  if (!navbarList.contains(e.target) && !hamburger.contains(e.target)) {
    navbarList.classList.remove("active");
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const hamburger = document.getElementById("hamburger");
  const navbarList = document.querySelector(".navbar-list");

  hamburger.addEventListener("click", function () {
    navbarList.classList.toggle("active");
  });
});

// --------------------------------------
// Index hamburger script ends
// --------------------------------------

// --------------------------------------
// Block 5 scripts start
// --------------------------------------

document.addEventListener("DOMContentLoaded", () => {
  const blocks = document.querySelectorAll(
    ".block51, .block52, .block53, .fblock54, .block55, .block56"
  );

  blocks.forEach((block) => {
    block.addEventListener("mouseenter", () => {
      block.style.transform = "translateY(-4px) scale(1.02)";
      block.style.boxShadow = "0 12px 32px rgba(0, 0, 0, 0.15)";
    });

    block.addEventListener("mouseleave", () => {
      block.style.transform = "translateY(0) scale(1)";
      block.style.boxShadow = "0 4px 12px rgba(0, 0, 0, 0.08)";
    });

    block.addEventListener("click", () => {
      block.style.transform = "scale(1.05)";
      setTimeout(() => {
        block.style.transform = "scale(1)";
      }, 150);
    });
  });
});

function showFeature(element, title, description) {
  document
    .querySelectorAll(".block5-body li")
    .forEach((li) => li.classList.remove("active"));

  element.classList.add("active");

  const titleElement = document.getElementById("feature-title");
  const descriptionElement = document.getElementById("feature-description");

  titleElement.textContent = title;
  descriptionElement.textContent = description;

  const contentBox = document.querySelector(".block5-content");
  contentBox.style.transform = "scale(1.05)";
  setTimeout(() => {
    contentBox.style.transform = "scale(1)";
  }, 200);
}

// --------------------------------------
//block5 script end
// --------------------------------------

// --------------------------------------
//FAQ script start
// --------------------------------------

document.addEventListener("DOMContentLoaded", () => {
  const faqButtons = document.querySelectorAll(".question-button");

  faqButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const answer = button.nextElementSibling;
      const icon = button.querySelector("svg");

      const isOpen = answer.classList.contains("show");

      faqButtons.forEach((otherButton) => {
        const otherAnswer = otherButton.nextElementSibling;
        const otherIcon = otherButton.querySelector("svg");

        otherAnswer.classList.remove("show");
        otherIcon.classList.remove("rotate-180");
      });

      if (!isOpen) {
        answer.classList.add("show");
        icon.classList.add("rotate-180");
      }
    });
  });
});

// --------------------------------------
//FAQ script end
// --------------------------------------

// --------------------------------------
// onclick scroll script start
// --------------------------------------
function scrollToSection(sectionId) {
  const homeSection = document.getElementById('home');
  const targetSection = document.getElementById(sectionId);

  if (homeSection && targetSection) {
    // homeSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    setTimeout(() => {
      targetSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  }
}

document.querySelectorAll('a[href^="#"]').forEach(link => {
  const sectionId = link.getAttribute('href').substring(1);
  link.addEventListener('click', (event) => {
    event.preventDefault(); 
    scrollToSection(sectionId);
  });
});
// --------------------------------------
// onclick scroll script end
// --------------------------------------




