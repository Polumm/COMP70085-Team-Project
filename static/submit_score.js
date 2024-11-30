// 使用 fetch API 从后端提交分数数据
async function submitScore() {
    // 获取表单中的数据
    const playerName = document.getElementById('player_name').value;
    const completionTime = document.getElementById('completion_time').value;
    const moves = document.getElementById('moves').value;

    // 创建请求的数据对象
    const requestData = {
        player_name: playerName,
        // TODO 
        completion_time: parseInt(completionTime),
        moves: parseInt(moves)
    };

    try {
        // 发送 POST 请求到 API
        const response = await fetch('http://localhost:8000/submit_score', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
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
