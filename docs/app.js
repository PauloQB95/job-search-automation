const PAGE_SIZE = 25;
const ORGANIZATIONS = [
    "IDB",
    "World Bank",
    "United Nations System",
    "Asian Development Bank",
];

const state = {
    jobs: [],
    page: 1,
    sortColumn: "Closing Date",
    sortDirection: "ascending",
};

const filtersForm = document.querySelector("#filters");
const organizationFilter = document.querySelector("#organization-filter");
const locationFilter = document.querySelector("#location-filter");
const titleFilter = document.querySelector("#title-filter");
const closingDateFilter = document.querySelector("#closing-date-filter");
const tableBody = document.querySelector("#job-table-body");
const noResults = document.querySelector("#no-results");
const pagination = document.querySelector("#pagination");
const jobCount = document.querySelector("#job-count");

function parseDate(value) {
    if (!value) {
        return null;
    }

    const dateText = value.length === 10 ? `${value}T00:00:00Z` : value;
    const parsedDate = new Date(dateText);

    return Number.isNaN(parsedDate.getTime()) ? null : parsedDate;
}

function formatDate(value) {
    const date = parseDate(value);

    if (!date) {
        return value || "—";
    }

    return new Intl.DateTimeFormat("en-GB", {
        day: "2-digit",
        month: "short",
        year: "numeric",
        timeZone: "UTC",
    }).format(date).replace(/ /g, "-");
}

function formatTimestamp(value) {
    const timestamp = parseDate(value);

    if (!timestamp) {
        return "Last updated: Data is not yet available.";
    }

    const parts = new Intl.DateTimeFormat("en-GB", {
        day: "2-digit", month: "short", year: "numeric", hour: "2-digit",
        minute: "2-digit", hour12: false, timeZone: "UTC",
    }).formatToParts(timestamp);
    const values = Object.fromEntries(
        parts.map((part) => [part.type, part.value])
    );

    return `Last updated: ${values.day}-${values.month}-${values.year} ${
        values.hour
    }:${values.minute} UTC`;
}

function getFilteredJobs() {
    const organization = organizationFilter.value;
    const location = locationFilter.value.trim().toLocaleLowerCase();
    const title = titleFilter.value.trim().toLocaleLowerCase();
    const selectedClosingDate = parseDate(closingDateFilter.value);

    return state.jobs.filter((job) => {
        const jobClosingDate = parseDate(job["Closing Date"]);

        return (
            (!organization || job["Dataset Source"] === organization)
            && (!location || (job.Location || "").toLocaleLowerCase().includes(location))
            && (!title || (job["Job Title"] || "").toLocaleLowerCase().includes(title))
            && (!selectedClosingDate || !jobClosingDate || jobClosingDate >= selectedClosingDate)
        );
    });
}

function compareJobs(firstJob, secondJob) {
    const firstValue = firstJob[state.sortColumn] || "";
    const secondValue = secondJob[state.sortColumn] || "";

    if (state.sortColumn.endsWith("Date")) {
        const firstDate = parseDate(firstValue);
        const secondDate = parseDate(secondValue);

        if (!firstDate && !secondDate) return 0;
        if (!firstDate) return 1;
        if (!secondDate) return -1;

        const comparison = firstDate - secondDate;
        return state.sortDirection === "ascending" ? comparison : -comparison;
    }

    const comparison = firstValue.localeCompare(secondValue, undefined, {
        sensitivity: "base",
    });
    return state.sortDirection === "ascending" ? comparison : -comparison;
}

function updateSortButtons() {
    document.querySelectorAll("[data-sort]").forEach((button) => {
        const isCurrentColumn = button.dataset.sort === state.sortColumn;
        button.dataset.direction = isCurrentColumn ? state.sortDirection : "";
        button.setAttribute(
            "aria-label",
            `${button.textContent.trim()}. ${isCurrentColumn
                ? `Sorted ${state.sortDirection}. Activate to reverse order.`
                : "Activate to sort ascending."}`
        );
    });
}

function createTableCell(value) {
    const cell = document.createElement("td");

    if (value instanceof HTMLElement) {
        cell.append(value);
    } else {
        cell.textContent = value;
    }

    return cell;
}

