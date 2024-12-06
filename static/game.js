document.addEventListener('DOMContentLoaded', () => {
    const gameBoard = document.getElementById('game-board');
    let gameId = null;
    let lockBoard = false;
    let startTime = null;
    let moves = 0;

    window.startGame = async function () {
        try {
            // 固定卡牌数量为 10 对（20 张卡片）
            const numPairs = 10;
            const totalCards = numPairs * 2;

            // 调用 API 创建新游戏
            const response = await fetch(`/create_default_game`, { method: 'POST' });
            if (!response.ok) {
                throw new Error('Failed to create game');
            }
            const newGameId = await response.json();
            gameId = newGameId;

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

            // 固定生成 5 行 4 列的卡片布局
            const rows = 5;
            const cols = 4;
            let cardIndex = 0;

            for (let row = 0; row < rows; row++) {
                const rowElement = document.createElement('div');
                rowElement.classList.add('row');
                rowElement.style.display = 'flex';
                rowElement.style.justifyContent = 'center';
                rowElement.style.marginBottom = '15px';

                for (let col = 0; col < cols; col++) {
                    if (cardIndex >= totalCards) break;
                    const card = cards[cardIndex];
                    const cardElement = document.createElement('div');
                    cardElement.classList.add('card');
                    cardElement.dataset.index = cardIndex;
                    cardElement.style.width = '80px';
                    cardElement.style.height = '120px';
                    cardElement.style.margin = '10px';
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
            const response = await fetch(`/flip/${gameId}/${cardIndex}`, {
                method: 'POST',
            });
            const result = await response.json();

            if (result === -1) {
                // 如果返回 -1，翻牌无效，翻回去
                setTimeout(() => {
                    cardElement.classList.remove('flipped');
                    lockBoard = false;
                }, 1000);
            } else {
                // 如果返回有效的 secret_index，说明匹配成功或需要移除卡片
                const secretIndex = result;

                // 找到所有和该 secret_index 匹配的卡片
                const matchingCards = document.querySelectorAll(`.card[data-value="${secretIndex}"]`);

                if (matchingCards.length === 2) {
                    // 如果找到两张卡片，移除它们
                    setTimeout(() => {
                        matchingCards.forEach(card => card.remove());
                        lockBoard = false;

                        // 检查游戏是否结束
                        if (document.querySelectorAll('.card').length === 0) {
                            setTimeout(submitScore, 500); // 所有卡片匹配成功后提交分数
                        }
                    }, 500);
                } else {
                    // 如果有问题（例如没有两张卡片），解锁牌板（防止卡住）
                    lockBoard = false;
                }
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
