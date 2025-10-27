// // start move-button

document.addEventListener("mousemove", (event) => {
    const buttons = document.querySelectorAll(".button");
    const { clientX, clientY } = event;
    console.log("move button");

    buttons.forEach((button) => {
        const buttonRect = button.getBoundingClientRect();
        const centerX = buttonRect.left + buttonRect.width / 0.5;
        const centerY = buttonRect.top + buttonRect.height / 0.5;
  
        // Calculate opposite direction
        const deltaX = (centerX - clientX) *.2;
        const deltaY = (centerY - clientY) *.2;
  
        // Check if the button is being hovered
        if (button.matches(":hover")) {
            // Combine hover scale and mouse movement
            button.style.transform = `translate(${deltaX}px, ${deltaY}px) scale(1.2)`;
        } else {
            // Apply only mouse movement
            button.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
        }
    });
  });

  document.addEventListener("mousemove", (event) => {
    const buttons = document.querySelectorAll(".button2");
    const { clientX, clientY } = event;
  
    buttons.forEach((button2) => {
        const buttonRect = button2.getBoundingClientRect();
        const centerX = buttonRect.left + buttonRect.width / 0.5;
        const centerY = buttonRect.top + buttonRect.height / 0.5;
  
        // Calculate opposite direction
        const deltaX = (centerX - clientX) * 0.3;
        const deltaY = (centerY - clientY) * 0.3;
  
        // Check if the button is being hovered
        if (button2.matches(":hover")) {
            // Combine hover scale and mouse movement
            button2.style.transform = `translate(${deltaX}px, ${deltaY}px) scale(1.5)`;
        } else {
            // Apply only mouse movement
            button2.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
        }
    });
  });


  
// // end move-button

// start of stacking card

const { ScrollObserver, valueAtPercentage } = aat;
console.log("Stacking card");
const cardsContainer = document.querySelector('.cards');
const cards = document.querySelectorAll('.carded');

// Dynamically calculate CSS properties
cardsContainer.style.setProperty('--cards-count', cards.length);
cardsContainer.style.setProperty('--card-height', `${cards[0].clientHeight}px`);

cards.forEach((carded, index) => {
  const offsetTop = 110 + index * 20;
  carded.style.paddingTop = `${offsetTop}px`;

  if (index === cards.length - 1) return;

  const scaleTarget = 1 - (cards.length - 1 - index) * 0.05;
  const nextCard = cards[index + 1];
  const cardInner = carded.querySelector('.card__inner');

  ScrollObserver.Element(nextCard, {
    offsetTop,
    offsetBottom: window.innerHeight - carded.clientHeight,
  }).onScroll(({ percentageY }) => {
    cardInner.style.scale = valueAtPercentage({ from: 1, to: scaleTarget, percentage: percentageY });
    cardInner.style.filter = `brightness(${valueAtPercentage({
      from: 1,
      to: 0.8,
      percentage: percentageY,
    })})`;
  });
});

// end of stacking card

// motion nav bar
console.log("motion nav bar");
const nav = document.querySelector("nav"),
        toggleBtn = nav.querySelector(".toggle-btn");
console.log("motion nav bar");
    toggleBtn.addEventListener("click" , () =>{
      nav.classList.toggle("open");
    });

  // js code to make draggable nav
  function onDrag({movementY}) { //movementY gets mouse vertical value
    const navStyle = window.getComputedStyle(nav), //getting all css style of nav
          navTop = parseInt(navStyle.top), // getting nav top value & convert it into string
          navHeight = parseInt(navStyle.height), // getting nav height value & convert it into string
          windHeight = window.innerHeight; // getting window height

    nav.style.top = navTop > 0 ? `${navTop + movementY}px` : "1px";
    if(navTop > windHeight - navHeight){
      nav.style.top = `${windHeight - navHeight}px`;
    }
  }

  //this function will call when user click mouse's button and  move mouse on nav
  nav.addEventListener("mousedown", () =>{
    nav.addEventListener("mousemove", onDrag);
  });

  //these function will call when user relase mouse button and leave mouse from nav
  nav.addEventListener("mouseup", () =>{
    nav.removeEventListener("mousemove", onDrag);
  });
  nav.addEventListener("mouseleave", () =>{
    nav.removeEventListener("mousemove", onDrag);
  });


