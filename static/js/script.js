console.log("CyberShield AI Loaded");

// Welcome animation
window.onload = () => {
    document.querySelectorAll(".tool-card").forEach(card=>{
        card.addEventListener("mouseenter",()=>{
            card.style.transform="scale(1.03)";
        });

        card.addEventListener("mouseleave",()=>{
            card.style.transform="scale(1)";
        });
    });
};