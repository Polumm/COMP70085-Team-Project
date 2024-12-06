document.addEventListener('DOMContentLoaded', () => {
    const gameBoard = document.getElementById('game-board');
    const timer = document.getElementById('timer');
    const moveCounter = document.getElementById('move-counter');
    let gameId = null;
    let boardIsLocked = false;
    let startTime = null;
    let moves = null;
    let images = null;

    let currentlyRevealedSecretIndex = null;
    let currentlyRevealedCard = null;

    window.startGame = async function () {
        moves = 0;
        try {
            // 固定卡牌数量为 10 对（20 张卡片）
            const numPairs = 10;
            const totalCards = numPairs * 2;

            // 调用 API 创建新游戏
            let url = null;
            if (gameId != null) {
                url = `/reset_game/${gameId}`;
            } else {
                url = "/create_default_game";
            }
            const response = await fetch(url, { method: 'POST' });
            // const response = await fetch(`/create_game/2`, { method: 'POST' });
            if (!response.ok) {
                throw new Error('Failed to create game');
            }
            const newGameId = await response.json();
            gameId = newGameId;

            // 重置游戏状态
            gameBoard.innerHTML = '';
            boardIsLocked = false;
            moves = 0;
            startTime = Date.now();

            // 获取随机图片作为卡片内容
            const imageResponse = await fetch(`/get_random_images?count=${numPairs}`);
            if (!imageResponse.ok) {
                throw new Error('Failed to fetch images');
            }
            images = await imageResponse.json();

            // 生成游戏卡片
            let cards = generateCardArray(numPairs);
            // cards = shuffle(cards);

            // 固定生成 4 行 5 列的卡片布局
            const rows = 4;
            const cols = 5;
            let cardIndex = 0;

            for (let row = 0; row < rows; row++) {
                const rowElement = document.createElement('div');
                rowElement.classList.add('row');
                for (let col = 0; col < cols; col++) {
                    if (cardIndex >= totalCards) break;
                    const card = cards[cardIndex];
                    const cardElement = document.createElement('div');
                    cardElement.classList.add('card','flip-card');
                    // cardElement.classList.add('card');
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
        } catch (error) {
            console.error('Error starting the game:', error);
        }
    }

    async function flipCard(cardElement) {
        // if (lockBoard || cardElement.classList.contains('flipped')) return;
        //
        // // 显示翻转的卡片
        // cardElement.classList.add('flipped');
        // lockBoard = true;
        // moves++;
        if (boardIsLocked)
            return;

        // 调用 API 检查卡片是否匹配
        try {
            const cardIndex = cardElement.dataset.index;
            const response = await fetch(`/flip/${gameId}/${cardIndex}`, {
                method: 'POST',
            });
            const secretIndex = await response.json();

            // flipping process failed
            if (secretIndex == -1) {
                return;
            } else {
                if (currentlyRevealedSecretIndex == null) {
                    currentlyRevealedSecretIndex = secretIndex;
                    currentlyRevealedCard = cardElement;
                    // animate the flipping process here
                    cardElement.querySelector('.flip-card-inner').classList.add('flipped');
                    const cardBack = cardElement.querySelector('.card-back');
                    cardBack.innerHTML = `<img src="${images[secretIndex].url}" alt="card image">`;

                    // cardElement.innerHTML = `
                    //     <div class="card-back"><img src=${images[secretIndex]["url"]}></div>
                    // `;

                    return;
                } else {
                    if (secretIndex == currentlyRevealedSecretIndex) {
                        // show for 1 sec then remove both cards without locking the board
                        cardElement.querySelector('.flip-card-inner').classList.add('flipped');
                        const cardBack = cardElement.querySelector('.card-back');
                        cardBack.innerHTML = `<img src="${images[secretIndex].url}" alt="card image">`;

                        const tempCard = currentlyRevealedCard;
                        setTimeout(() => {
                            // tempCard.innerHTML = null;
                            // cardElement.innerHTML = null;
                            tempCard.style.opacity = 0.0;
                            cardElement.style.opacity = 0.0;
                        }, 1000);
                    } else {
                        currentlyRevealedSecretIndex = null;

                        // animate the flipping process here
                        cardElement.querySelector('.flip-card-inner').classList.add('flipped');
                        const cardBack = cardElement.querySelector('.card-back');
                        cardBack.innerHTML = `<img src="${images[secretIndex].url}" alt="card image">`;

                        // cardElement.innerHTML = `
                        //     <div class="card-back"><img src=${images[secretIndex]["url"]}></div>
                        // `;

                        // lock the board, wait for 1 sec then flip both back
                        boardIsLocked = true;
                        const tempCard = currentlyRevealedCard;
                        setTimeout(() => {
                            cardElement.querySelector('.flip-card-inner').classList.remove('flipped');
                            cardBack.innerHTML = null;
                            tempCard.querySelector('.flip-card-inner').classList.remove('flipped');
                            tempCard.querySelector('.card-back').innerHTML = null;
                            boardIsLocked = false;
                        }, 1000);
                    }
                    currentlyRevealedSecretIndex = null;
                    currentlyRevealedCard = null;
                }
            }
        } catch (error) {
            console.error('Failed to flip the card:', error);
            // setTimeout(() => {
            //     cardElement.classList.remove('flipped');
            //     boardIsLocked = false;
            // }, 1000);
            return;
        }
    }

    async function submitScore() {
        try {
            const completionTime = (Date.now() - startTime) / 1000;
            const playerName = prompt("Enter your name:");

            const requestData = {
                player_name: playerName,
                completion_time: completionTime,
                moves: moves,
            };

            const response = await fetch('/submit_score', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData),
            });

            if (response.ok) {
                const data = await response.json();
                alert('Score submitted successfully!');
            } else {
                const errorData = await response.json();
                alert('Error: ' + errorData.error);
            }
        } catch (error) {
            console.error('Error submitting score:', error);
            alert('An error occurred while submitting the score. Please try again later.');
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
                startGame(); // 重新开始游戏
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

    function generateCardArray(numPairs) {
        const cards = [];
        for (let i = 1; i <= numPairs; i++) {
            cards.push(i);
            cards.push(i);
        }
        return cards;
    }

    function shuffle(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }
});
