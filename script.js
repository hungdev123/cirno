const snowContainer = document.getElementById("snow-container");

const SNOW_COUNT = 65;

for (let i = 0; i < SNOW_COUNT; i++) {
    const snowflake = document.createElement("span");

    snowflake.className = "snowflake";
    snowflake.textContent = "❄";

    const size = Math.random() * 12 + 6;
    const duration = Math.random() * 8 + 7;
    const delay = Math.random() * -15;

    snowflake.style.left = `${Math.random() * 100}%`;
    snowflake.style.fontSize = `${size}px`;
    snowflake.style.animationDuration = `${duration}s`;
    snowflake.style.animationDelay = `${delay}s`;
    snowflake.style.opacity = `${Math.random() * 0.55 + 0.3}`;

    snowContainer.appendChild(snowflake);
}

const cirno = document.getElementById("cirno");
const bakaSound = document.getElementById("baka-sound");

cirno.addEventListener("click", () => {
    bakaSound.currentTime = 0;
    bakaSound.play().catch(() => {});
});

cirno.addEventListener("animationend", (event) => {
    if (event.animationName === "cirno-click") {
        cirno.classList.remove("clicked");
    }
});

const music = document.getElementById("bg-music");
const musicToggle = document.getElementById("music-toggle");
const musicStatus = document.getElementById("music-status");
const musicVolume = document.getElementById("music-volume");
// const cirno = document.getElementById("cirno");

const CIRNO_STATIC = "resources/cirno.png";
const CIRNO_DANCING = "resources/cirno-fumo.gif";

music.volume = Number(musicVolume.value);

function updateMusicUI() {
    const isPlaying = !music.paused && !music.ended;

    cirno.src = isPlaying ? CIRNO_DANCING : CIRNO_STATIC;
    musicToggle.textContent = isPlaying ? "⏸️" : "▶️";
    musicToggle.setAttribute(
        "aria-label",
        isPlaying ? "Pause" : "Play"
    );
    musicStatus.textContent = isPlaying
        ? "♪ Now Playing..."
        : "♫ Music Paused";
}

musicToggle.addEventListener("click", async () => {
    if (music.paused) {
        try {
            await music.play();
        } catch (error) {
            musicStatus.textContent = "Cant";
            console.error("idk error:", error);
        }
    } else {
        music.pause();
    }

    updateMusicUI();
});

music.addEventListener("play", updateMusicUI);
music.addEventListener("pause", updateMusicUI);
music.addEventListener("ended", updateMusicUI);

musicVolume.addEventListener("input", () => {
    music.volume = Number(musicVolume.value);
});

updateMusicUI();
