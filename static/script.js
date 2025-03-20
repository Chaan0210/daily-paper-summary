// static/script.js
const spinner = document.getElementById("spinner");
const papersContainer = document.getElementById("papersContainer");
const dateDisplay = document.getElementById("dateDisplay");
const prevLink = document.getElementById("prevLink");
const nextLink = document.getElementById("nextLink");
const noPapersMsg = document.getElementById("noPapersMsg");
const progressInfo = document.getElementById("progressInfo");

function loadDateNav(dateStr) {
  fetch(`/api/date-nav/${dateStr}`)
    .then((res) => res.json())
    .then((data) => {
      dateDisplay.textContent = dateStr;
      prevLink.href = `/papers/${data.prev_date}`;

      if (data.can_go_next) {
        nextLink.href = `/papers/${data.next_date}`;
        nextLink.classList.remove("disabled");
      } else {
        nextLink.href = "#";
        nextLink.classList.add("disabled");
      }
    })
    .catch((err) => console.error(err));
}

function loadProgress(dateStr) {
  fetch(`/api/date-progress/${dateStr}`)
    .then((res) => res.json())
    .then((data) => {
      const { total, processed } = data;
      if (total === 0) {
        progressInfo.textContent = "";
      } else {
        progressInfo.textContent = `(${processed} / ${total})`;
      }
    })
    .catch((err) => console.error(err));
}

function loadPapers(dateStr) {
  fetch(`/api/papers/${dateStr}`)
    .then((res) => res.json())
    .then((data) => {
      spinner.style.display = "none";

      if (data.length === 0) {
        papersContainer.innerHTML = "";
        noPapersMsg.style.display = "block";
        return;
      } else {
        noPapersMsg.style.display = "none";
      }

      const html = data
        .map(
          (paper) => `
            <div class="paper">
              <h2>${paper.title}</h2>
              <div class="section">
                <div class="highlight">
                    <div class="subtitle">• Upvote: ${
                      paper.num_vote || ""
                    }</div>
                </div>
              </div>
              <div class="section">
                <div class="highlight">
                    <div class="subtitle">• Abstract</div>
                </div>
                <div>${paper.translated_abstract_md}</div>
              </div>
              <div class="section">
                <div class="highlight">
                    <div class="subtitle">• Summary</div>
                </div>
                <div>${paper.summary_md}</div>
              </div>
              <div class="section">
                <div class="highlight">
                    <div class="subtitle">• Paper URL: </div>
                    
                </div>
                <a href="${paper.pdf_link}" target="_blank">${
            paper.pdf_link
          }</a>
              </div>
            </div>
          `
        )
        .join("");
      papersContainer.innerHTML = html;
    })
    .catch((err) => {
      console.error(err);
      spinner.style.display = "none";
    });
}

function initPage(dateStr) {
  loadDateNav(dateStr);
  loadPapers(dateStr);
  loadProgress(dateStr);
}
