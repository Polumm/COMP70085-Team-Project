document.addEventListener('DOMContentLoaded', () => {
    const gameBoard = document.getElementById('game-board');
    const timer = document.getElementById('time-value');
    const moveCounter = document.getElementById('moves-value');
    let gameId = null;
    let boardIsLocked = false;
    let startTime = null;
    let moves = null;
    let images = null;

    let currentlyRevealedSecretIndex = null;
    let currentlyRevealedCard = null;

    let timerInterval = null;

    let flippedCardsCount = 0;

    window.startGame = async function () {
        resetGameState();


        try {
            // Fix the number of card pairs to 10 (20 cards total)
            const numPairs = 10;
            const totalCards = numPairs * 2;


            // Call API to create a new game
            let url = null;
            if (gameId != null) {
                url = `/reset_game/${gameId}`;
            } else {
                url = "/create_default_game";
            }
            const response = await fetch(url, { method: 'POST' });
            if (!response.ok) {
                throw new Error('Failed to create game');
            }
            const newGameId = await response.json();
            gameId = newGameId;


            // Reset game state
            gameBoard.innerHTML = '';
            boardIsLocked = false;
            moves = 0;
            startTime = Date.now();


            updateMoveCounter(0);
            updateTimer(0);


            // Start the timer for the game
            if (timerInterval) {
                clearInterval(timerInterval); // Prevent existing timer from repeating
            }
            timerInterval = setInterval(() => {
                const elapsedTime = Math.floor((Date.now() - startTime) / 1000);
                updateTimer(elapsedTime);
            }, 1000); // Update timer every second

            // Fetch random images to use as card content
            const imageResponse = await fetch(`/get_random_images?count=${numPairs}`);
            if (!imageResponse.ok) {
                throw new Error('Failed to fetch images');
            }
            images = await imageResponse.json();

            // Create a fixed layout of 4 rows and 5 columns for the cards
            const rows = 4;
            const cols = 5;
            let cardIndex = 0;

            for (let row = 0; row < rows; row++) {
                const rowElement = document.createElement('div');
                rowElement.classList.add('row');
                for (let col = 0; col < cols; col++) {
                    if (cardIndex >= totalCards) break;
                    const cardElement = document.createElement('div');
                    cardElement.classList.add('card', 'flip-card');
                    cardElement.dataset.index = cardIndex;
                    cardElement.innerHTML = `
                        <div class="flip-card-inner">
                            <div class="card-front"></div>
                            <div class="card-back"></div>
                        </div>
                    `;
                    cardElement.addEventListener('click', () => flipCard(cardElement));
                    rowElement.appendChild(cardElement);
                    cardIndex++;
                }
                gameBoard.appendChild(rowElement);
            }
            // Set the timer and move counter to be visible
            document.getElementById('timer').style.opacity = 1;
            document.getElementById('move-counter').style.opacity = 1;

        } catch (error) {
            console.error('Error starting the game:', error);
        }
    }

    async function flipCard(cardElement) {
        if (boardIsLocked) return; // Prevent flipping when game is over

        moves++; // Increment the number of card flips
        updateMoveCounter(moves); // Update the card flip counter display

        // Call API to check if cards match
        try {
            const cardIndex = cardElement.dataset.index;
            const response = await fetch(`/flip/${gameId}/${cardIndex}`, {
                method: 'POST',
            });
            const secretIndex = await response.json();

            // Flipping process failed
            if (secretIndex == -1) {
                return;
            } else {
                if (currentlyRevealedSecretIndex == null) {
                    currentlyRevealedSecretIndex = secretIndex;
                    currentlyRevealedCard = cardElement;
                    cardElement.querySelector('.flip-card-inner').classList.add('flipped');
                    const cardBack = cardElement.querySelector('.card-back');
                    cardBack.innerHTML = `<img src="${images[secretIndex].url}" alt="card image">`;
                    return;
                } else {
                    if (secretIndex == currentlyRevealedSecretIndex) {
                        // show for 1 sec then remove both cards without locking the board
                        cardElement.querySelector('.flip-card-inner').classList.add('flipped');
                        const cardBack = cardElement.querySelector('.card-back');
                        cardBack.innerHTML = `<img src="${images[secretIndex].url}" alt="card image">`;

                        const tempCard = currentlyRevealedCard;
                        setTimeout(() => {
                            tempCard.style.opacity = 0.0;
                            cardElement.style.opacity = 0.0;
                        }, 1000);

                        // Increment flipped cards count
                        flippedCardsCount += 2;
                        checkAllCardsFlipped(); // Call the function to check if all cards are flipped
                    } else {
                        currentlyRevealedSecretIndex = null;
                        cardElement.querySelector('.flip-card-inner').classList.add('flipped');
                        const cardBack = cardElement.querySelector('.card-back');
                        cardBack.innerHTML = `<img src="${images[secretIndex].url}" alt="card image">`;

                        // Lock the board, wait for 1 second, then flip both cards back
                        boardIsLocked = true;
                        const tempCard = currentlyRevealedCard;
                        setTimeout(() => {
                            cardElement.querySelector('.flip-card-inner').classList.remove('flipped');
                            tempCard.querySelector('.flip-card-inner').classList.remove('flipped');
                            boardIsLocked = false;
                        }, 1000);
                    }
                    currentlyRevealedSecretIndex = null;
                    currentlyRevealedCard = null;
                }
            }
        } catch (error) {
            console.error('Failed to flip the card:', error);
            return;
        }
    }

    function checkAllCardsFlipped() {
        const totalCards = 20; // Get the total number of cards
        if (flippedCardsCount === totalCards) {
            console.log("All cards flipped!");
            gameOver();
        }
    }

    function gameOver() {
        console.log("Game over: stopping timer");
        clearInterval(timerInterval); // Stop the timer
        timerInterval = null;

        const gameOverPopup = document.getElementById("game-over-popup");
        const leaderboardBtn = document.getElementById("leaderboard");
        const submitScoreBtn = document.getElementById("submit-score");
        const returnHomeBtn = document.getElementById("return-home");
        const startNewGameBtn = document.getElementById("start-new-game");

        // Show the game over popup and leaderboard button
        gameOverPopup.classList.remove("hidden");
        leaderboardBtn.classList.remove("hidden");

        // Submit score button event listener
        submitScoreBtn.addEventListener("click", async () => {
            await submitGame(gameId);
            gameOverPopup.classList.add("hidden");
        });

        // Return home button event listener
        returnHomeBtn.addEventListener("click", () => {
            // Redirect to home page
            window.location.href = "/index.html";
        });

        // Start new game button event listener
        startNewGameBtn.addEventListener("click", () => {
            // Logic to start a new game, e.g., reset game state
            startGame();
            gameOverPopup.classList.add("hidden");
        });
    }

    function updateTimer(time) {
        timer.textContent = `${time}`; // Update the time value
    }

    function updateMoveCounter(flipCount) {
        moveCounter.textContent = `${flipCount}`; // Update the move count value
    }

    function resetGameState() {
        boardIsLocked = false;
        startTime = null;
        moves = null;
        images = null;

        currentlyRevealedSecretIndex = null;
        currentlyRevealedCard = null;

        timerInterval = null;
    }
});

