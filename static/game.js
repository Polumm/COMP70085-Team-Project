document.addEventListener('DOMContentLoaded', () => {
    const gameBoard = document.getElementById('game-board');
    let game_id = null;
    let lockBoard = false;
    let startTime = null;
    let moves = 0;

    window.startGame = async function() {
        try {
            // 生成一个 4 到 20 之间的随机对数
            const numPairs = Math.floor(Math.random() * 17) + 4;
            const totalCards = numPairs * 2;

            // 调用 API 创建新游戏
            const response = await fetch(`/create_game/${numPairs}`, { method: 'POST' });
            if (!response.ok) {
                throw new Error('Failed to create game');
            }
            const newGameId = await response.json();
            game_id = newGameId;

            // 重置游戏状态
            gameBoard.innerHTML = '';
            lockBoard = false;
            moves = 0;
            startTime = Date.now();

            // 获取随机图片作为卡片内容
            const imageResponse = await fetch(`/get_random_images?count=${numPairs}`);
            if (!imageResponse.ok) {
                throw new Error('Failed to fetch images');
            }
            const images = await imageResponse.json();

            // 生成游戏卡片
            let cards = generateCardArray(numPairs);
            cards = shuffle(cards);

            // 动态生成卡片布局
            const rows = Math.floor(Math.sqrt(totalCards));
            const cols = Math.ceil(totalCards / rows);
            let cardIndex = 0;

            for (let row = 0; row < rows; row++) {
                const rowElement = document.createElement('div');
                rowElement.classList.add('row');

                for (let col = 0; col < cols; col++) {
                    if (cardIndex >= totalCards) break;
                    const card = cards[cardIndex];
                    const cardElement = document.createElement('div');
                    cardElement.classList.add('card');
                    cardElement.dataset.index = cardIndex;
                    cardElement.innerHTML = `
                        <div class="card-back"></div>
                        <div class="card-front"><img src="${images[card - 1].url}" alt="Card Image"></div>
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
        if (lockBoard || cardElement.classList.contains('flipped')) return;

        // 显示翻转的卡片
        cardElement.classList.add('flipped');
        lockBoard = true;
        moves++;

        // 调用 API 检查卡片是否匹配
        try {
            const cardIndex = cardElement.dataset.index;
            const response = await fetch(`/flip/${game_id}/${cardIndex}`, {
                method: 'POST',
            });
            const result = await response.json();

            if (result.matched) {
                // 如果匹配成功，保持卡片翻开状态
                lockBoard = false;
                if (document.querySelectorAll('.card.flipped').length === numPairs * 2) {
                    setTimeout(submitScore, 500); // 所有卡片匹配成功后提交分数
                }
            } else {
                // 如果匹配失败，将卡片翻回去
                setTimeout(() => {
                    cardElement.classList.remove('flipped');
                    const firstFlippedCard = document.querySelector('.card.flipped:not([data-index="' + cardIndex + '"])');
                    if (firstFlippedCard) {
                        firstFlippedCard.classList.remove('flipped');
                    }
                    lockBoard = false;
                }, 1000);
            }
        } catch (error) {
            console.error('Failed to flip the card:', error);
            setTimeout(() => {
                cardElement.classList.remove('flipped');
                lockBoard = false;
            }, 1000);
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
            const response = await fetch(`/get_time/${game_id}`);
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
            const response = await fetch(`/get_flip_count/${game_id}`);
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
            const response = await fetch(`/reset_game/${game_id}`, { method: 'POST' });
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
            const response = await fetch(`/detect_game_finish/${game_id}`);
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
            const response = await fetch(`/delete_game/${game_id}`, { method: 'DELETE' });
            if (response.ok) {
                console.log('Game deleted successfully');
                game_id = null;
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
