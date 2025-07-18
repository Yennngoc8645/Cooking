document.addEventListener("DOMContentLoaded", function(){
  const input = document.getElementById("search-input");
  const suggestionBox = document.getElementById("suggestions");

  let timeout = null;
  input.addEventListener("input", function(){
    clearTimeout(timeout);
    const val = this.value.trim();
    if (!val) {
      suggestionBox.innerHTML = "";
      return;
    }
    timeout = setTimeout(() => {
      fetch(`/ajax/autocomplete/?q=${encodeURIComponent(val)}`)
        .then(res => res.json())
        .then(data => {
          if (data.results.length > 0) {
            suggestionBox.innerHTML = data.results.map(name => `<li>${name}</li>`).join("");
            suggestionBox.style.display = "block";  // ✅ hiện suggestions
          } else {
            suggestionBox.innerHTML = "";
            suggestionBox.style.display = "none";   // ẩn nếu không có gì
          }
        });
    }, 300);  // debounce 300ms
  });

  suggestionBox.addEventListener("click", function(e){
    if (e.target.tagName === "LI") {
      input.value = e.target.textContent;
      suggestionBox.innerHTML = "";
      input.form.submit(); // Gửi form ngay
    }
  });

 document.addEventListener("click", function(e){
  if (!input.contains(e.target) && !suggestionBox.contains(e.target)) {
    suggestionBox.innerHTML = "";
    suggestionBox.style.display = "none";  // 👈 nhớ ẩn luôn
  }
});
});