async function submitGame(gameId) {
    try {
        const playerName = "default_name";
        const apiUrl = `/submit_game/${gameId}/${playerName}`;
        const response = await fetch(apiUrl, { method: 'GET', });

        if (response.ok) {
            const data = await response.json();
            console.log("Game submitted successfully:", data);
            alert("Game submitted successfully!");
        } else {
            const errorData = await response.json();
            console.error("Error submitting game:", errorData);
            alert(`Error: ${errorData.error}`);
        }
    } catch (error) {
        console.error("Network error or API call failed:", error);
        alert("An error occurred while submitting the game. Please try again later.");
    }
}


async function getTime() {
    try {
        const response = await fetch(`/get_time/${gameId}`);
        if (response.ok) {
            const time = await response.json();
            console.log('Game time:', time);
        } else {
            console.error('Failed to get game time');
        }
    } catch (error) {
        console.error('Error getting game time:', error);
    }
}

async function getFlipCount() {
    try {
        const response = await fetch(`/get_flip_count/${gameId}`);
        if (response.ok) {
            const flipCount = await response.json();
            console.log('Flip count:', flipCount);
        } else {
            console.error('Failed to get flip count');
        }
    } catch (error) {
        console.error('Error getting flip count:', error);
    }
}

async function resetGame() {
    try {
        const response = await fetch(`/reset_game/${gameId}`, { method: 'POST' });
        if (response.ok) {
            console.log('Game has been reset');
            startGame(); // Restart the game
        } else {
            console.error('Failed to reset game');
        }
    } catch (error) {
        console.error('Error resetting game:', error);
    }
}

