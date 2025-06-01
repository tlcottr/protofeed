document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("brand-input");
  if (!input) return;

  const brands = ["Nike", "Google", "Apple", "Netflix", "Amazon"];
  let brandIndex = 0;
  let charIndex = 0;
  let isDeleting = false;

  function handleSubmit() {
    const brand = document.getElementById("brand-input").value;
    document.getElementById("loading").style.display = "block";
    document.getElementById("loading-brand").textContent = brand;
  }  

  function type() {
    const current = brands[brandIndex];
  
    if (!isDeleting) {
      charIndex++;
    } else {
      charIndex--;
    }
  
    const displayed = current.substring(0, charIndex);
    input.placeholder = displayed;
  
    if (charIndex === current.length && !isDeleting) {
      isDeleting = true;
      setTimeout(type, 1500);
      return;
    }
  
    if (isDeleting && charIndex === 0) {
      isDeleting = false;
      brandIndex = (brandIndex + 1) % brands.length;
    }
  
    setTimeout(type, isDeleting ? 60 : 80);
  }  

  type();
});
