import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

export default {
  async generateMaze(size, onData, onComplete, onError) {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/maze/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'text/event-stream'
        },
        body: JSON.stringify({ size })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let buffer = '';
      while (true) {
        const { value, done } = await reader.read();
        if (done) {
          if (onComplete) onComplete();
          break;
        }
        
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n\n');
        buffer = lines.pop(); // Keep the last, possibly incomplete, line

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const jsonStr = line.substring(6);
            if (jsonStr) {
              try {
                const data = JSON.parse(jsonStr);
                // Pass the whole data object to the callback, not just the maze
                if (onData) onData(data);
              } catch (e) {
                console.error("Failed to parse maze chunk", e);
              }
            }
          }
        }
      }
    } catch (err) {
      if (onError) onError(err);
      console.error('Failed to generate maze:', err);
    }
  },
  solveDp(maze) {
    return apiClient.post('/solve/dp', { maze });
  },
  solveGreedy(maze) {
    return apiClient.post('/solve/greedy', { maze });
  },
  solvePuzzle(puzzleData) {
    return apiClient.post('/solve/puzzle', {
      password_hash: puzzleData.password_hash,
      constraints: puzzleData.constraints,
    });
  },
  solveBossBattle(bossHps, skills) {
    // Use boss_hps to match the updated Pydantic model
    return apiClient.post('/solve/boss', { boss_hps: bossHps, skills });
  },
};