async function detectGameFinish() {
    try {
        const response = await fetch(`/detect_game_finish/${gameId}`);
        if (response.ok) {
            const finished = await response.json();
            console.log("Game finished status:", finished); // Log the game finish status
            if (finished) {
                // Stop the timer
                console.log("Game over: stopping timer");
                clearInterval(timerInterval);
                timerInterval = null;

                // Show the game over popup
                const gameOverPopup = document.getElementById("game-over-popup");
                const leaderboardBtn = document.getElementById("leaderboard");
                const submitScoreBtn = document.getElementById("submit-score");
                const returnHomeBtn = document.getElementById("return-home");
                const startNewGameBtn = document.getElementById("start-new-game");

                // Show the game over popup and leaderboard button
                gameOverPopup.classList.remove("hidden");
                leaderboardBtn.classList.remove("hidden");

                // Submit score button event listener
                submitScoreBtn.addEventListener("click", async () => {
                    await submitGame(gameId);
                    gameOverPopup.classList.add("hidden");
                });

                // Return home button event listener
                returnHomeBtn.addEventListener("click", () => {
                    window.location.href = "/";
                });

                // Start new game button event listener
                startNewGameBtn.addEventListener("click", () => {
                    // Logic to start a new game, e.g., reset game state
                    startGame();
                    gameOverPopup.classList.add("hidden");
                });
            }
        } else {
            console.error('Failed to detect if game is finished');
        }
    } catch (error) {
        console.error('Error detecting game finish:', error);
    }
}

async function deleteGame() {
    try {
        const response = await fetch(`/delete_game/${gameId}`, { method: 'DELETE' });
        if (response.ok) {
            console.log('Game deleted successfully');
            gameId = null;
            gameBoard.innerHTML = '';
        } else {
            console.error('Failed to delete game');
        }
    } catch (error) {
        console.error('Error deleting game:', error);
    }
}


document.getElementById("enter-name-btn").addEventListener("click", function () {
    const usernameInput = document.getElementById("username");
    const username = usernameInput.value.trim();

    // Check if the username is empty
    if (!username) {
        document.getElementById("name-empty").style.display = "block";
        return;
    }

    // Hide the name entry section
    document.getElementById("name-entry").style.display = "none";

    // Display the game interface with the username
    document.getElementById("game-interface").style.display = "block";
    document.getElementById("user-name-display").textContent = username;

    // Optionally, you can store the username in local storage for use in other parts of the game
    localStorage.setItem("username", username);
});


// Function to start the game
function startGame() {
    // Hide the description and button section
    document.querySelector(".description-and-button").style.display = "none";

    // Display the game board
    document.getElementById("game-board").style.display = "block";

    alert("Game Started!");
    // Add additional game logic here
}
