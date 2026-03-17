const API_URL =
  window.MOVERS_API_URL ||
  "https://2sfrxohtdi.execute-api.us-east-1.amazonaws.com/movers";

const COMPANY_NAMES = {
  AAPL: "Apple",
  AMZN: "Amazon",
  GOOGL: "Google",
  MSFT: "Microsoft",
  TSLA: "Tesla"
};

const latestDateEl = document.getElementById("latest-date");
const summaryTitleEl = document.getElementById("summary-title");
const companyLineEl = document.getElementById("company-line");
const companyNameEl = document.getElementById("company-name");
const tickerNameEl = document.getElementById("ticker-name");
const percentChangeEl = document.getElementById("percent-change");
const closingPriceEl = document.getElementById("closing-price");
const historyBodyEl = document.getElementById("history-body");
const statusMessageEl = document.getElementById("status-message");

const longDateFormatter = new Intl.DateTimeFormat("en-US", {
  month: "long",
  day: "numeric",
  year: "numeric"
});

const shortDateFormatter = new Intl.DateTimeFormat("en-US", {
  month: "short",
  day: "numeric",
  year: "numeric"
});

const currencyFormatter = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD"
});

function parseApiDate(dateString) {
  const [year, month, day] = dateString.split("-").map(Number);
  return new Date(year, month - 1, day);
}

function formatLongDate(dateString) {
  return longDateFormatter.format(parseApiDate(dateString));
}

function formatShortDate(dateString) {
  return shortDateFormatter.format(parseApiDate(dateString));
}

function formatPercentChange(value) {
  const sign = value > 0 ? "+" : "";
  return `${sign}${value.toFixed(2)}%`;
}

function getTrendClass(value) {
  if (value > 0) {
    return "positive";
  }

  if (value < 0) {
    return "negative";
  }

  return "neutral";
}

function getCompanyName(ticker) {
  return COMPANY_NAMES[ticker] || ticker;
}

function sortByNewest(data) {
  return [...data].sort((a, b) => b.date.localeCompare(a.date));
}

function renderSummary(item) {
  const companyName = getCompanyName(item.ticker);
  const trendClass = getTrendClass(item.percentChange);

  latestDateEl.textContent = formatLongDate(item.date);
  summaryTitleEl.textContent = "Top mover";
  companyLineEl.textContent = `${companyName} was the biggest move that day.`;
  companyNameEl.textContent = companyName;
  tickerNameEl.textContent = item.ticker;
  percentChangeEl.textContent = formatPercentChange(item.percentChange);
  percentChangeEl.className = `metric-value ${trendClass}`;
  closingPriceEl.textContent = currencyFormatter.format(item.closingPrice);
}

function renderHistory(data) {
  historyBodyEl.innerHTML = data
    .map((item) => {
      const companyName = getCompanyName(item.ticker);
      const trendClass = getTrendClass(item.percentChange);

      return `
        <tr>
          <td>${formatShortDate(item.date)}</td>
          <td>${companyName}</td>
          <td>${item.ticker}</td>
          <td><span class="change-pill ${trendClass}">${formatPercentChange(item.percentChange)}</span></td>
          <td>${currencyFormatter.format(item.closingPrice)}</td>
        </tr>
      `;
    })
    .join("");
}

function setStatus(message, tone = "") {
  statusMessageEl.textContent = message;
  statusMessageEl.className = tone ? `status-message ${tone}` : "status-message";
}

async function loadMovers() {
  try {
    setStatus("Loading market data...");

    const response = await fetch(API_URL, {
      method: "GET",
      mode: "cors"
    });

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    const payload = await response.json();
    const entries = Array.isArray(payload.data) ? sortByNewest(payload.data).slice(0, 7) : [];

    if (!entries.length) {
      throw new Error("No mover data was returned.");
    }

    renderSummary(entries[0]);
    renderHistory(entries);
    setStatus("");
  } catch (error) {
    latestDateEl.textContent = "Market data unavailable";
    summaryTitleEl.textContent = "Top mover";
    companyLineEl.textContent = "The app could not load the latest mover results.";
    companyNameEl.textContent = "--";
    tickerNameEl.textContent = "--";
    percentChangeEl.textContent = "--";
    percentChangeEl.className = "metric-value";
    closingPriceEl.textContent = "--";
    historyBodyEl.innerHTML = `
      <tr>
        <td colspan="5" class="table-status">Unable to load the last 7 market days.</td>
      </tr>
    `;
    setStatus(
      `Could not reach the movers API. ${error.message}`,
      "error"
    );
    console.error(error);
  }
}

loadMovers();
