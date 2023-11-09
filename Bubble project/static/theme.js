document.addEventListener("DOMContentLoaded", function() {
  const setTheme = (theme) => {
    const selectedTheme = theme;
    localStorage.setItem("selectedTheme", JSON.stringify(selectedTheme));
  };

  document
    .getElementById("theme-select")
    .addEventListener("change", function () {
      setTheme(this.value);
    });

  const getTheme = () => {
    const theme = JSON.parse(localStorage.getItem("selectedTheme"));
    theme && setTheme(theme);
  };
  getTheme();
});