function renderTable() {
    const filteredJobs = getFilteredJobs().sort(compareJobs);
    const totalPages = Math.max(1, Math.ceil(filteredJobs.length / PAGE_SIZE));
    state.page = Math.min(state.page, totalPages);
    const firstJobIndex = (state.page - 1) * PAGE_SIZE;
    const visibleJobs = filteredJobs.slice(firstJobIndex, firstJobIndex + PAGE_SIZE);

    tableBody.replaceChildren();
    noResults.hidden = filteredJobs.length !== 0;

    visibleJobs.forEach((job) => {
        const row = document.createElement("tr");
        const title = document.createElement(job["Application URL"] ? "a" : "span");
        title.textContent = job["Job Title"] || "Untitled job";

        if (job["Application URL"]) {
            title.href = job["Application URL"];
            title.target = "_blank";
            title.rel = "noopener noreferrer";
        }

        row.append(
            createTableCell(job.Organization || "—"),
            createTableCell(title),
            createTableCell(job.Location || "—"),
            createTableCell(formatDate(job["Posting Date"])),
            createTableCell(formatDate(job["Closing Date"]))
        );
        tableBody.append(row);
    });

    const firstResult = filteredJobs.length ? firstJobIndex + 1 : 0;
    const lastResult = Math.min(firstJobIndex + PAGE_SIZE, filteredJobs.length);
    jobCount.textContent = filteredJobs.length
        ? `Showing ${firstResult}–${lastResult} of ${filteredJobs.length} jobs`
        : "0 jobs";

    renderPagination(totalPages, filteredJobs.length);
    updateSortButtons();
}

function createPageButton(label, pageNumber, disabled) {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = label;
    button.disabled = disabled;
    button.addEventListener("click", () => {
        state.page = pageNumber;
        renderTable();
    });
    return button;
}

function renderPagination(totalPages, resultCount) {
    pagination.replaceChildren();

    if (resultCount <= PAGE_SIZE) return;

    pagination.append(createPageButton("Previous", state.page - 1, state.page === 1));

    const pageStatus = document.createElement("span");
    pageStatus.className = "page-status";
    pageStatus.textContent = `Page ${state.page} of ${totalPages}`;
    pagination.append(pageStatus);

    pagination.append(createPageButton("Next", state.page + 1, state.page === totalPages));
}

function renderSummaryCards() {
    const cards = document.querySelector("#summary-cards");
    cards.replaceChildren();

    ORGANIZATIONS.forEach((organization) => {
        const count = state.jobs.filter(
            (job) => job["Dataset Source"] === organization
        ).length;
        const card = document.createElement("article");
        const name = document.createElement("h3");
        const value = document.createElement("p");
        card.className = "summary-card";
        name.textContent = organization;
        value.textContent = `${count} ${count === 1 ? "job" : "jobs"}`;
        card.append(name, value);
        cards.append(card);
    });
}

function resetFilters() {
    filtersForm.reset();
    state.page = 1;
    state.sortColumn = "Closing Date";
    state.sortDirection = "ascending";
    renderTable();
}

function setUpInteractions() {
    ["input", "change"].forEach((eventName) => {
        filtersForm.addEventListener(eventName, () => {
            state.page = 1;
            renderTable();
        });
    });
    document.querySelector("#clear-filters").addEventListener("click", resetFilters);

    document.querySelectorAll("[data-sort]").forEach((button) => {
        button.addEventListener("click", () => {
            const selectedColumn = button.dataset.sort;
            state.sortDirection = state.sortColumn === selectedColumn
                ? (state.sortDirection === "ascending" ? "descending" : "ascending")
                : "ascending";
            state.sortColumn = selectedColumn;
            state.page = 1;
            renderTable();
        });
    });
}

async function loadJobs() {
    try {
        const response = await fetch("job_data.json", { cache: "no-store" });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        state.jobs = Array.isArray(data.jobs) ? data.jobs : [];
        document.querySelector("#last-updated").textContent = formatTimestamp(data.generatedAt);
        renderSummaryCards();
        renderTable();
    } catch (error) {
        document.querySelector("#last-updated").textContent = (
            "Last updated: The current website dataset could not be loaded."
        );
        jobCount.textContent = "Job data unavailable";
        noResults.hidden = false;
    }
}

setUpInteractions();
loadJobs();
