// 使用 fetch API 从后端获取排行榜数据
async function fetchLeaderboard() {
    try {
        // 发起请求获取排行榜数据
        const response = await fetch('http://localhost:8000/leaderboard'); 
        const data = await response.json();
        const leaderboardContainer = document.getElementById('leaderboard');

        // 清空容器，防止重复渲染
        leaderboardContainer.innerHTML = '';

        // 如果数据为空，显示提示信息
        if (data.length === 0) {
            leaderboardContainer.innerHTML = '<p id="no-data" style="text-align: center;">No leaderboard data available.</p>';
            return;
        }

        // 遍历数据并创建 HTML 元素
        data.forEach((player, index) => {
            const playerElement = document.createElement('div');
            playerElement.classList.add('leaderboard-item');

            // 创建玩家条目，包含排名、玩家名字和完成时间
            playerElement.innerHTML = `<strong>#${index + 1} ${player.player_name}</strong> <span>${player.moves}</span> <span>${player.completion_time}</span>`;

            // 将生成的玩家条目添加到排行榜容器中
            leaderboardContainer.appendChild(playerElement);
        });
    } catch (error) {
        console.error('Error fetching leaderboard data:', error);
        // 请求失败时，显示错误信息
        document.getElementById('leaderboard').innerHTML = '<p id="no-data" style="text-align: center;">Failed to load leaderboard. Please try again later.</p>';
    }
}

// 在页面加载完成后调用函数
window.onload = fetchLeaderboard;
