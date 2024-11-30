const UNSPLASH_API_URL = 'https://api.unsplash.com/photos/random?count=8&client_id=amBRe7czSSZTFwnopRm0iqwa4CRLZc3lMYqIR-p15cE';

let cardImages = [];
let flippedCards = [];

async function fetchImages() {
    try {
        let response = await fetch(UNSPLASH_API_URL);
        let data = await response.json();
        cardImages = data.map(img => img.urls.small);
    } catch (error) {
        console.error('Error fetching images from Unsplash:', error);
    }
}

async function startGame() {
    // Fetch random images from Unsplash
    await fetchImages();
    
    // Duplicate images and shuffle cards
    let images = [...cardImages, ...cardImages];
    images.sort(() => 0.5 - Math.random());

    // Clear the game board
    document.getElementById('row-1').innerHTML = '';
    document.getElementById('row-2').innerHTML = '';

    // Create cards and add them to the rows
    images.forEach((image, index) => {
        let card = document.createElement('div');
        card.classList.add('card');
        card.dataset.index = index;

        let front = document.createElement('div');
        front.classList.add('front');
        front.innerText = '?';

        let img = document.createElement('img');
        img.src = image;

        card.appendChild(front);
        card.appendChild(img);

        card.addEventListener('click', () => flipCard(card));

        // Add cards to specific rows
        if (index < 8) {
            document.getElementById('row-1').appendChild(card);
        } else {
            document.getElementById('row-2').appendChild(card);
        }
    });
}

function flipCard(card) {
    if (flippedCards.length < 2 && !card.classList.contains('flipped')) {
        card.classList.add('flipped');
        flippedCards.push(card);
    }

    if (flippedCards.length === 2) {
        setTimeout(checkMatch, 1000);
    }
}

function checkMatch() {
    let [card1, card2] = flippedCards;
    let img1 = card1.querySelector('img').src;
    let img2 = card2.querySelector('img').src;

    if (img1 === img2) {
        // Cards match, leave them flipped
        flippedCards = [];
    } else {
        // Cards do not match, flip them back
        card1.classList.remove('flipped');
        card2.classList.remove('flipped');
        flippedCards = [];
    }
}
