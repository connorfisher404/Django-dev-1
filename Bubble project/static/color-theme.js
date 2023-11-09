const setTheme = (theme) => {
    document.documentElement.className = theme;
    localStorage.setItem("theme", theme);
  };

  document
    .getElementById("theme-select")
    .addEventListener("change", function () {
      setTheme(this.value);
    });

  const getTheme = () => {
    const theme = localStorage.getItem("theme");
    theme && setTheme(theme);
  };
  getTheme();