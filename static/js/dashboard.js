// Dashboard Welcome Message

window.addEventListener("load",()=>{

    console.log("CyberShield Dashboard Loaded");

});

// Scanner Card Hover Animation

document.querySelectorAll(".scanner-card").forEach(card=>{

    card.addEventListener("mouseenter",()=>{
        card.style.transform="translateY(-8px)";
    });

    card.addEventListener("mouseleave",()=>{
        card.style.transform="translateY(0px)";
    });

});