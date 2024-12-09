// 使用 fetch API 从后端获取排行榜数据
async function fetchLeaderboard() {
    try {
        // 发起请求获取排行榜数据
        const response = await fetch("/fetch_leaderboard");
        const data = await response.json();
        const leaderboardContainer = document.getElementById('leaderboard');

        // 清空容器，防止重复渲染
        leaderboardContainer.innerHTML = '';

        // 如果数据为空，显示提示信息
        if (data.length === 0) {
            leaderboardContainer.innerHTML = '<p id="no-data" style="text-align: center;">No leaderboard data available.</p>';
            return;
        }

        // // 遍历数据并创建 HTML 元素
        // data.forEach((player, index) => {
        //     const playerElement = document.createElement('div');
        //     playerElement.classList.add('leaderboard-item');

        //     // 创建玩家条目，包含排名、玩家名字和完成时间
        //     // playerElement.innerHTML = `<div class="leaderboard-item-content"><strong>#${index + 1} ${player.player_name}</strong></div> <div class="leaderboard-item-content"><span>${player.moves}</span></div> <div class="leaderboard-item-content"><span>${player.completion_time}</span></div>`;
        //     playerElement.innerHTML = `<strong>#${index + 1} ${player.player_name}</strong> <span>${player.moves}</span> <span>${player.completion_time}</span>`;

        //     // 将生成的玩家条目添加到排行榜容器中
        //     leaderboardContainer.appendChild(playerElement);
        // });
                // Create a table for the leaderboard
                const table = document.createElement('table');
                table.classList.add('leaderboard-table');
        
                // Add a header row
                const headerRow = document.createElement('thead');
                headerRow.innerHTML = `
                    <tr>
                        <th>Rank</th>
                        <th>Player Name</th>
                        <th>Moves</th>
                        <th>Completion Time</th>
                    </tr>
                `;
                table.appendChild(headerRow);
        
                // Add a body for player data
                const tableBody = document.createElement('tbody');
                data.forEach((player, index) => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${index + 1}</td>
                        <td>${player.player_name}</td>
                        <td>${player.moves}</td>
                        <td>${player.completion_time}</td>
                    `;
                    tableBody.appendChild(row);
                });
                table.appendChild(tableBody);
        
                // Append the table to the container
                leaderboardContainer.appendChild(table);
    } catch (error) {
        console.error('Error fetching leaderboard data:', error);
        // 请求失败时，显示错误信息
        document.getElementById('leaderboard').innerHTML = '<p id="no-data" style="text-align: center;">Failed to load leaderboard. Please try again later.</p>';
    }
}

// 在页面加载完成后调用函数
window.onload = fetchLeaderboard;
