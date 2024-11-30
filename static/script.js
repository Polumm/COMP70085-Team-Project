// script.js
document.addEventListener("DOMContentLoaded", () => {
    const gameBoard = document.getElementById('game-board');

    // 生成卡片数（双数，因为每个图片需要配对）
    const numPairs = 8;

    async function getRandomImages() {
        const apiKey = "amBRe7czSSZTFwnopRm0iqwa4CRLZc3lMYqIR-p15cE";  // 请替换为你从 Unsplash 获取的 API Key
        const response = await fetch(`https://api.unsplash.com/photos/random?client_id=${apiKey}&count=${numPairs}`);
        const data = await response.json();
        
        // 返回16张图片（每张图片有一对）
        return [...data, ...data].map(item => item.urls.small);
    }

    async function startGame() {
        const images = await getRandomImages();
        const shuffledImages = images.sort(() => Math.random() - 0.5);

        // 清空游戏面板
        gameBoard.innerHTML = '';

        // 创建卡片
        shuffledImages.forEach((imageSrc, index) => {
            const card = createCard(imageSrc, index);
            gameBoard.appendChild(card);
        });
    }

    function createCard(imageSrc, index) {
        // 创建卡片元素
        const card = document.createElement('div');
        card.classList.add('card');
        card.dataset.index = index;

        // 创建卡片内层，用于翻转
        const cardInner = document.createElement('div');
        cardInner.classList.add('card-inner');

        // 创建卡片正面
        const cardFront = document.createElement('div');
        cardFront.classList.add('card-front');
        cardFront.textContent = "Card";

        // 创建卡片背面
        const cardBack = document.createElement('div');
        cardBack.classList.add('card-back');
        const img = document.createElement('img');
        img.src = imageSrc;
        cardBack.appendChild(img);

        // 组装卡片
        cardInner.appendChild(cardFront);
        cardInner.appendChild(cardBack);
        card.appendChild(cardInner);

        // 添加点击事件
        card.addEventListener('click', () => {
            card.classList.toggle('flip');
        });

        return card;
    }

    startGame();
});
