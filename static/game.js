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

    window.startGame = async function () {
        moves = 0;
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
                    cardElement.classList.add('card');
                    cardElement.dataset.index = cardIndex;
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
        if (boardIsLocked) return;

        moves++; // 增加翻牌次数
        updateMoveCounter(moves); // 更新翻牌计数显示

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
                    // Animate the flipping process here
                    cardElement.innerHTML = `
                        <div class="card-back"><img src=${images[secretIndex]["url"]}></div>
                    `;
                    return;
                } else {
                    if (secretIndex == currentlyRevealedSecretIndex) {
                        // Show for 1 second, then remove both cards without locking the board
                        cardElement.innerHTML = `
                            <div class="card-back"><img src=${images[secretIndex]["url"]}></div>
                        `;
                        const tempCard = currentlyRevealedCard;
                        setTimeout(() => {
                            tempCard.style.opacity = 0.0;
                            cardElement.style.opacity = 0.0;
                        }, 1000);
                    } else {
                        currentlyRevealedSecretIndex = null;

                        // Animate the flipping process here
                        cardElement.innerHTML = `
                            <div class="card-back"><img src=${images[secretIndex]["url"]}></div>
                        `;

                        // Lock the board, wait for 1 second, then flip both cards back
                        boardIsLocked = true;
                        const tempCard = currentlyRevealedCard;
                        setTimeout(() => {
                            cardElement.innerHTML = null;
                            tempCard.innerHTML = null;
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

    function updateTimer(time) {
        timer.textContent = `${time}`; // Update the time value
    }

    function updateMoveCounter(flipCount) {
        moveCounter.textContent = `${flipCount}`; // Update the move count value
    }
});

async function submitGame(gameId) {
    try {
        // 设置固定的玩家姓名
        const playerName = "default_name";

        // 构建 API URL
        const apiUrl = `/submit_game/${gameId}/${playerName}`;

        // 使用 fetch 发起请求
        const response = await fetch(apiUrl, {
            method: 'GET', // 修改为实际后端需要的 HTTP 方法
        });

        // 检查响应是否成功
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
            if (finished) {
                alert('Game finished!');
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
